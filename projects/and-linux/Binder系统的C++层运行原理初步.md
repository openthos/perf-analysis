# 1 前言

本文是《深入理解Android：卷1》中 第6章 深入理解Binder 的读书笔记。
作者：邓平凡，ISBN：9787111389187。

这本书的第6章从MediaServer服务的启动、提供服务的角度叙述了Android中的Binder在C++层面的运行原理（书中说是深刻的揭示了Binder的原理，然而Binder驱动层并没有说）。
原书中的Android版本较老，为 Android 2.2 ，可喜的是到 Android 6.0 ，这些底层的组件大致运行原理变化并不大。

推荐与原书和我画的调用图同时食用，效果更佳。
这个调用图可谓是我看完这章的结晶，本文的内容也是围绕这个调用图来说的。
二维的图比线性的文字描述更直观，调用图尺寸非常大，建议下载下来看。
下载地址：https://raw.githubusercontent.com/openthos/research-analysis/master/projects/and-linux/image/MediaServer_calling_process.svg

在Android 6.0中，涉及到的源代码文件位置如下：
frameworks/av/media/mediaserver/Main_mediaserver.cpp
frameworks/native/libs/binder/ProcessState.cppframeworks/native/libs/binder/IServiceManager.cpp
frameworks/native/libs/binder/BpBinder.cpp
frameworks/native/libs/binder/Binder.cpp
frameworks/native/libs/binder/IPCThreadState.cpp
frameworks/native/include/binder/IInterface.h
frameworks/native/include/binder/IPCThreadState.h
frameworks/native/include/binder/IServiceManagerManager.h
frameworks/av/media/libmediaplayerservice/MediaPlayerService.cpp

# 2 MediaServer 服务的启动

`MediaServer`顾名思义，就是提供多媒体功能的一个服务。一个服务想在Android中运行都得注册到一个叫做ServiceManager的组件。所以启动的过程就是自己初始化和注册到ServiceManager的过程。

它的运行入口在`Main_mediaserver.cpp`中的main函数。
``` c++
int main(int argc, char** argv)
{
    ……

    //获得一个ProcessState实例
    sp<ProcessState> proc(ProcessState::self());

    //MS作为ServiceManager的客户端，需要向ServiceManager注册服务
    //调用defaultServiceManager，得到一个IserviceManager
    sp<IServiceManager> sm = defaultServiceManager();

    //初始化音频系统的AudioFlinger服务
    AudioFlinger::instantiate();

    //多媒体系统的MediaPlayer服务，我们将以它作为主切入点
    MediaPlayerService::instantiate();

    CameraService::instantiate();
    AudioPolicyService::instantiate();

    //创建线程池，新启动的线程里面也会调用joinThreadPool读取binder设备    ProcessState::self()->startThreadPool();
    //主线程调用joinThreadPool读取binder设备，查看是否有请求
    IPCThreadState::self()->joinThreadPool();
}
```
## 2.1 获得一个 ProcessState 实例

我们可以看到这个入口函数如上所示，我已经删除了一些不太影响流程的语句，只保留了重要的语句，下面出现的代码也如此。

首先运行了`sp<ProcessState> proc(ProcessState::self());`，它创建了一个ProcessState实例。ProcessState是每个进程都有的一个对象。

### 2.1.1 打开 /dev/binder 文件

`ProcessState::self()`函数在`ProcessState.cpp`文件中，它返回了一个`new ProcessState`对象。而ProcessState的初始化里面有一个重要的动作就是`open_driver()`，可以看到这个函数**打开了`"/dev/binder"`文件**，并且把打开的fd存储了起来。这个文件就是Binder驱动文件，打开它才能和Binder通信，以及提供服务。

这是非常重要的一个过程，Android中的绝大部分跨进程通信都是通过`ioctl`操作这个文件。

`ProcessState.cpp`文件如下：
``` c++
sp<ProcessState> ProcessState::self()
{
    Mutex::Autolock _l(gProcessMutex);
    if (gProcess != NULL) {
        return gProcess;
    }
    gProcess = new ProcessState;
    return gProcess;
}

……

ProcessState::ProcessState()
    : mDriverFD(open_driver())
    , mVMStart(MAP_FAILED)
    , mThreadCountLock(PTHREAD_MUTEX_INITIALIZER)
    , mThreadCountDecrement(PTHREAD_COND_INITIALIZER)
    , mExecutingThreadsCount(0)
    , mMaxThreads(DEFAULT_MAX_BINDER_THREADS)
    , mManagesContexts(false)
    , mBinderContextCheckFunc(NULL)
    , mBinderContextUserData(NULL)
    , mThreadPoolStarted(false)
    , mThreadPoolSeq(1)
{
    if (mDriverFD >= 0) {
#if !defined(HAVE_WIN32_IPC)
        mVMStart = mmap(0, BINDER_VM_SIZE, PROT_READ, MAP_PRIVATE | MAP_NORESERVE, mDriverFD, 0);
……
}

static int open_driver()
{
    int fd = open("/dev/binder", O_RDWR);
    if (fd >= 0) {
……
        size_t maxThreads = DEFAULT_MAX_BINDER_THREADS;
        result = ioctl(fd, BINDER_SET_MAX_THREADS, &maxThreads);
…...
    return fd;
}
```
现在我们暂时知道这些就够了。

## 2.2 得到一个IServiceManager来操作ServiceManager

MediaServer 作为 ServiceManager 的客户端，需要向 ServiceManager 注册服务。因此`sp<IServiceManager> sm = defaultServiceManager();`调用defaultServiceManager，得到一个IServiceManager。这个IServiceManager就是ServiceManager组件的一个代理类，这是使用了代理模式，操作代理类，就如同操作远程的本体。

`defaultServiceManager()`函数的位置在`IServiceManager.cpp`文件。

``` c++
......

sp<IServiceManager> defaultServiceManager()
{
    if (gDefaultServiceManager != NULL) return gDefaultServiceManager;

    {
        AutoMutex _l(gDefaultServiceManagerLock);
        while (gDefaultServiceManager == NULL) {
	//相当于interface_cast<IServiceManager>(new BpBinder(0))功能
            gDefaultServiceManager = interface_cast<IServiceManager>(
                ProcessState::self()->getContextObject(NULL));
            if (gDefaultServiceManager == NULL)
                sleep(1);
        }
    }

    return gDefaultServiceManager;
}

......
```

这中间关键的一行就是`gDefaultServiceManager = interface_cast<IServiceManager>(ProcessState::self()->getContextObject(NULL));`。

这一行非常复杂，先说说里面`ProcessState::self()->getContextObject(NULL)`，这个函数在之前所说的`ProcessState.cpp`文件里。

``` c++
sp<IBinder> ProcessState::getContextObject(const sp<IBinder>& /*caller*/)
{
    return getStrongProxyForHandle(0);
}
……
sp<IBinder> ProcessState::getStrongProxyForHandle(int32_t handle)
{
    sp<IBinder> result;

    AutoMutex _l(mLock);

    handle_entry* e = lookupHandleLocked(handle);

    if (e != NULL) {
        IBinder* b = e->binder;
        if (b == NULL || !e->refs->attemptIncWeak(this)) {
            if (handle == 0) {
…...
                Parcel data;
                status_t status = IPCThreadState::self()->transact(
                        0, IBinder::PING_TRANSACTION, data, NULL, 0);
                if (status == DEAD_OBJECT)
                   return NULL;
            }

            b = new BpBinder(handle);	//创建一个新的BpBiner
            e->binder = b;
            if (b) e->refs = b->getWeakRefs();
            result = b;
        } else {
            result.force_set(b);
            e->refs->decWeak(this);
        }
    }

    return result;	//返回BpBinder，注意handle的值为0
}
…...
```
它在里面直接返回了一个`getStrongProxyForHandle(0)`，这个函数里面先与ServiceManager通信，然后创建了一个`new BpBinder(handle)`，并赋值给result返回。

`IPCThreadState::self()->transact(0, IBinder::PING_TRANSACTION, data, NULL, 0)`就是与ServiceManager通信，transact第一个参数0就代表ServiceManager，我们暂时先不去看里面的细节。如果通信成功就创建继续BpBinder。

### 2.2.1 创建代理对象BpBinder

BpBinder继承了IBinder类，它们是Binder通信的使者（代理模式），BpBinder是使用者（客户端）的代理对象，所以在这里新建的是BpBinder。还有个BBinder类也继承IBinder，这是给服务提供者用的，在这里也就是ServiceManager。

BpBinder类在`BpBinder.cpp`文件。

``` c++
…...
BpBinder::BpBinder(int32_t handle)
    : mHandle(handle)
    , mAlive(1)
    , mObitsSent(0)
    , mObituaries(NULL)
{
    ALOGV("Creating BpBinder %p handle %d\n", this, mHandle);

    extendObjectLifetime(OBJECT_LIFETIME_WEAK);
    IPCThreadState::self()->incWeakHandle(handle);
}
……
```

### 2.2.2 服务标识 handle

可以看到这里保存了一个`handle`值，这个 handle 相当于一个编号，每个服务都有一个独一无二的编号。从函数调用我们可以看到这里handle的值是从`getStrongProxyForHandle(0)`这里传进来的，也就是0。所以handle=0就代表ServiceManager，它的handle值是固定的。

对，ServiceManager就是一个服务，它的功能就是管理Android中的服务，所以我们的MediaServer才需要向它注册，其他想使用MediaServer的客户端也得向ServiceManager查询有没有MediaService服务，有的话并且请求合法，就会把MediaService的handle值发过去。

所以，到时候我们操作这个BpBinder就可以连接到ServiceManager。

### 2.2.3 interface_cast 转换

`gDefaultServiceManager = interface_cast<IServiceManager>(ProcessState::self()->getContextObject(NULL));`这里面`ProcessState::self()->getContextObject(NULL)`就相当于`new BpBinder(0)`对象。

interface_cast的代码在`IInterface.h`里面。

``` c++
…...
template<typename INTERFACE>
inline sp<INTERFACE> interface_cast(const sp<IBinder>& obj)
{
    return INTERFACE::asInterface(obj);
}
……
#define DECLARE_META_INTERFACE(INTERFACE)                               \
    static const android::String16 descriptor;                          \
    //定义一个asInterface函数，函数实现在IServiceManager.cpp里
    static android::sp<I##INTERFACE> asInterface(                       \
            const android::sp<android::IBinder>& obj);                  \
    virtual const android::String16& getInterfaceDescriptor() const;    \
    I##INTERFACE();                                                     \
    virtual ~I##INTERFACE();                                            \


#define IMPLEMENT_META_INTERFACE(INTERFACE, NAME)                       \
    const android::String16 I##INTERFACE::descriptor(NAME);             \
    const android::String16&                                            \
            I##INTERFACE::getInterfaceDescriptor() const {              \
        return I##INTERFACE::descriptor;                                \
    }                                                                   \
//实现asInterface函数
    android::sp<I##INTERFACE> I##INTERFACE::asInterface(                \
            const android::sp<android::IBinder>& obj)                   \
    {                                                                   \
        android::sp<I##INTERFACE> intr;                                 \
        if (obj != NULL) {                                              \
            intr = static_cast<I##INTERFACE*>(                          \
                obj->queryLocalInterface(                               \
                        I##INTERFACE::descriptor).get());               \
            if (intr == NULL) {                                         \
//把BpBinder指针转换成一个IserviceManager指针obj；new类名是BpServiceManager
                intr = new Bp##INTERFACE(obj);                          \
            }                                                           \
        }                                                               \
        return intr;                                                    \
    }                                                                   \
    I##INTERFACE::I##INTERFACE() { }                                    \
    I##INTERFACE::~I##INTERFACE() { }                                   \


#define CHECK_INTERFACE(interface, data, reply)                         \
    if (!data.checkInterface(this)) { return PERMISSION_DENIED; }       \

……

template<typename INTERFACE>
inline BpInterface<INTERFACE>::BpInterface(const sp<IBinder>& remote)
    : BpRefBase(remote)	//基类构造函数
{
}

…...
```

可以看到里面返回了`INTERFACE::asInterface(obj);`。
这个`INTERFACE`的asInterface函数在`IServiceManager.h`文件里创建。
这个文件里调用了`DECLARE_META_INTERFACE(ServiceManager);`来创建成员函数。

### 2.2.4 DECLARE_META_INTERFACE(INTERFACE) 宏

而`#define DECLARE_META_INTERFACE(INTERFACE)`宏的定义仍然在上面的`IInterface.h`文件里。

``` c++
……

class IServiceManager : public IInterface
{
public:
    DECLARE_META_INTERFACE(ServiceManager);	//关键无比的宏
    //下面是业务函数
    virtual sp<IBinder>         getService( const String16& name) const = 0;

    virtual sp<IBinder>         checkService( const String16& name) const = 0;

    virtual status_t            addService( const String16& name,
                                            const sp<IBinder>& service,
                                            bool allowIsolated = false) = 0;

    virtual Vector<String16>    listServices() = 0;

    enum {
        GET_SERVICE_TRANSACTION = IBinder::FIRST_CALL_TRANSACTION,
        CHECK_SERVICE_TRANSACTION,
        ADD_SERVICE_TRANSACTION,
        LIST_SERVICES_TRANSACTION,
    };
};

…...
```
这个宏里用INTERFACE带入`static android::sp<I##INTERFACE> asInterface(const android::sp<android::IBinder>& obj); `，因此在IServiceManager里声明的函数是返回值为`sp<IServiceManager>`的函数`asInterface`。

而这个函数的实现也在`IInterface.h`，`#define IMPLEMENT_META_INTERFACE(INTERFACE, NAME)`。
可以看到这里面调用了` intr = new Bp##INTERFACE(obj);`，而这个对象经过宏的转换就是`BpServiceManager`，里面的obj参数就是之前所说的BpBinder的指针，可以从传参看到。这个`inir`的类型则是`BpServiceManager`的父类`IServiceManager`。asInterface函数最后将这个对象返回。

因此`gDefaultServiceManager = interface_cast<IServiceManager>(ProcessState::self()->getContextObject(NULL));`最终相当于`gDefaultServiceManager = new BpServiceManager(new BpBinder(0))`。

我们的` sp<IServiceManager> sm = defaultServiceManager();`最终拿到的就是`new BpServiceManager(new BpBinder(0))`或者说是`new IServiceManger()`，通过这个代理对象操作ServiceManager。

## 2.3 初始化AudioFlinger服务

回到MediaServer的入口函数，继续看下一行。
`AudioFlinger::instantiate();`则是初始化音频系统的AudioFlinger服务。

这个函数在`MeidaPlayerService.cpp`文件里。

``` c++
…...

void MediaPlayerService::instantiate() {
    defaultServiceManager()->addService(
            String16("media.player"), new MediaPlayerService());
}

…...
```

可以看到它调用了`defaultServiceManager()->addService`函数。
这个函数用于向ServiceManager注册自己，即向ServiceManager发送注册信息。
这个函数在`IServiceManager.cpp`文件中。

``` c++
……

    virtual status_t addService(const String16& name, const sp<IBinder>& service,
            bool allowIsolated)
    {
        status_t err;
        for (int i=0; i<ADD_SERVICE_RETRY_SECS; i++) {
            Parcel data, reply;
            data.writeInterfaceToken(IServiceManager::getInterfaceDescriptor());
            data.writeString16(name);
            data.writeStrongBinder(service);
            data.writeInt32(allowIsolated ? 1 : 0);
//remote返回的是mRemote，也就是BpBinder对象
            err = remote()->transact(ADD_SERVICE_TRANSACTION, data, &reply);
            if (err == NO_ERROR)
                return reply.readExceptionCode();
            …...
        }
        return err;
    }
……
```

这个函数中，主要调用`remote()->transact(ADD_SERVICE_TRANSACTION, data, &reply)`函数进行远程通信。
可以看到它的通信命令就是`ADD_SERVICE_TRANSACTION`。`remote()`函数返回就是BpBinder对象，我们就不去看了。

transact函数在`BpBinder.cpp`里。

``` c++
status_t BpBinder::transact(
    uint32_t code, const Parcel& data, Parcel* reply, uint32_t flags)
{
    if (mAlive) {
//将工作交给IPCThreadState
        status_t status = IPCThreadState::self()->transact(
            mHandle, code, data, reply, flags);
        if (status == DEAD_OBJECT)
            if (this != ProcessState::self()->getContextObject(NULL).get())
                mAlive = 0;
        return status;
    }
    return DEAD_OBJECT;
}
```

可以看到，里面调用了`IPCThreadState::self()->transact(mHandle, code, data, reply, flags);`。
IPCThreadState则是一个进程中的每个线程都有一个对象，它则是真正负责传输的对象，传输工作由它负责。

IPCThreadState的代码在`IPCThreadState.cpp`文件。

``` c++
……

status_t IPCThreadState::transact(int32_t handle,
                                  uint32_t code, const Parcel& data,
                                  Parcel* reply, uint32_t flags)
{
    status_t err = data.errorCheck();

    flags |= TF_ACCEPT_FDS;
……	//BC_TRANSACTION是应用程序向binder设备发送消息的消息码
        err = writeTransactionData(BC_TRANSACTION, flags, handle, code, data, NULL);
…...
            err = waitForResponse(reply);
…...
    return err;
}

……

IPCThreadState::IPCThreadState()
    : mProcess(ProcessState::self()),
      mMyThreadId(gettid()),
      mStrictModePolicy(0),
      mLastTransactionBinderFlags(0)
{
    pthread_setspecific(gTLS, this);	//把自己设置到线程本地存储中去
    clearCaller();
//mIn和mOut是两个Parcel，把它看成是发送和接收命令的缓冲区即可
    mIn.setDataCapacity(256);
    mOut.setDataCapacity(256);
}

……

status_t IPCThreadState::waitForResponse(Parcel *reply, status_t *acquireResult)
{
    uint32_t cmd;
    int32_t err;

    while (1) {
        if ((err=talkWithDriver()) < NO_ERROR) break;
        err = mIn.errorCheck();
        if (err < NO_ERROR) break;
        if (mIn.dataAvail() == 0) continue;

        cmd = (uint32_t)mIn.readInt32();

        IF_LOG_COMMANDS() {
            alog << "Processing waitForResponse Command: "
                << getReturnString(cmd) << endl;
        }

        switch (cmd) {
        case BR_TRANSACTION_COMPLETE:
            if (!reply && !acquireResult) goto finish;
            break;

        ……

        default:
            err = executeCommand(cmd);
            if (err != NO_ERROR) goto finish;
            break;
        }
    }

finish:
    if (err != NO_ERROR) {
        if (acquireResult) *acquireResult = err;
        if (reply) reply->setError(err);
        mLastError = err;
    }

    return err;
}

status_t IPCThreadState::talkWithDriver(bool doReceive)
{
    if (mProcess->mDriverFD <= 0) {
        return -EBADF;
    }

    binder_write_read bwr;

    // Is the read buffer empty?
    const bool needRead = mIn.dataPosition() >= mIn.dataSize();

    const size_t outAvail = (!doReceive || needRead) ? mOut.dataSize() : 0;

    bwr.write_size = outAvail;
    bwr.write_buffer = (uintptr_t)mOut.data();

    // This is what we'll read.
    if (doReceive && needRead) {
        bwr.read_size = mIn.dataCapacity();
        bwr.read_buffer = (uintptr_t)mIn.data();
    } else {
        bwr.read_size = 0;
        bwr.read_buffer = 0;
    }
…...
    if ((bwr.write_size == 0) && (bwr.read_size == 0)) return NO_ERROR;

    bwr.write_consumed = 0;
    bwr.read_consumed = 0;
    status_t err;
    do {
…...
#if defined(HAVE_ANDROID_OS)
//可以看到是ioctl调用
        if (ioctl(mProcess->mDriverFD, BINDER_WRITE_READ, &bwr) >= 0)
            err = NO_ERROR;
        else
            err = -errno;
#else
        err = INVALID_OPERATION;
#endif
        if (mProcess->mDriverFD <= 0) {
            err = -EBADF;
        }
…...
    } while (err == -EINTR);
…...
    if (err >= NO_ERROR) {
        if (bwr.write_consumed > 0) {
            if (bwr.write_consumed < mOut.dataSize())
                mOut.remove(0, bwr.write_consumed);
            else
                mOut.setDataSize(0);
        }
        if (bwr.read_consumed > 0) {
            mIn.setDataSize(bwr.read_consumed);
            mIn.setDataPosition(0);
        }
…...
        return NO_ERROR;
    }

    return err;
}

status_t IPCThreadState::writeTransactionData(int32_t cmd, uint32_t binderFlags,
    int32_t handle, uint32_t code, const Parcel& data, status_t* statusBuffer)
{
    binder_transaction_data tr;

    tr.target.ptr = 0; /* Don't pass uninitialized stack data to a remote process */
    tr.target.handle = handle;
    tr.code = code;
    tr.flags = binderFlags;
    tr.cookie = 0;
    tr.sender_pid = 0;
    tr.sender_euid = 0;

    const status_t err = data.errorCheck();
    if (err == NO_ERROR) {
        tr.data_size = data.ipcDataSize();
        tr.data.ptr.buffer = data.ipcData();
        tr.offsets_size = data.ipcObjectsCount()*sizeof(binder_size_t);
        tr.data.ptr.offsets = data.ipcObjects();
    } else if (statusBuffer) {
        tr.flags |= TF_STATUS_CODE;
        *statusBuffer = err;
        tr.data_size = sizeof(status_t);
        tr.data.ptr.buffer = reinterpret_cast<uintptr_t>(statusBuffer);
        tr.offsets_size = 0;
        tr.data.ptr.offsets = 0;
    } else {
        return (mLastError = err);
    }
//把命令写到mOut中，而不是直接发出去，可见这个函数有点名不副实
    mOut.writeInt32(cmd);
    mOut.write(&tr, sizeof(tr));

    return NO_ERROR;
}

……

status_t IPCThreadState::executeCommand(int32_t cmd)
{
    BBinder* obj;
    RefBase::weakref_type* refs;
    status_t result = NO_ERROR;

    switch ((uint32_t)cmd) {
    case BR_ERROR:
        result = mIn.readInt32();
        break;
……

    case BR_TRANSACTION:
        {
            binder_transaction_data tr;
            result = mIn.read(&tr, sizeof(tr));
            ALOG_ASSERT(result == NO_ERROR,
                "Not enough command data for brTRANSACTION");
            if (result != NO_ERROR) break;

            Parcel buffer;
            buffer.ipcSetDataReference(
                reinterpret_cast<const uint8_t*>(tr.data.ptr.buffer),
                tr.data_size,
                reinterpret_cast<const binder_size_t*>(tr.data.ptr.offsets),
                tr.offsets_size/sizeof(binder_size_t), freeBuffer, this);
…...
            Parcel reply;
            status_t error;
…...
            if (tr.target.ptr) {

                if (reinterpret_cast<RefBase::weakref_type*>(
                        tr.target.ptr)->attemptIncStrong(this)) {
/这里的reinterpret_cast转换之后的对象就是实现BnServiceXXX对象
                    error = reinterpret_cast<BBinder*>(tr.cookie)->transact(tr.code, buffer,
                            &reply, tr.flags);
                    reinterpret_cast<BBinder*>(tr.cookie)->decStrong(this);
                } else {
                    error = UNKNOWN_TRANSACTION;
                }

            } else {
                error = the_context_object->transact(tr.code, buffer, &reply, tr.flags);
            }
…...
        }
        break;

    case BR_DEAD_BINDER:
        {
            BpBinder *proxy = (BpBinder*)mIn.readPointer();
            proxy->sendObituary();
            mOut.writeInt32(BC_DEAD_BINDER_DONE);
            mOut.writePointer((uintptr_t)proxy);
        } break;

    case BR_CLEAR_DEATH_NOTIFICATION_DONE:
        {//收到驱动发来service死掉的消息，看来只有Bp端能收到
            BpBinder *proxy = (BpBinder*)mIn.readPointer();
            proxy->getWeakRefs()->decWeak(proxy);
        } break;

    case BR_FINISHED:
        result = TIMED_OUT;
        break;

    case BR_NOOP:
        break;

    case BR_SPAWN_LOOPER:
        mProcess->spawnPooledThread(false);//收到驱动指示，创建一个新线程通信
        break;

    default:
        printf("*** BAD COMMAND %d received from Binder driver\n", cmd);
        result = UNKNOWN_ERROR;
        break;
    }

    if (result != NO_ERROR) {
        mLastError = result;
    }

    return result;
}
```

可以看到 IPCThreadState::transact 函数里调用了
`err = writeTransactionData(BC_TRANSACTION, flags, handle, code, data, NULL);`和`err = waitForResponse(reply);`。
writeTransactionData 则是把要发送的数据存储到mOut缓存里。
waitForResponse 里有两个关键调用。
`if ((err=talkWithDriver()) < NO_ERROR) break;`和`err = executeCommand(cmd);`。

`talkWithDriver()`里主要调用`ioctl(mProcess->mDriverFD, BINDER_WRITE_READ, &bwr)`，将数据发送出去，数据存放在`bwr`对象里。

`executeCommand(cmd);`则是用于执行对方返回来的需要执行的操作。

其他的几个服务类似，我们就不一一叙述了。

## 2.4 startThreadPool() &&　joinThreadPool()

入口函数最后执行`ProcessState::self()->startThreadPool();`和`IPCThreadState::self()->joinThreadPool();`。

顾名思义，这两个函数分别启动线程池和加入线程池。
startThreadPool 就是创建线程池，新启动的线程里面也会调用joinThreadPool读取binder设备。
joinThreadPool 就是把当前进程加入线程池。用于读取binder设备，查看是否有请求。
所以，除了创建的线程池在等待客户端的请求，主线程也作为线程池的一部分，也在等待客户端的请求。

startThreadPool 和 joinThreadPool 都在`IPCThreadState.cpp`文件里。

``` c++
……

void IPCThreadState::joinThreadPool(bool isMain)
{
…...
    mOut.writeInt32(isMain ? BC_ENTER_LOOPER : BC_REGISTER_LOOPER);

    set_sched_policy(mMyThreadId, SP_FOREGROUND);

    status_t result;
    do {
        processPendingDerefs();
        // now get the next command to be processed, waiting if necessary
        result = getAndExecuteCommand();

        if (result < NO_ERROR && result != TIMED_OUT && result != -ECONNREFUSED && result != -EBADF) {
…...
            abort();
        }

        if(result == TIMED_OUT && !isMain) {
            break;
        }
    } while (result != -ECONNREFUSED && result != -EBADF);
…...
    mOut.writeInt32(BC_EXIT_LOOPER);
    talkWithDriver(false);
}
……
```
我们看一下 joinThreadPool 函数，这个函数里进入循环，通过`getAndExecuteCommand()`与Binder交互，获取客户端请求。

# 3 总结

书里第六章还有两节，分别讲了ServiceManager和客户端的执行流程，其实和这里类似，就不再说了。

Binder在C++层的原理其实就是这样，主要是类和宏的跳转很绕，实际还是调用ioctl与/dev/binder文件交互，当然这里面其实还有mmap内存加速过程，书里没有说到。服务端在ServiceManager注册之后，启动线程池并发等待来自客户端的请求。

但我想要了解的内容这本书里说的还不够，我想要了解Binder更底层的原理，ioctl之后驱动层发生了什么，所以还有待继续学习。


