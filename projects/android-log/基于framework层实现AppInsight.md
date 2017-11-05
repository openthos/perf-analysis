## 基于framework实现AppInsight的大致思路
 - 应用层的所有override的函数都是从framework层进行调用的，因此可以在framework层找到对应的函数位置插入log，通过log信息知道调用函数的关系，从而确定线程之间的关系，最后找到异步调用的路径
## 实验过程
 - 自定义一个简单App进行实验，该App可以实现多线程的模式
 - 了解从点击事件到界面更新的整个函数调用流程，从onCreate->onClick->thread.start->thread.run->handler.sendMessage->handler.handlerMessage->onCreate
 - 根据应用层的函数调用关系找到framework层的函数关系，具体关系如下：
### onClick点击事件
  - onClick点击事件，调用的是performClick()，插入的Log为4799和4801行，具体代码如下：
```
代码地址：frameworks/base/core/java/android/view/View.java 

            public boolean performClick() {
 4794         final boolean result;
 4795         final ListenerInfo li = mListenerInfo;
 4796         if (li != null && li.mOnClickListener != null) {
 4797             playSoundEffect(SoundEffectConstants.CLICK);
 4798            //获取线程号和线程名称
 4799            Log.i("aaaaaaaa","onClick()  start  " + android.os.Process.myTid() + "  " + Thread.currentThread().getName());
 4800             li.mOnClickListener.onClick(this);
 4801            Log.i("aaaaaaaa","onClick()  end  " + android.os.Process.myTid() + "  " + Thread.currentThread().getName());
 4802 
 4803             result = true;
 4804         } else {
 4805             result = false;
 4806         }
 4807 
 4808         sendAccessibilityEvent(AccessibilityEvent.TYPE_VIEW_CLICKED);
 4809         return result;
 4810     }

```
### thread开启事件
  - thread开启事件，因为thread的开启是调用的java.lang包的thread.java文件，应用层的start首先调用的是libcore的start，然后转调C++层，最后调libcore的run()方法，因此添加的Log如下：
```
代码地址：libcore/libart/src/main/java/java/lang/Thread.java

1086     public synchronized void start() {
1087         Log("aaaaaaaa","Thread start");
1088         checkNotStarted();
1089 
1090         hasBeenStarted = true;
1091 
1092         nativeCreate(this, stackSize, daemon);
1093     }

 842     public void run() {
 843         Log("aaaaaaaa","new Thread start  ");
 844         if (target != null) {
 845             target.run();
 846         }
 847         Log("aaaaaaaa","new Thread end  " );
 848     }
   
   
```
#### sendMessage事件
  - handler.sendMessage事件，应用层的Handler发送消息在子线程完成，且有send和post两种方式，但是不管那种方式最后的调用函数归结为为sendMessageAtTime和
  sendMessageAtFrontOfQueue两个函数，且最终return的都是enqueueMessage函数，所以最终选取enqueueMessage函数的位置进行插Log，具体代码如下：
  ```
  代码地址：frameworks/base/core/java/android/os/MessageQueue.java 
    //其中msg.target.mLooper.mThread.getName()和msg.target.mLooper.mThread.getId()是为了得到目标线程的名称和id，因为target是Handler
    //对象，对应一个looper且对应一个thread，因此可以得到thread的信息
  boolean enqueueMessage(Message msg, long when) {
316         if(!msg.isAsynchronous()  &&  msg.target.getClass().getName() != "android.view.ViewRootImpl$ViewRootHandler" &&
317           msg.target.getClass().getName() !="com.android.internal.view.IInputConnectionWrapper$MyHandler"){
318         Log.i("aaaaaaaa","enqueMessage" + msg + "enque msg" );
319           Log.i("aaaaaaaa","enqueueMessage  start   " + android.os.Process.myTid() + "  " + Thread.currentThread().getName() + "  "
320          +msg.target.mLooper.mThread.getName() + "  " + msg.target.mLooper.mThread.getId());
321         }
322 
323         if (msg.target == null) {
324             throw new IllegalArgumentException("Message must have a target.");
325         }
326         if (msg.isInUse()) {
327             throw new IllegalStateException(msg + " This message is already in use.");
328         }
329 
330         synchronized (this) {
331             if (mQuitting) {
332                 IllegalStateException e = new IllegalStateException(
333                         msg.target + " sending message to a Handler on a dead thread");
334                 Log.w("MessageQueue", e.getMessage(), e);
335                 msg.recycle();
336                 return false;
337             }
               `
               `
               `
375         if(!msg.isAsynchronous()  &&  msg.target.getClass().getName() != "android.view.ViewRootImpl$ViewRootHandler" &&
376            msg.target.getClass().getName() !="com.android.internal.view.IInputConnectionWrapper$MyHandler"){
377          Log.i("aaaaaaaa","enqueMessage" + msg + "enque msg" );
378            Log.i("aaaaaaaa","enqueueMessage  end   " + android.os.Process.myTid() + "  " + Thread.currentThread().getName() + "  "
379           +msg.target.mLooper.mThread.getName() + "  " + msg.target.mLooper.mThread.getId());
380          }
381     
382         return true;
383 
384     }

  ```
#### handlerMessage事件
  - handler.handlerMessage事件，handlerMessage是handler对子线程发过来的消息进行处理的过程，所以这是在UI线程完成的，在应用层的handlerMessage
    回调的是dispatchMessage,所以在添加UI线程回调处理消息的Log，具体代码如下：
    
  ```
  代码地址：frameworks/base/core/java/android/os/handler.java
  public void dispatchMessage(Message msg) {
 94 
 95          if (!msg.isAsynchronous() && msg.target.getClass().getName() != "android.view.ViewRootImpl$ViewRootHandler" &&
 96          msg.target.getClass().getName() != "com.android.internal.view.IInputConnectionWrapper$MyHandler"){
 97             Log.i("aaaaaaaa","dispatchMessage start   "+android.os.Process.myTid());
 98         }
 99 
100 
101         if (msg.callback != null) {
102             handleCallback(msg);
103         } else {
104             if (mCallback != null) {
105                 if (mCallback.handleMessage(msg)) {
106                     return;
107                 }
108             }
109             handleMessage(msg);
110         }
111 
112          if (!msg.isAsynchronous()  && msg.target.getClass().getName() != "android.view.ViewRootImpl$ViewRootHandler" &&
113          msg.target.getClass().getName() !="com.android.internal.view.IInputConnectionWrapper$MyHandler"){
114            Log.i("aaaaaaaa","dispatchMessage end  " + android.os.Process.myTid());
115          }
116 
117     }

  ```
  
## IntentService开启新线程的Log添加
```
源码地址：frameworks/base/core/java/android/app/IntentService.java

//新线程开启的Log
public void onCreate() {
104         // TODO: It would be nice to have an option to hold a partial wakelock
105         // during processing, and to have a static startService(Context, Intent)
106         // method that would launch the service & hand off a wakelock.
107 
108         super.onCreate();
109         HandlerThread thread = new HandlerThread("IntentService[" + mName + "]");
110         Log.d("IntentService","Thread start "+ android.os.Process.myTid());
111         thread.start();
112         Log.d("IntentService","Thread end "+ android.os.Process.myTid());
113         mServiceLooper = thread.getLooper();
114         mServiceHandler = new ServiceHandler(mServiceLooper);
115     }


// 新线程开启后处理异步任务的Log
private final class ServiceHandler extends Handler {
 59         public ServiceHandler(Looper looper) {
 60             super(looper);
 61         }
 62 
 63         @Override
 64         public void handleMessage(Message msg) {
 65             Log.d("IntentService","new Thread start  "+ android.os.Process.myTid());
 66             onHandleIntent((Intent)msg.obj);
 67             stopSelf(msg.arg1);
 68                 Log.d("IntentService","new Thread end  "+ android.os.Process.myTid());
 69         }
 70     }

```
## 实验结果
  - 现在点击事件、sendMessage和handlerMessage的Log已经可以看到，具体如下,但thread.run的log还存在问题
## 仍存在的问题
  - 虽然目前对log已经进行了一定的筛选，不会大规模的打印无关的log，但是对于复杂的App(例如GT),仍然会有非常多的无关log
  - 对于多线程调用的时间点不够准确
  
  
  
  
  
  
