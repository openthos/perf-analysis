# 2017.07.11~2017.11.02日志

------

Android Binder Demo示例程序，分别从Android应用层(Java)、framework层(Java)、native层(C++)3个角度，通过example阐述如何创建和使用Android Binder IPC实例

https://github.com/yuanhuihui/BinderSample

下载到虚拟机

`/media/deep/data/android-x86/frameworks/BinderSample`

Binder系列8—如何使用Binder

http://gityuan.com/2015/11/22/binder-use/

## 2017-7-13 19:24:43

编译失败
```
unknown package name of class file org/android_x86/analytics/AnalyticsHelper.class
```
不知道是什么情况，重新编译了几次都这样


https://stackoverflow.com/questions/5012163/how-to-discard-changes-using-repo

重置代码
`repo forall -vc "git reset --hard"`

出错，不知道哪错了

换
`make iso_img -j8`
可以编译了。。。

编译成功

进入
`/media/deep/data/android-x86/frameworks/BinderSample/NativeBinderDemo`
编译
`mm`

输出位置
`media/deep/data/android-x86/out/target/product/x86/obj/EXECUTABLES/ServerDemo_intermediates`

新建虚拟机Virtualbox

搞定

## 2017-7-13 23:10:45

[APP] ADB enhanced Putty (replacement for "adb shell" command)
https://forum.xda-developers.com/showthread.php?t=803225

使用adb putty。
对于网络连接的adb，地址输入transport-any

``` shell
root@x86:/system # mkdir test
root@x86:/system # cd test/
root@x86:/system/test # pwd
/system/test
```

见鬼，cygwin出错了
`Error: Could not fork child process: There are no available terminals (-1).`
先不管了
``` shell
adb push ServerDemo /system/test/
adb push ClientDemo /system/test/
```
运行，OK

连接虚拟机
`ssh deep@192.168.50.128`

查看
```
vim ClientDemo.cpp

deep@deep-virtual-machine:/media/deep/data/android-x86/frameworks$ find -name ActivityManagerService.java
./base/services/core/java/com/android/server/am/ActivityManagerService.java

ServiceManager.addService(Context.ACTIVITY_SERVICE, this, true);

deep@deep-virtual-machine:/media/deep/data/android-x86/frameworks$ find -type f|xargs grep "ACTIVITY_SERVICE ="
./base/core/java/android/content/Context.java: public static final String ACTIVITY_SERVICE = "activity";
```
ClientDemo.cpp修改得到
ActivityClientDemo.cpp
``` c++
sp < IServiceManager > sm = defaultServiceManager();
sp < IBinder > binder = sm->getService(String16("activity"))
```
``` shell
export DISPLAY=:0
nautilus .
```
就可以在远程shell启动本地图形界面的资源管理器
``` shell
adb push ActivityClientDemo
chmod +x *
```
可以运行，无报错


就此看来，在JAVA层模拟是最妥的方式

- 手动构建JNI，编译依赖
- 创建Intent，编译程序
- 用root用户发送Intent，运行程序

先想着做第一步，能够自己在JDK上使用JAVA的东西

查找mRemote.transact的代码 JNI
``` java
private IBinder mRemote;
```


在BinderInternal.java里
``` java
public static final native IBinder getContextObject();

方法 android_os_BinderInternal_getContextObject
static jobject android_os_BinderInternal_getContextObject(JNIEnv* env, jobject clazz)
{
  sp<IBinder> b = ProcessState::self()->getContextObject(NULL);
  return javaObjectForIBinder(env, b);
}
```
在ProcessState.cpp里
``` c++
sp<IBinder> ProcessState::getContextObject(const sp<IBinder>& /*caller*/)
{
  return getStrongProxyForHandle(0);
}
```
这个过程就在 MediaServer_calling_process.svg 里有

这个 javaObjectForIBinder(env, b) 里面做了JNI相关的映射
``` c++
jobject javaObjectForIBinder(JNIEnv* env, const sp<IBinder>& val)
```
里面
``` c++
object = env->NewObject(gBinderProxyOffsets.mClass, gBinderProxyOffsets.mConstructor);//创建一个BinderProxy对象
```
可能要学一下 JNI jobject 的原理
``` c++
jobject refObject = env->NewGlobalRef(env->GetObjectField(object, gBinderProxyOffsets.mSelf));//获取BinderProxy内部的成员变量mSelf(BinderProxy的弱引用对象)，接着再创建一个全局引用对象来引用它
```
NewGlobalRef 是 JNI里的全局对象
JNI 支持3中不透明的引用：局部引用、全局引用和弱全局引用

JAVA里
``` java
mRemote.transact(START_ACTIVITY_TRANSACTION, data, reply, 0);
public boolean transact(int code, Parcel data, Parcel reply, int flags)
  throws RemoteException;
```
C++里
``` c++
status_t BpBinder::transact(uint32_t code, const Parcel& data, Parcel* reply, uint32_t flags) 
status_t IPCThreadState::transact(int32_t handle,uint32_t code, const Parcel& data,Parcel* reply, uint32_t flags)
```
transact 的参数是一致的，四个。IPCThreadState::transact里面多个handle而已
这里面涉及一个类Parcel，JAVA里的和C++里的

http://blog.csdn.net/jltxgcy/article/details/29861583

JAVA里的Parcel的方法也是native的。
jobject指的是JNI里用JAVA的对象。

明天看看startActivity里填充哪些参数，以及自己做个JNI调用Parcel，IBinder不需要模拟。

比如 JAVA类 Parcel 的 writeString(String) 方法实现是 nativeWriteString
在 frameworks/base/core/jni/android_os_Parcel.cpp 里
`{"nativeWriteString", "(JLjava/lang/String;)V", (void*)android_os_Parcel_writeString},`

在
`static void android_os_Parcel_writeString(JNIEnv* env, jclass clazz, jlong nativePtr, jstring val)`
里面 直接调用
`err = parcel->writeString16(reinterpret_cast<const char16_t*>(str), env->GetStringLength(val));`
写入

2017-8-5 09:39:45

开始实践，做个Parcel的JNI例子

http://wiki.jikexueyuan.com/project/jni-ndk-developer-guide/workflow.html

JNI 开发流程主要分为以下 6 步：
- 编写声明了 native 方法的 Java 类
- 将 Java 源代码编译成 class 字节码文件
- 用 javah -jni 命令生成.h头文件（-jni 参数表示将 class 中用native 声明的函数生成 JNI 规则的函数）
- 用本地代码实现.h头文件中的函数
- 将本地代码编译成动态库（Windows：\*.dll，linux/unix：\*.so，mac os x：\*.jnilib）
- 拷贝动态库至 java.library.path 本地库搜索目录下，并运行 Java 程序
``` shell
vim HelloWorld.java
javac HelloWorld.java
javah -jni -classpath . HelloWorld
gcc -I. -I/usr/lib/jvm/java-7-openjdk-amd64/include -fPIC -shared HelloWorld.c -o libHelloWorld.so
```
成功输出

注意：ReleaseStringUTFChars要用完在释放，否则取出的c_str会被删除
`(*env)->ReleaseStringUTFChars(env, j_str, c_str);`

方案探讨：

- 方案一，在Android环境里运行，就需要使用Android.mk等在源码里编译。
编译成dex文件，在Android里加载。
- 方案二，在Linux环境里运行，就需要使用JDK和gcc编译。
需要把依赖提取出来。
然后编译成class文件，在Linux环境中运行。

由于依赖提取复杂，采取方案一。
其实可以不需要JNI部分，直接在C++里写就行了。
先编译吧。

## 2017-8-5 20:47:44

编写好了mk和包含startActivity的java文件
``` shell
source build/envsetup.sh
lunch 10
mm
```
报错，需要 AndroidManifest.xml。
写了个空的，还是不行

`recipe for target 'out/target/common/obj/APPS/ActivityDemo_intermediates/with-local/classes.dex' failed`
调用的是
``` shell
java -Dfile.encoding=UTF-8 -Xms2560m -XX:+TieredCompilation -jar out/host/linux-x86/framework/jack-launcher.jar -cp out/
host/linux-x86/framework/jack.jar com.android.jack.server.JackSimpleServer
```

能正确编译的app会提示 Building with Jack。
比如：/media/deep/data/android-x86/development/tutorials/MoarRam

## 2017-9-30 12:29:20

查看之前的进展
``` shell
deep@deep-virtual-machine:/media/deep/data/android-x86$
lunch 10
```
/media/deep/data/android-x86/frameworks/BinderSample/IntentDemo

之前做了一个 JNIParcelTest.java ，编译不了，因为缺少JAVA依赖。

再看看 Anbox 的解决方案

https://github.com/anbox/anbox/blob/master/Android.mk

可以看到 android/service/main.cpp 里面启动anbox的服务，但是这只启动了服务，并不知道apk应用是怎么启动的。

桌面快捷方式是 anbox.desktop 它是个ubuntu snap应用
```
Exec=anbox run --rootfs=android-rootfs

deep@deep-virtual-machine:/$ which anbox
/snap/bin/anbox

anbox -> /usr/bin/snap

strace hello 2> strace_hello

execve("/snap/bin/hello", ["hello"], [/* 54 vars */]) = 0
execve("/snap/core/current/usr/bin/snap", ["/snap/bin/hello"], [/* 55 vars */]) = 0
execve("/snap/core/current/usr/lib/snapd/snap-confine",
```
这个 hello 不知道怎么运行的，只输出一个 Hello, world!
应该是与执行 /snap/core/current/usr/bin/snap 有关

不知道怎么追

看源码 src/anbox/android/intent.cpp 

发现这里面可以直接用cpp解析intent的内容，包括 package action uri 等。

`find -type f | xargs grep 'intent.h' 2> /dev/null`

tests/anbox/android/intent_tests.cpp
这个文件里测试了intent

#include <gtest/gtest.h> 搜不到这个gtest.h

一个突破口，查找谁读写了binder文件
``` shell
deep@deep-virtual-machine:/media/deep/data/anbox$ myfind dev/binder
./scripts/load-kmods.sh:(cd kernel/binder ; make clean && make -j4 ; sudo insmod binder_linux.ko; sudo chmod 666 /dev/binder)
./src/anbox/cmds/session_manager.cpp:    if (!fs::exists("/dev/binder") || !fs::exists("/dev/ashmem")) {
./src/anbox/cmds/session_manager.cpp:        {"/dev/binder", "/dev/binder"},
./src/anbox/cmds/system_info.cpp:constexpr const char *binder_path{"/dev/binder"};
./README.md: * A udev rule to set correct permissions for /dev/binder and /dev/ashmem
```

没什么有用信息，不知道谁打开了它

2017-9-30 22:46:21
明天再看

## 2017-10-1 10:06:15

看了src/CMakeLists.txt

`add_executable(anbox main.cpp)`
发现  src/main.cpp 最后编译成可执行文件anbox
搜了一下  myfind add_executable ，总共只有
```
add_executable(${test_name} ${src})
add_executable(anbox main.cpp)
add_executable(anboxd ${ANBOXD_SOURCES})
add_executable(xdg_test xdg_test.cpp)
add_executable(emugen ${SOURCES})
```
这几个可执行文件

看anbox的main函数
`return daemon.Run(anbox::utils::collect_arguments(argc, argv));`

`anbox::utils::collect_arguments(argc, argv)`
collect_arguments 在 utils.cpp 里，作用是把参数放在了 vector 里
`Daemon::Run` 在 daemon.cpp 里，

## 2017-11-1 12:33:55

src/anbox/cmds/session_manager.cpp
这里面有个
``` c++
251     container::Configuration container_configuration;
252     if (!standalone_) {
253       container_configuration.bind_mounts = {
254         {qemu_pipe_connector->socket_file(), "/dev/qemu_pipe"},
255         {bridge_connector->socket_file(), "/dev/anbox_bridge"},
256         {audio_server->socket_file(), "/dev/anbox_audio"},
257         {SystemConfiguration::instance().input_device_dir(), "/dev/input"},
258         {"/dev/binder", "/dev/binder"},
259         {"/dev/ashmem", "/dev/ashmem"},
260         {"/dev/fuse", "/dev/fuse"},
261       };
```
它把binder文件路径给配置到container_configuration里了

`176     container_ = lxc_container_new("default", container_config_dir.c_str());`

搜不到 lxc_container_new 这个函数，这个应该是LXC的内置函数

不管这个了

bind_mounts 这块是设置容器里的文件挂载的，跟程序逻辑好像没什么关系。

vim tests/anbox/android/intent_tests.cpp
``` c++
23   anbox::android::Intent intent;
```
``` shell
myfind "Intent"
./src/anbox/bridge/android_api_stub.h:1526: void launch(const android::Intent &intent,
./src/anbox/bridge/android_api_stub.cpp:1506:void AndroidApiStub::launch(const android::Intent &intent,
./src/anbox/protobuf/anbox_bridge.proto:156:message Intent {
./src/anbox/dbus/skeleton/application_manager.h:1323: void launch(const android::Intent &intent,
./src/anbox/dbus/skeleton/application_manager.cpp:1565: android::Intent intent;
./src/anbox/dbus/stub/application_manager.h:1372: void launch(const android::Intent &intent,
./src/anbox/dbus/stub/application_manager.cpp:1892:void ApplicationManager::launch(const android::Intent &intent,
./src/anbox/application/manager.h:1024: virtual void launch(const android::Intent &intent,
./src/anbox/application/database.h:993: android::Intent launch_intent;
./src/anbox/cmds/launch.h:1142: android::Intent intent_;
./src/anbox/cmds/session_manager.cpp:3318: android::Intent launch_intent;
./tests/anbox/android/intent_tests.cpp:736:TEST(Intent, IsValid) {
./tests/anbox/application/restricted_manager_tests.cpp:847: MOCK_METHOD3(launch, void(const anbox::android::Intent&,
./android/camera/EmulatedFakeCamera2.cpp:85921: uint8_t controlIntent = 0;
./android/appmgr/src/org/anbox/appmgr/AppsLoader.java:1732: PackageIntentReceiver mPackageObserver;
```
vim src/anbox/bridge/android_api_stub.cpp
``` c++
 53 void AndroidApiStub::launch(const android::Intent &intent,
 54                             const graphics::Rect &launch_bounds,
 55                             const wm::Stack::Id &stack) {

 90   if (!intent.action.empty()) launch_intent->set_action(intent.action);

105   channel_->call_method(
106       "launch_application", &message, c->response.get(),
107       google::protobuf::NewCallback(this, &AndroidApiStub::application_launched,
108                                     c.get()));
```
在set_rpc_channel()里传入的channel
``` c++
 42 void AndroidApiStub::set_rpc_channel(
 43     const std::shared_ptr<rpc::Channel> &channel) {
 44   channel_ = channel;
 45 }
```
``` shell
myfind set_rpc_channel
./src/anbox/cmds/session_manager.cpp:233: android_api_stub->set_rpc_channel(rpc_channel);
```
``` c++
226               auto pending_calls = std::make_shared<rpc::PendingCallCache>();
227               auto rpc_channel =
228                   std::make_shared<rpc::Channel>(pending_calls, sender);
```
std::make_shared这个是C++智能指针的模板函数，指向的就是 rpc::Channel 

 vim src/anbox/rpc/channel.cpp
``` c++
 30 Channel::Channel(const std::shared_ptr<PendingCallCache> &pending_calls,
 31                  const std::shared_ptr<network::MessageSender> &sender)
 32     : pending_calls_(pending_calls), sender_(sender) {}

 36 void Channel::call_method(std::string const &method_name,
 37                           google::protobuf::MessageLite const *parameters,
 38                           google::protobuf::MessageLite *response,
 39                           google::protobuf::Closure *complete) {
 40   auto const &invocation = invocation_for(method_name, parameters);
 41   pending_calls_->save_completion_details(invocation, response, complete);
 42   send_message(MessageType::invocation, invocation);
 43 }
```
找 send_message
``` c++
 73 void Channel::send_message(const std::uint8_t &type,
 74                            google::protobuf::MessageLite const &message) {

 88     sender_->send(reinterpret_cast<const char *>(send_buffer.data()),
 89                   send_buffer.size());

 94 }
```
调用了sender_发送，是构造桉树传入的
``` c++
 const std::shared_ptr<network::MessageSender> &sender
```
myfind class\ MessageSender | less
 vim src/anbox/network/message_sender.h
``` c++
 28  public:
 29   virtual void send(char const* data, size_t length) = 0;
```
没有cpp文件,这个是虚函数，在子类里面进行实现。
``` shell
 myfind :send\(
 myfind "send(char"
./src/anbox/network/base_socket_messenger.cpp:87:void BaseSocketMessenger<stream_protocol>::send(char const* data,
./src/anbox/network/socket_connection.cpp:51:void SocketConnection::send(char const* data, size_t length) {
```
有两个,这不对

myfind public\ MessageSender | less 我的这个myfind脚本还有点问题，遇到空格不能加入进$1去
```
./android/service/local_socket_connection.h:28:class LocalSocketConnection : public network::MessageSender {
./src/anbox/network/socket_messenger.h:30:class SocketMessenger : public MessageSender, public MessageReceiver {
```
看了只有 LocalSocketConnection 实现了send
 vim android/service/local_socket_connection.cpp
``` c++
 60 void LocalSocketConnection::send(char const* data, size_t length) {

 63     while(bytes_written < length) {
 64         ssize_t const result = ::send(fd_,
 65                                       data + bytes_written,
 66                                       length - bytes_written,
 67                                       MSG_NOSIGNAL);

 76     }
 77 }
```
这里面的 ::send 应该就是系统自带的send，有四个参数。
``` c++
 35 namespace anbox {
 36 LocalSocketConnection::LocalSocketConnection(const std::string &path) :
 37     fd_(Fd::invalid) {

 45     fd_ = Fd{socket(AF_UNIX, SOCK_STREAM, 0)};
```
这个fd_是一个unix socket。

也就是这里的intent发送通过rpc_channel -> sender_ -> ::send(

这里面是发送方，没有与Android有任何直接接触，Android的binder是个字符设备文件，不是unix socket。

那么在接收方肯定要与Android接触了。

## 2017-11-1 17:41:28

vim src/anbox/network/message_receiver.h
``` c++
 30 class MessageReceiver {
 31 public:
 32   // receive message from the socket. 'handler' will be called when 'buffer' has
 33   // been filled with exactly 'size'
 34   typedef std::function<void(boost::system::error_code const&, size_t)>
 35       AnboxReadHandler;
 36   virtualvoid async_receive_msg(
 37       AnboxReadHandler const& handler,
 38       boost::asio::mutable_buffers_1 const& buffer) = 0;
```
可以看到这个 async_receive_msg() 函数里，有个AnboxReadHandler来处理
这个 MessageReceiver 类是个虚函数，没有实现这些。

``` shell
 myfind MessageReceiver
./src/anbox/network/socket_messenger.h:30:class SocketMessenger : public MessageSender, public MessageReceiver {
```
只有 SocketMessenger 实现了 MessageReceiver

但是这个 src/anbox/network/socket_messenger.cpp 是空的。。。

vim src/anbox/network/base_socket_messenger.h
``` c++
 31 class BaseSocketMessenger : public SocketMessenger {
```
BaseSocketMessenger 实现了 SocketMessenger 

说明上面的 MessageSender 也有间接继承者，就是 BaseSocketMessenger，这要看sender调用的是
BaseSocketMessenger 还是 LocalSocketConnection

不过接收者就这一个 BaseSocketMessenger

vim src/anbox/network/base_socket_messenger.cpp
``` c++
106 void BaseSocketMessenger<stream_protocol>::async_receive_msg(
107     AnboxReadHandler const& handler, ba::mutable_buffers_1 const& buffer) {
108   socket->async_read_some(buffer, handler);
109 }
```
不过这里的发送和接收都是socket，而且接收只有一个，所以不可能是binder，而且就看这个接收就行了。
``` shell
 myfind async_receive_msg
./src/anbox/container/client.cpp:66: messenger_->async_receive_msg(callback, ba::buffer(buffer_));
./src/anbox/qemu/adb_message_processor.cpp:157: host_messenger_->async_receive_msg(callback, boost::asio::buffer(host_buffer_));
./src/anbox/network/socket_connection.cpp:57: message_receiver_->async_receive_msg(callback, ba::buffer(buffer_));
```
 vim src/anbox/network/socket_connection.cpp
``` c++
 55 void SocketConnection::read_next_message() {
 56   auto callback = std::bind(&SocketConnection::on_read_size, this, std::placeholders::_1, std::placeholders::_2);
 57   message_receiver_->async_receive_msg(callback, ba::buffer(buffer_));
 58 }
 vim src/anbox/container/client.cpp
 63 void Client::read_next_message() {
 64   auto callback = std::bind(&Client::on_read_size, this, std::placeholders::_1,
 65                             std::placeholders::_2);
 66   messenger_->async_receive_msg(callback, ba::buffer(buffer_));
 67 }
```
callback怎么运转的呢。。。

上面这两个类都没有子类

得看谁调用了 read_next_message  函数

Client自己就调用了，而且没有返回值，数据存哪了，Client有个buffer
``` c++
57   std::array<std::uint8_t, 8192> buffer_;
```
## 2017-11-2 17:16:25
``` c++
222     auto bridge_connector = std::make_shared<network::PublishedSocketConnector>(
223         utils::string_format("%s/anbox_bridge", socket_path), rt,
224         std::make_shared<rpc::ConnectionCreator>(
225             rt, [&](const std::shared_ptr<network::MessageSender> &sender) {
226               auto pending_calls = std::make_shared<rpc::PendingCallCache>();
227               auto rpc_channel =
228                   std::make_shared<rpc::Channel>(pending_calls, sender);
```
这里的 [&](const std::shared_ptr<network::MessageSender> &sender) { 看不懂，是会被回调？

所以这里的sender暂时不能确定是哪个类的实例？

之前看了只有 LocalSocketConnection 实现了send

跟踪 buffer_ ，发现

`vim src/anbox/rpc/message_processor.cpp`

只有它可能在处理rpc相关的buffer_，其他的涉及graphics，qemu，camera，opengl
``` c++
 45 bool MessageProcessor::process_data(const std::vector<std::uint8_t> &data) {
 46   for (const auto &byte : data) buffer_.push_back(byte);

 58     if (message_type == MessageType::invocation) {
 59       anbox::protobuf::rpc::Invocation raw_invocation;
 60       raw_invocation.ParseFromArray(buffer_.data() + header_size, message_size);
 61
 62       dispatch(Invocation(raw_invocation));
 63     } else if (message_type == MessageType::response) {
 64       auto result = make_protobuf_object<protobuf::rpc::Result>();
 65       result->ParseFromArray(buffer_.data() + header_size, message_size);
 66
 67       if (result->has_id()) {
 68         pending_calls_->populate_message_for_result(*result,
 69                                                     [&](google::protobuf::MessageLite *result_message) {
 70                                                       result_message->ParseFromString(result->response());
 71                                                     });
 72         pending_calls_->complete_response(*result);
 73       }
 74
 75       for (int n = 0; n < result->events_size(); n++)
 76         process_event_sequence(result->events(n));
 77     }
```
 vim src/anbox/rpc/message_processor.h
``` c++
50 class MessageProcessor : public network::MessageProcessor {

61   virtual void dispatch(Invocation const&) {}
```
发现这个dispatch函数是virtual
``` sehll
 myfind  rpc::MessageProcessor | grep public
./src/anbox/container/management_api_message_processor.h:26:class ManagementApiMessageProcessor : public rpc::MessageProcessor {
./src/anbox/bridge/platform_message_processor.h:26:class PlatformMessageProcessor : public rpc::MessageProcessor {
./android/service/message_processor.h:25:class MessageProcessor : public rpc::MessageProcessor {
```
发现这个文件比较靠谱
 vim android/service/message_processor.cpp
``` c++
 39 void MessageProcessor::dispatch(rpc::Invocation const& invocation) {
 40   if (invocation.method_name() == "launch_application")
 41     invoke(this, platform_api_.get(), &AndroidApiSkeleton::launch_application, invocation);
```
当方法名等于 launch_application

这个方法名确实在src/anbox/bridge/android_api_stub.cpp的106行发出的，应该直接找这个关键字就行了，我还找了半天

这里的 invoke 方法只是个远程调用的包装，以protobuf形式发送数据，在

vim src/anbox/rpc/template_message_processor.h

这个 AndroidApiSkeleton::launch_application 应该是调用方法

vim android/service/android_api_skeleton.cpp
``` c++
 66 void AndroidApiSkeleton::launch_application(anbox::protobuf::bridge::LaunchApplication const *request,
 67                                 anbox::protobuf::rpc::Void *response,
 68                                 google::protobuf::Closure *done) {
 69     (void) response;
 70
 71     auto intent = request->intent();
 72
 73     std::vector<std::string> argv = {
 74         "/system/bin/am",
 75         "start",
 76     };
```
发现最后竟然还是用Android自带的am命令执行intent。。。醉了
失望。但是它的其他功能是如何进行的呢
