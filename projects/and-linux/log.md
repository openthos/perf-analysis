# 2017.02.25~2017.03.23日志

-----

# 2017.03.16~2017.03.23

## 1 本周工作：

研究Android中通过Intent发送启动一个Service的发送方的全过程。

在本周五的例会上，听取了师兄的建议，对我的课题思路进行了修改。

## Android中通过Intent发送启动一个Service的发送方的过程

通过前几周的研究，一个APP通过Intent发送一个启动Service的请求的过程已经基本清楚。

主要是通过ActivityManagerService的代理类ActivityManagerProxy，把Intent数据通过Binder发送给ActivityManagerService。

Binder的发送过程是通过JNI在C++层完成的。

![Alt text](https://cdn.rawgit.com/openthos/research-analysis/cd448b296b59edd1d70f48d93b14b74c7282e234/projects/and-linux/image/plan_1_android-app1_start_adnroid-app2_call.svg)

作为Intent发送方，如果从第一次IPC算起，其实需要三次Binder通信过程。

第一次通过 binder 驱动获取 ServiceManager 服务的代理。这个服务是Binder层的管理服务，用来获取Framework层的各种服务。

第二次从ServiceManager获取 ActivityManagerService 服务代理。

第三次向 ActivityManagerService 服务发出请求启动 APP2 的 指定 Service。

![Alt text](https://cdn.rawgit.com/openthos/research-analysis/cd448b296b59edd1d70f48d93b14b74c7282e234/projects/and-linux/image/plan_1_android-app1_start_adnroid-app2_ipc.svg)

## 2 我之前设想的思路

我之前设想通过修改ActivityManagerService等服务能够使得 Android 能够接受来自 Linux 的请求。

这种方式可能需要修改有关权限有关的很多地方，包括Binder权限检测、Framework层的服务等。

![Alt text](https://cdn.rawgit.com/openthos/research-analysis/master/projects/and-linux/image/plan_1_before_linux-start-android-service.svg)

## 3 听取师兄建议后，修改后的思路

在例会上，师兄指出我这种设想侵入性太强，不仅需要在Linux程序上做适配而且，修改了Binder、Framework层。应该找一种方法减少对原有的机制的更改，比如加入一种中间层。

我听取师兄的建议，设想了新的思路。

如下图所示，通过加入 Linux 与Android 中进程间通信方式的转换模块 ，使得在Linux和Android“共有的操作”（还有待研究）上，甚至不用修改Linux上的程序。

然后在Binder驱动中，加入Binder中间层，使得需要通过Bidner通信的程序先走Binder中间层，如果中间层判断该请求为Android内部（与Linux无关）的通信，则传递给原有的binder驱动进行处理。否则拦截进行自定义处理。

![Alt text](https://cdn.rawgit.com/openthos/research-analysis/master/projects/and-linux/image/plan_1_after_linux_start_android_service.svg)

若目标是启动Linux中的Service，则不走Android原有的Binder，直接由中间层操作。

![Alt text](https://cdn.rawgit.com/openthos/research-analysis/master/projects/and-linux/image/plan_1_after_android_start_linux_service.svg)

若目标是Android中的Service，则传递给原有的Bidner，正常处理。

![Alt text](https://cdn.rawgit.com/openthos/research-analysis/master/projects/and-linux/image/plan_1_after_android_start_android_service.svg)

### 有待研究的问题

1. Linux 与 Android 共有的操作有哪些，以至于不用修改Linux的程序就能适配与Android程序的通信。比如：打开浏览器？

2. 设计一种中间层拦截判断通信请求的目的地，Android程序还是Linux程序。

3. 等。

## 4 am 命令启动Service的过程研究

发现Android里面自带一个am命令可以启动Activity、Service等，研究它的实现：

![Alt text](https://cdn.rawgit.com/openthos/research-analysis/master/projects/and-linux/image/am.svg)

# 2017.03.08~2017.03.15

## 1 本周目标：

1. 了解其他两种思路：

有人在Linux上运行Android程序，陈莉君老师给过的Shashlik项目资料

Google在Chrome上运行Android程序，它的做法

2. 对于我已有的调研工作：在Linux上调用Android Service，可以尝试一下，做实验。

## 2 研究过程：
 
### 了解其他两种思路

思路二：

陈老师给过的资料 Shashlik项目

https://www.maketecheasier.com/run-android-apps-linux/

这里面介绍了，这个项目运行Android程序的原理是利用Android SDK里的Android模拟器。

但是它号称没有用虚拟机？

在我看来，它只是做了一下包装，能够自动安装APK，创建桌面快捷方式。

思路三：

用Chrome/Chrome OS运行Android应用，叫： Android Runtime for Chrome（ARC）

以前有个 ARC Welder 插件可以直接在Chrome市场里下载，但是现在搜不到了。

参考：http://www.iplaysoft.com/arc-welder.html

发现直接输入 https://chrome.google.com/webstore/detail/arc-welder/emfinbmielocnlhgmfkkmkngdoccbadn 可以安装

安装 ARC Welder 好之后不能用，加载不上apk。在chrome://plugins开启Native Client支持也不行。

参考：http://eyehere.net/2015/use-arc-welder/ 但是以前是可以自动下载runtime的。

安装ARChon插件： https://github.com/vladikoff/chromeos-apk

安装好之后还是不行，加载apk一直转圈。

可能我用Chrome版本太新了，是 55.0.2883.87 m (64-bit)，因为以前用过，没问题的。

使用其他方法运行，慢复杂的，参考百度经验：http://jingyan.baidu.com/article/f79b7cb379d82c9145023e61.html

安装nodejs 

转换apk

加载出错，提示：There is no "message" element for key extName.

参考：http://www.playubuntu.cn/article/223.html

将转换后的应用添加到开发者插件

今日头条 运行失败。。。

网易云音乐 失败。。。

还是按照百度经验来试试，安装 twerk 插件

用twerk转换

还是运行失败

可能是 ARChon 太老了，在市场上下载新的Beta版

使用新版的 ARChon 还是运行不了。暂时不再尝试了，以前也试过，有些了解。

分析一下 ARChon 插件的原理

找不到相关的分析资料，名称上的意思是Android运行环境。应该是搭建了一套安卓程序解释器，并且自己实现了Android的API，从而运行Android程序。

这个项目的核心功能在 ARChon 插件的_platform_specific\nacl_x86_64目录，都是编译成so文件，闭源。

比如：dalvikvm.so     libsqlite_jni.so     libwebviewchromium.so

这里面还有一个精简的系统镜像readonly_fs_image.img

应该就是自己实现了接口，实现了二进制兼容。

这种方式工作量太大，每个接口都要适配，但是这种native实现，性能很好。

### 实验研究



#### 1 在Linux中运行Service

尝试在Linux运行之前编写的Service：

自己写个类，加载Service，在这个Service里面发送一个Intent。

报错：Error: Could not find or load main class

类是在的，加载出错。

这个和Intent没关系，加载Service就是出错。

发现是android.jar的问题，只要加载这个android.jar就有问题。哪怕代码里没有与之相关的东西。

发现android.jar包里有java的类在里面。可能造成与rt.jar冲突。

java参数 http://www.cnblogs.com/ilife/archive/2012/08/01/2618617.html

-Xbootclasspath:android.jar

出错

用javac -Xbootclasspath:android.jar TestS.java 重新编译

还是相同错误。

大概明白了，这是因为依赖的class不是一个编译器编译出来的，我用的android.jar是Google提供的。

如果使用C/C++ 编写Service，像 https://github.com/hungys/binder-for-linux 项目一样，是不是更靠近底层

但是这里的Service不是APP的Service，这里的是系统服务（Android Native Service）。如果是

无法使用C/C++发送Intent，必须在JAVA层发送
http://stackoverflow.com/questions/9990830/sending-intents-from-an-android-ndk-application

Android NDK 里有个ndk-bundle\sysroot\usr\include\android\native_activity.h

说明NDK里可以连接ActivityManager服务，但是NDK里没有任何有关Intent的头文件，说明不能在C/C++上直接发送Intent
很可能所有的操作还是通过JAVA层的Binder连接的。

#### 2 在Linux上调用Android Service

想搞清楚在JAVA层发送Intent最终的数据读写代码在哪。

探究APP中JAVA层的最终Binder发送是否依赖非JAVA层的本地库，还是直接能够调用read、write进行操作。

换个思路，由于这个Intent发送过程肯定不涉及IPC，所以一定是在这个进程内部完成的，但是可能不是在JAVA层

在startService过程中，APP端最终追踪到

mRemote.transact(START_SERVICE_TRANSACTION, data, reply, 0);

mRemote 是 interface IBinder

直接追查不了了

参考：http://www.cnblogs.com/bastard/archive/2012/05/25/2517522.html

在类 android.os.Binder

```
public final boolean transact(int code, Parcel data, Parcel reply,
  int flags) throws RemoteException {
...
boolean r = onTransact(code, data, reply, flags);
...
}
```

看这个onTransact没用，这里会被子类覆盖。

在startService()中的transact()最终是到ActivityManagerService里的startService()里

但是博客里面分析，说ActivityManagerService是在一个独立的进程里。
AMS是作为管理Android系统组件的核心服务，他在SystemServer执行run()方法的时候被创建，并运行在独立的进程中。具体来说就是SystemServer管理着Android中所有的系统服务，这些系统服务的生命周期回调都由SystemServer去调度负责。

所以这个startService是怎么跳过去的。。。。

回到 ActivityManagerNative 里的 mRemote.transact

public ActivityManagerProxy(IBinder remote)
{
  mRemote = remote;
}
这个remote到底是从哪来的，这个remote不可能是ActivityManagerService
因为不是在一个进程，是它的一个代理，但是这个代理在哪赋值的

最终的Intent发送操作肯定是由这个 remote 对象完成。

## 3 本周结果

1. 对于其他两种思路，Shashlik项目其实就是用了Android SDK里的虚拟机，Chrome下的 ARC 编写了一套API接口实现。

2. 实验方面，虽然知道了Intent的数据构成，但是在JAVA层最终如何发送到Binder设备文件还不清楚。现在想找到在JAVA层发送Intent最终的操作对象 mRemote 代码在哪，希望能够找到它，然后用它的代码在Linux上发送Intent数据。

## 4 下周计划

查找到JAVA层用于读写Binder对象的mRemote的代码。

# 2017.03.03~2017.03.08

## 1 本周目标：
搞懂ActivityManagerService服务运行的详细过程，然后研究一个调用方案，实现在Linux中启动该Service，并且能够与Android中的ActivityManagerService服务相交互。

## 2 研究过程：

现在的短期思路是：

搞清楚Service启动时，应用需要通过Intent发送哪些数据给系统，系统才能找到Service并启动。

题外话：想到一种更简易的修改方式，借鉴插件化开发的思想，使用代理Activity等形式，达到间接与Linux上的程序交互。

参考：http://gityuan.com/2016/03/06/start-service/

启动初始化重点在ActivityThread.java 里的 15. AT.handleCreateService 这里面loadClass，然后创建了context和application，调用service.onCreate() 

现在研究，发送一个启动Service的Intent需要哪些数据，并把这些数据通过Binder发送给ActivityManagerService。

分析这过程中包含的进程和对象。

|整个过程参与的进程|作用|
| ------------- |------------- |
|Process A进程                |    发送Intent的进程
|system_server进程            |   ActivityManagerService服务所在进程
|Zygote进程                   |      创建新进程的进程

比如Process A进程 里的Activity对象执行startService()方法，Activity继承了ContextWrapper类，在ContextWrapper类中，有一个成员变量mBase，它是一个ContextImpl实例。ContextWrapper类的startService函数最终过调用ContextImpl类的startService函数来实现。

即 Process A进程 执行startService()方法

Activity extends ContextWrapper

执行 startService() -> ContextImpl里的startService()

在ContextImpl类的startService类，最终又调用了ActivityManagerNative里的ActivityManagerProxy类的startService来实现启动服务的操作。

abstract class ActivityManagerNative extends Binder implements IActivityManager

ActivityManagerProxy 是 ActivityManagerNative 的内部类

class ActivityManagerProxy implements IActivityManager
``` java
public ComponentName startService(IApplicationThread caller, Intent service,
        String resolvedType, String callingPackage, int userId) throws RemoteException
{
    Parcel data = Parcel.obtain();
    Parcel reply = Parcel.obtain();
    data.writeInterfaceToken(IActivityManager.descriptor);
    data.writeStrongBinder(caller != null ? caller.asBinder() : null);
    service.writeToParcel(data, 0);
    data.writeString(resolvedType);
    data.writeString(callingPackage);
    data.writeInt(userId);
    mRemote.transact(START_SERVICE_TRANSACTION, data, reply, 0);
    reply.readException();
    ComponentName res = ComponentName.readFromParcel(reply);
    data.recycle();
    reply.recycle();
    return res;
}
```

可以看到data存储了以下内容

|变量|内容作用|
| ------------- |------------- |
|IActivityManager.descriptor    | String descriptor = "android.app.IActivityManager";
|IApplicationThread caller| 辅助？
|Intent service                 | 里面指定了要启动的服务的名称
|String resolvedType           | 表示service这个Intent的MIME类型，它是在解析Intent时用到的
|String callingPackage| 调用者的包名
|int userId   | 调用者的用户ID

action 标识为 `START_SERVICE_TRANSACTION`

ActivityManagerProxy类的startService函数把这三个参数写入到data本地变量去，接着通过mRemote.transact函数进入到Binder驱动程序，然后Binder驱动程序唤醒正在等待Client请求的ActivityManagerService进程，最后进入到ActivityManagerService的startService函数中。

然后进入之前看到的20步的 ActivityManagerService的startService函数的处理流程

在 startServiceLocked 里 通过 retrieveServiceLocked 解析intent里需要的Service

retrieveServiceLocked : 通过intent 和PackageManagerService 获得ServiceRecord

参考 http://3dobe.com/archives/30/

ServiceRecord，我们可以称之服务记录，也可以叫服务描述符，每一个运行中的服务都会在 AMS 的 HashMap<ComponentName, ServiceRecord> mServices 字段中存储一份自己的 ServiceRecord，该类记录了一个 Service 的状态信息。

查找源有二：AMS 中的 mServices（正在运行中的服务）和 PMS 中的 mServices（已经安装服务的解析类）

对于Linux上的程序启动Android上的Service这种情况，我们暂时不考虑Service的注册问题。我们可以模拟Android上的程序将IActivityManager.descriptor、caller等五个信息通过Binder发送给AMS。并通过将userID设置为0之类的手段，暂时屏蔽掉AMS的调用者权限检测，应该能够成功实现调用。

但是对于在Linux上运行Service这种情况，首先需要在PMS里注册Service。在Android里注册后，启动Service时，ActivityManagerService会调用Zogote进程创建新进程。

但是，Linux中的程序应该是自主运行的，运行的进程不受Android上的ActivityManagerService控制。

应该如何修改ActivityManagerService机制？


## 3 本周结果：

通过 ActivityManagerService 服务发送启动Service的Intent、并启动Service的部分已经看完。

对于情景： **Linux上的程序启动Android上的Service** 已经比较清楚。

这种情景，我们暂时不需要考虑Service的注册问题。

我们可以模拟Android上的程序将IActivityManager.descriptor、caller等五个信息通过Binder发送给AMS。并通过将userID设置为0之类的手段，暂时屏蔽掉AMS的调用者权限检测，应该能够成功实现调用。

对于情景：**Android上的APP调用Linux上运行Service** 不太清楚。

这种情况，首先需要在 PackageManagerService 里注册该 Service 。在Android里注册后，启动Service时，ActivityManagerService会调用Zogote进程创建新进程。但是，Linux中的程序应该是自主运行的，运行的进程不受Android上的ActivityManagerService控制。

如果是这样，如何修改ActivityManagerService的机制，来实现Linux上的Service自主启动，不使用Zogote进程，并连接上ActivityManagerService。

## 4 下载计划：

听取老师的建议，先了解更多Linux与Android相互调用的思路，别局限在一条路上。

# 2017.02.25~2017.03.02

## 1 本周目标：

上周与陈渝老师进行远程会议后，定下本周计划是做一个简单的例子，如下：

尝试在Linux中运行一个简单的Service（如：只有简单的计算功能），然后在Android中的APP可以调用该Service。

第一步：了解 Binder 如何启动新的Service

第二步：了解如何在 Binder 中注册新的Service

第三步：移植相关代码测试

如果这个例子不能够简单的完成，则说明本课题不是我想象中的那么简单，是有研究价值的。

## 2 研究过程：

通过几天的努力，我现在能够在Linux上编译Android中的Service类，但是该Service并不能够运行。

由于我现在还没有完全弄清楚Android中的APP启动机制，所以先说一说已经研究的部分。

参考罗升阳的博客： Android系统在新进程中启动自定义服务过程（startService）的原理分析

http://blog.csdn.net/luoshengyang/article/details/6677029

将ActivityManagerService的startService函数的处理流程记录下，共20步。如果自己找的话，中间很多是通过父类调用子类方法、Socket、Binder通信等方式，无法直接找出下一步跳到哪，所以罗升阳的这篇博客有很大阅读价值。
```
Step 1. ActivityManagerService.startService
Step 2. ActivityManagerService.startServiceLocked
Step 3. ActivityManagerService.bringUpServiceLocked
Step 4. ActivityManagerService.startProcessLocked
Step 5. Process.start
Step 6. ActivityThread.main
Step 7. ActivityThread.attach
Step 8. ActivityManagerProxy.attachApplication
Step 9. ActivityManagerService.attachApplication
Step 10. ActivityManagerService.attachApplicationLocked
Step 11. ActivityManagerService.realStartServiceLocked
Step 12. ApplicationThreadProxy.scheduleCreateService
Step 13. ApplicationThread.scheduleCreateService
Step 14. ActivityThread.queueOrSendMessage
Step 15. H.sendMessage
Step 16. H.handleMessage
Step 17. ActivityThread.handleCreateService
Step 18. ClassLoader.loadClass
Step 19. Obtain Service
Step 20. Service.onCreate
```
这样，Android系统在新进程中启动服务的过程就分析完成了，虽然很复杂，但是条理很清晰。它通过三次Binder进程间通信完成了服务的启动过程，分别是：

  一. Step 1至Step 7，从主进程调用到ActivityManagerService进程中，完成新进程的创建；
  
  二. Step 8至Step 11，从新进程调用到ActivityManagerService进程中，获取要在新进程启动的服务的相关信息；
  
  三. Step 12至Step 20，从ActivityManagerService进程又回到新进程中，最终将服务启动起来。

参考

以Binder视角来看Service启动 http://blog.csdn.net/omnispace/article/details/52732442

startService启动过程分析 http://gityuan.com/2016/03/06/start-service/

![调用图](http://ww3.sinaimg.cn/large/0060lm7Tgy1fd8urgqdx8j30j9054aae.jpg)

1 - ActivityManagerService通过Socket通信方式向Zygote进程请求生成(fork)用于承载服务的进程ActivityThread。此处讲述启动远程服务的过程，即服务运行于单独的进程中，对于运行本地服务则不需要启动服务的过程。ActivityThread是应用程序的主线程；

2 - Zygote通过fork的方法，将zygote进程复制生成新的进程，并将ActivityThread相关的资源加载到新进程；

3 - ActivityManagerService向新生成的ActivityThread进程，通过Binder方式发送生成服务的请求；

4 - ActivityThread启动运行服务，这便于服务启动的简易过程，真正流程远比这服务复杂；

我自己再查看 ActivityManagerService.java 源码

在Step 4  startProcessLocked中
```
Process.ProcessStartResult startResult = Process.start(entryPoint,
                    app.processName, uid, uid, gids, debugFlags, mountExternal,
                    app.info.targetSdkVersion, app.info.seinfo, requiredAbi, instructionSet,
                    app.info.dataDir, entryPointArgs);
```
进入Step 5 Process.start()
```
return startViaZygote(processClass, niceName, uid, gid, gids,
  debugFlags, mountExternal, targetSdkVersion, seInfo,
  abi, instructionSet, appDataDir, zygoteArgs);
```
进入 startViaZygote()
return zygoteSendArgsAndGetResult(openZygoteSocketIfNeeded(abi), argsForZygote);

可以看到，程序通过 zygoteState.writer 将命令写入Socket

另外查找源码看到 public static ZygoteState connect(String socketAddress) throws IOException {

可以看到在connect里创建了socket连接

另外，通过查资料看到，这个Socket就是 /dev/socket/zygote

后面的暂时不用不看了，已经大致过了一遍Service的启动流程。

## 3 本周结果：

通过发现上图 1 Socket 过程，看到ActivityManagerService启动Service是通过Socket的方式连接Zygote进程，让它来fork出新的进程，然后ClassLoader.loadClass，之后ActivityManagerService通过Binder与新进程交互，完成启动。
所以Service的运行并不是像我之前想象的一样：是一个进程fork之后，自己通过Binder连接系统服务完成初始化。Service的整个初始化过程受到Zygote控制，它并没有一个main函数主动执行所有逻辑，全是被调用。
我之前完全没有意识到这个概念，太天真了。并且Android系统中的程序在ART虚拟机中运行，这就造成谁来启动Service的问题：

1. Android中的Service在ART虚拟机中运行，而我在Linux中不能这样干，因为我要和Linux中的程序结合，必然要在Linux中启动，比如：Linux中的JAVA程序在JVM中运行。

2. 需要一个服务程序主动调用Service中的函数，完成Service的生命周期。

所以现在将android.jar（APP层依赖库）复制过来，在Linux中编译程序

javac -Djava.ext.dirs=. com/example/bboxh/testipcapplication/MyService.java

虽然能够编译，但是没有程序能够调用。。。

## 4 下周计划：

搞懂ActivityManagerService服务运行的详细过程，然后研究一个调用方案，实现在Linux中启动该Service，并且能够与Android中的ActivityManagerService服务相交互。

目前想到这里面有一些细节有待解决：

1. Linux中的Service的注册问题

2. Linux中的Service的生命周期同步问题
