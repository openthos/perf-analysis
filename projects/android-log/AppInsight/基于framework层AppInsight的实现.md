# 基于framework层AppInsight的实现
## 1.基础
AppInsight论文主要针对applications层APP的二进制代码进行动态插桩，通过在APP各线程主要函数中插入log，从而实现跨异步调用边界，获取代码执行关键路径
## 2.差异
本项研究主要针对framework层的Android的源码进行静态插桩，在framework层中存在APP各线程主要函数的对应函数，找到这些函数，在其中插入恰当的log，从而实现跨异步调用边界，获取代码执行关键路径
## 3.关键
* 准确的log位置，可以精确表示函数执行的时间
* 恰当的log内容，可以明确获得线程间异步调用因果关系
## 4.测试APP代码
1. **APP1：**
  * 功能：TextView显示内容”hello world“，点击Button，更新TextView的内容为”nice to meet you“
  * 实现方法：主线程创建Handler对象，其handleMessage函数中对TextView的内容进行更新，Button的onClick函数中新建子线程，子线程中通过主线程创建的Handler对象的sendMessage函数发送更新TextView内容的Message对象
## 5.实现过程
### 1. 如何知道某条log信息是由目标进程的哪个线程打印出来的？
* **ps** 可以获得目标进程的进程id
* **ps -t 进程id** 可以获得该进程id下面的所有存活的线程信息
* **logcat -v threadtime | grep 进程id** 可以获得目标进程的log信息，并显示打印出该条log信息的进程号和线程号
### 2. 什么是APP各线程的主要函数？
* **开启新线程的onClick函数** 获取主线程处理click事件的执行时间
* **新线程的start函数** 获取从主线程到子线程的异步调用因果关系
* **新线程的run函数** 获取子线程的执行时间
* **Handler对象的sandMessage函数** 获取从子线程到主线程的异步调用因果关系
* **Handler对象的handleMessage函数** 获取主线程更新ui的执行时间
### 3.framework层中与APP各线程主要函数的对应函数在哪里？
* **开启新线程的onClick函数** 
  * frameworks/base/core/java/android/view/View.java 4798行
  * performClick()中通过li.mOnClickListener.onClick(this);调用Applications层APP的onClick函数
* **新线程的start函数** 
  * libcore/libart/src/main/java/java/lang/Thread.java 1061行 start()
  * 交给了nativeCreate方法执行，并且把当前Thread的实例自己传了进去
  
  ```
  public synchronized void start() {
         checkNotStarted();
         hasBeenStarted = true;
         nativeCreate(this, stackSize, daemon);
     }
  ```
  
  * art/runtime/native/java_lang_Thread.cc 47行 nativeCreate
  * nativeCreate方法，换了方法名，名字换成了CreateNativeThread
  
  ```
  static void Thread_nativeCreate(JNIEnv* env, jclass, jobject java_thread, jlong stack_size,
  jboolean daemon) {
     Thread::CreateNativeThread(env, java_thread, stack_size, daemon == JNI_TRUE);
  }
  ```
  
  * art/runtime/thread.cc 288行 CreateNativeThread
  * 把java层的run方法实体传递给子线程
  
  ```
  child_thread->tlsPtr_.jpeer = env->NewGlobalRef(java_peer);
  ```
  
  * 创建新线程的方法，返回一个标志
  
  ```
  int pthread_create_result = pthread_create(&new_pthread, &attr, Thread::CreateCallback, child_thread);
  ```
  
  * art/runtime/thread.cc 145行 CreateCallback
  * Invoke the 'run' method of our java.lang.Thread.
  
  ```
  mirror::Object* receiver = self->tlsPtr_.opeer;
  jmethodID mid = WellKnownClasses::java_lang_Thread_run;
  InvokeVirtualOrInterfaceWithJValues(soa, receiver, mid, nullptr);
  ```
  * **如何找到主线程和工作线程的因果关系？** 
  
* **新线程的run函数** 
  * libcore/libart/src/main/java/java/lang/Thread.java 816行
  * **现在只是在run函数的头和结尾处打log，调用新线程的run函数的函数位于native层，应该在那个函数里打log，如何打？**  
* **Handler对象的sandMessage函数** 
  * frameworks/base/core/java/android/os/Handler.java 511行
  * Handler对象有多种发送异步消息的方法，通过对这些方法进行分析，总结如下：
    * post(Runnable r)、postDelayed(Runnable r, long delayMillis)、sendEmptyMessageDelayed(int what, long delayMillis)sendMessage(Message msg)会依次调用sendMessageDelayed(getPostMessage(r), 0)sendMessageAtTime(msg, SystemClock.uptimeMillis() + delayMillis)，最终调用enqueueMessage(queue, msg, uptimeMillis)方法实现异步消息的发送
    * postAtTime(Runnable r, long uptimeMillis)、postAtTime(Runnable r, Object token, long uptimeMillis)、sendEmptyMessageAtTime(int what, long uptimeMillis)会调用sendMessageAtTime(getPostMessage(r), uptimeMillis)最终调用enqueueMessage(queue, msg, uptimeMillis)方法实现异步消息的发送
    * postAtFrontOfQueue(Runnable r)会调用sendMessageAtFrontOfQueue(getPostMessage(r))最终调用enqueueMessage(queue, msg, 0)方法实现异步消息的发送
  * 不论Handler对象使用哪种发送异步消息的方法，最终都会调用enqueueMessage(queue, msg, 0)（632行）方法实现异步消息的发送，所以在这个函数里进行插桩
  * enqueueMessage(queue, msg, 0)中通过queue.enqueueMessage(msg, uptimeMillis)将异步消息放入创建Handler对象的线程队列中，最后通过Looper循环取出消息进行处理
  * 根据对Message、Handler、Looper机制的学习，得到msg.target保存的是创建Handler对象的线程，即异步消息最终进行处理的线程，根据Message、Handler、Looper的关系，可以通过msg.target.mLooper.mThread.getName()获取到异步消息最终进行处理的线程名（**线程id没有想到有效的方法获取**）
* **Handler对象的handleMessage函数** 
  * frameworks/base/core/java/android/os/Handler.java 93行 
  * dispatchMessage(Message msg)中通过handleMessage(msg);调用Applications层APP的handleMessage函数
  * Handler对象有多种发送异步消息的方法，所以有多种处理异步消息的方法，并且Handler对象的构造函数也有多种，而dispatchMessage(Message msg)先对多种情况进行了判断，然后根据不同的情况调用不同的函数进行异步消息的处理，所以在dispatchMessage(Message msg)的首尾插桩
### 4.log应该输出什么内容？
* **开启新线程的onClick函数** 
  * 在li.mOnClickListener.onClick(this)的前后分别打log，分别输出线程的id和name，实现获取主线程处理click事件的执行时间
  
  ```
  Log.e("LEILOG","onClick()start-"+android.os.Process.myTid()+"-"+Thread.currentThread().getName());
  li.mOnClickListener.onClick(this);
  Log.e("LEILOG","onClick()end-"+android.os.Process.myTid()+"-"+Thread.currentThread().getName());
  ```
  
* **新线程的start函数** 
* **新线程的run函数** 
  * 在run函数的头和结尾处打log，分别输出线程的id和name，实现获取工作线程异步工作的执行时间
  
  ```
  public void run() {
         Logger logger = Logger.getLogger("LEILOG");
         logger.info("run()start"+Thread.currentThread().getId()+"-"+Thread.currentThread().getName());
         if (target != null) {
             target.run();
         }
         logger.info("run()end"+Thread.currentThread().getId()+"-"+Thread.currentThread().getName());
     }
  ```
  
* **Handler对象的sandMessage函数** 
  * 在return queue.enqueueMessage(msg, uptimeMillis);的前面打log，分别输出发送异步消息的线程id和name与处理异步消息的线程名，实现获取获取从子线程到主线程的异步调用因果关系
  
   ```
   if (!msg.isAsynchronous()){   
    Log.e("LEILOG","enqueueMessage()start-"+android.os.Process.myTid()+"-"+Thread.currentThread().
    getName()+"-"+msg.target.mLooper.mThread.getName());
   }
   return queue.enqueueMessage(msg, uptimeMillis);
   ```
   
  * **获取的log中有很多无关的post和enqueueMessage出现，初步分析和Choreographer等有关，为了更清楚的获取我们打的log，判断log是否正确且有用，此处使用!msg.isAsynchronous()对系统其他的log实现过滤，原理还有待进一步研究，之后会继续分析系统的log是为何产生的，从而获得系统与应用运行的影响**
* **Handler对象的handleMessage函数** 
  * 在dispatchMessage(Message msg)函数的首尾分别打log，分别输出线程的id和name，实现获取主线程更新ui的执行时间
  
  ```
  public void dispatchMessage(Message msg) {
         if (!msg.isAsynchronous() ){
             Log.e("LEILOG","callback or handle start-"+android.os.Process.myTid()+"-"+Thread.
             currentThread().getName());
         }
         if (msg.callback != null) {
             handleCallback(msg);
         } else {
             if (mCallback != null) {
                 if (mCallback.handleMessage(msg)) {
                     return;
                 }
             }
             handleMessage(msg);
         }
         if (!msg.isAsynchronous()){
             Log.e("LEILOG","callback or handle end-"+android.os.Process.myTid()+"-"+Thread.
             currentThread().getName());
         }
     }
  ```
### 5.实验结果
  
  ```
  04-27 14:45:03.978 25162 25162 E LEILOG  : onClick()start-25162-main
  04-27 14:45:03.978 25162 25162 E art     : LEILOG CreateNativeThread 
  04-27 14:45:03.978 25162 25162 E LEILOG  : onClick()end-25162-main
  04-27 14:45:03.978 25162 25162 E LEILOG  : callback or handle end-25162-main
  04-27 14:45:03.978 25162 25162 E LEILOG  : callback or handle start-25162-main
  04-27 14:45:03.978 25162 25162 E LEILOG  : callback or handle end-25162-main
  04-27 14:45:03.978 25162 25187 I LEILOG  : run()start-140017608083456-Thread-172
  04-27 14:45:03.978 25162 25187 E LEILOG  : enqueueMessage()start-25187-Thread-172-main
  04-27 14:45:03.978 25162 25187 I LEILOG  : run()end-140017608083456-Thread-172
  04-27 14:45:03.985 25162 25162 E LEILOG  : callback or handle start-25162-main
  04-27 14:45:03.986 25162 25162 E LEILOG  : callback or handle end-25162-main
  ```
  
### 6.appinsight log 分析方法
* **目标** 
  * 揭示性能变化根源
  * 发现异常事务
* **事务分组** 
  * 将相同图形（相同节点和连接性）的事务分组（保守分组）在一起
* **对每个事务组进行量化方差，分析方差根源** 
  * 影响事务持续时间的因素有网络传输、位置查询和本地处理，将每一个事务的关键路径上事务持续时间分为这三类进行方差分析，从而分析根源
* **异常事务检测** 
  * 大于(mean + (k * standard deviation))的事务为异常事务，本项研究中 k = 3
