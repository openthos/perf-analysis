# HandlerThread
## HandlerThread的特点与适用环境
  
  - HandlerThread本质上是一个Thread对象，只不过其内部帮我们创建了该线程的Looper和MessageQueue
  - 通过HandlerThread我们不但可以实现UI线程与子线程的通信同样也可以实现子线程与子线程之间的通信
  - HandlerThread在不需要使用的时候需要手动的回收掉
  - 使用HandlerThread处理本地IO读写操作（数据库，文件），因为本地IO操作大多数的耗时属于毫秒级别，对于单线程 + 异步队列的形式 不会产生较大的阻塞
## HandlerThread的基本用法

```
/**
 * HandlerThread的初始化：新建对象，并初始化mHandler绑定Looper
 */
HandlerThread mHandlerThread = new HandlerThread("myHandlerThreand");
        mHandlerThread.start();

        // 创建的Handler将会在mHandlerThread线程中执行
        final Handler mHandler = new Handler(mHandlerThread.getLooper()) {
            @Override
            public void handleMessage(Message msg) {
              /*
              *handlerMessage可以处理异步耗时任务
              */
              Log.i("tag", "接收到消息：" + msg.obj.toString());
            }
        };

        title = (TextView) findViewById(R.id.title);
        title.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
              
              /*
              * 在主线程可以发消息给HandlerThread
              */
                Message msg = new Message();
                msg.obj = "11111";
                mHandler.sendMessage(msg);
            }
        });
```
  
## HandlerThread的源码解析

  - HandlerThread的构造函数，HandlerThread本质上是一个线程，其构造方法主要是做一些初始化的操作
  
```
public HandlerThread(String name) {
        super(name);
        mPriority = Process.THREAD_PRIORITY_DEFAULT;
    }
```

  - 我们的基本用法是在App中调用HandlerThread的start方法开启一个HandlerThread，然后调用Thread的run()方法，HandlerThread已经把run()方法写好
  
```
/*
*调用了Looper.prepate()方法和Loop.loop()方法,创建了该线程的Looper与MessageQueue
*/
@Override
    public void run() {
        mTid = Process.myTid();
        Looper.prepare();
        synchronized (this) {
            mLooper = Looper.myLooper();
            notifyAll();
        }
        Process.setThreadPriority(mPriority);
        onLooperPrepared();
        Looper.loop();
        mTid = -1;
    }
```

  - 在HandlerThread初始化以上多有的参数之后，我们在App中就可以通过Looper进行sendMessage和handlerMessage并处理异步任务，最后需要注意的是在我们不需要这个looper线程的时候需要手动停止掉
  
 ```
 protected void onDestroy() {
        super.onDestroy();
        mHandlerThread.quit();
    }
 ```
# IntentService
## IntentService与Thread的区别
  - IntentService 实际上是Looper,Handler,Service 的集合体
  - IntentService是继承于Service并处理异步请求的一个类，在IntentService内有一个工作线程来处理耗时操作，启动IntentService的方式和启动传统Service一样，
  同时，当任务执行完后，IntentService会自动停止，而不需要我们去手动控制。另外，可以启动IntentService多次，而每一个耗时操作会以工作队列的方式在
  IntentService的onHandleIntent回调方法中执行，并且，每次只会执行一个工作线程，执行完第一个再执行第二个，以此类推
  - IntentService是android中开启异步线程的一种方法，程序员不需要new Thread，也不需要start和stop。程序员可以很简单的使用。IntentService可以
  自动开启一个HandleThread，并自动调用intentService中的onHandleIntent()方法来处理异步任务
 
## IntentService的源码解析
  - 首先onCreate()
```
源码地址：/frameworks/base/core/java/android/app/IntentService.java
 public void onCreate() {
        super.onCreate();
       //开启一个新的HandlerThread线程
        HandlerThread thread = new HandlerThread("IntentService[" + mName + "]");
        thread.start();
      // 调用自定义的一个内部类
        mServiceLooper = thread.getLooper();
        mServiceHandler = new ServiceHandler(mServiceLooper);
    }

```
  - 自定义的内部类：ServiceHandler
```
 private final class ServiceHandler extends Handler {
   //构造函数，ServiceHandler与Looper绑定，通过Handler向Looper发消息
   public ServiceHandler(Looper looper) {
            super(looper);
        }
   
   // 当MessageQueue有消息时，handlerMessage处理消息，并调用onHandleIntent处理任务，处理完之后stop
        @Override
        public void handleMessage(Message msg) {
            onHandleIntent((Intent)msg.obj);
            stopSelf(msg.arg1);
        }
    }
```
  - onStartCommand()
```
 public int onStartCommand(@Nullable Intent intent, int flags, int startId) {
        //调用onStart
        onStart(intent, startId);
        return mRedelivery ? START_REDELIVER_INTENT : START_NOT_STICKY;
    }
    
  
  public void onStart(@Nullable Intent intent, int startId) {
        Message msg = mServiceHandler.obtainMessage();
        msg.arg1 = startId;
        msg.obj = intent;
        //sendMessage之后，就可以HandleMessage了
        mServiceHandler.sendMessage(msg);
    }
```
  - 最主要的onHandleIntent()
```
// 抽象方法，应用层重写这个方法进行异步处理任务
protected abstract void onHandleIntent(Intent intent);
```
## 实践的问题
  
  - HandlerThread处理异步任务的时候，一般是在handlerMessage中进行处理，因为它调用的是Handler的sendMessage和handlerMessage，所以对于这个子线程对异步任务处理的时间不好确认
  - 自己写的Demo中，App打开就会开启五六个新的线程，这几个线程并不是Thread.start之后的线程;另外thread.start之后也开启了两个新的线程，他们之间的
  关系是怎样的，哪个线程是我们主要需要关注的
