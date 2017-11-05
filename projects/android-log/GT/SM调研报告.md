# SM调研报告
## 1 背景知识
### 1.1 Android 的图像渲染流程特征
![Android图像渲染流程](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/Android%E5%9B%BE%E5%83%8F%E6%B8%B2%E6%9F%93%E6%B5%81%E7%A8%8B.png)

1. Android 图像渲染架构分为应用（Surface）、系统（SurfaceFlinger）、硬件（Screen）三个层级，其中绘制在应用层，合成及提交上屏在系统层，显示在硬件层；

1. 无论应用（Surface）、系统（SurfaceFlinger）、硬件（Screen）都是当且仅当绘制内容发生改变，才会对绘制内容进行处理；

1. 系统中的 SurfaceFlinger 以及绝大部分 Surface 都是按照 VSYNC 信号的节奏来安排自己的任务；

1. 目前，绝大部分 Surface 都属于 Hardware Rendering。

###　1.2 VSYNC机制下的绘制过程
VSync（Vertical Synchronization，垂直同步），可以简单的把它认为是一种定时中断。	CPU和GPU的处理时间都少于一个VSync的间隔，即16.6ms，每个间隔都有绘制的情况下，当前的FPS即为60帧，如下图所示。

![VSYNC机制下的绘制过程](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/VSync.png)

双Buffer机制的情况下，当CPU和GPU处理时间都很慢，或因为其他的原因，如在主线程中干活太多，使得CPU和GPU的处理时间大于一个VSync的间隔（16.6ms）时，第二个VSync还在处理A区域的绘制，不可能实现理论上的60FPS，同时也出现了丢帧(SF: Skipped Frame)情况。

![双BufferVSYNC机制](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/Jank.png)

Android 4.1引入了Triple Buffer，所以当双Buffer不够用时，Triple Buffer丢帧的情况如下图所示。

![三BufferVSYNC机制](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/Jank3.png)

简单来说，VSync机制就像是一台转速固定的发动机(60转/s)。每一转会带动着去做一些UI相关的事情，但不是每一转都会有工作去做(就像有时在空挡，有时在D档)。有时候因为各种阻力某一圈工作量比较重超过了16.6ms，那么这台发动机这秒内就不是60转了，当然也有可能被其他因素影响，比如给油不足(主线程里干的活太多)等等，就会出现转速降低的状况。我们把这个转速叫做流畅度。

### 1.3 SurfaceFlinger、HWComposer与Surface的关系
1. **Surface**：基本显示单元。Android任意一种API绘图的结果都将反映在Surface上。

1. **SurfaceFlinger**：运行在System进程中，用来统一管理系统的帧缓冲区设备，其主要作用是使用GPU将系统中的大部分Surface进行合成，合成的结果将形成一个FrameBuffer。

1. **HWComposer**：即Hardware Composer HAL，将SurfaceFlinger通过GPU合成的结果与其他Surface（不由WindowManager管理）一起最终形成BufferQueue中的一个Buffer。HWComposer还可以协助SurfaceFlinger进行Surface的合成，但是否进行协助是由HWComposer决定的。

**注意**：有的Surface不由WindowManager管理，将直接作为HWComposer的输入之一与SurfaceFlinger的输出做最后的合成。
### 1.4 Choreographer、SurfaceFlinger、HWComposer与VSYNC的关系

1. **VSYNC**：作用是使GPU的渲染频率与显示器的刷新频率（一般为固定值）同步从而避免出现画面撕裂的现象。

1. **Choreographer**：当收到VSYNC信号时，Choreographer将按优先级高低依次去调用使用者通过postCallback提前设置的回调函数，它们优先级从高到低是：CALLBACK_INPUT、CALLBACK_ANIMATION、CALLBACK_TRAVERSAL。

1. **SurfaceFlinger**：Surface的合成操作也是基于VSYNC信号进行的。

1. **HWComposer**：通过硬件触发VSYNC信号。

## 2. 为什么用SM作为衡量流畅度的指标
在很多Android的App中，很少有需要不断地去绘制的场景，很多时候页面都是静态的。也就是说1s中VSync的60个Loop不是每个都在做绘制的工作，FPS会比较低，但并不代表这个时候程序不流畅(如我将App放着不动，实测FPS为1)。所以FPS较低并不能代表当前App在UI上界面不流畅，而1s内VSync这个Loop运行了多少次更加能说明当前App的流畅程度。所以，下面这2个指标比FPS更能代表当前的App是否处于流畅的状态。同样这2个指标更加能够量化App卡顿的程度：

**丢帧(SF: Skipped Frame)**：应该在16.6ms完成工作却因各种原因没做完，占了后n个16.6ms的时间，相当于丢了n帧。

**流畅度(SM: SMoothness)**：在VSync机制中1s内Loop运行的次数。描述的是应用绘制轮询的频率
## ３. 如何得到SM
### ３.1初始思想
每次Loop运行之前记个数就可以得到SM。
### ３.2 Choreographer
Android机制中有一个Choreographer对象。它是用来协调animations、input以及drawing时序的，并且每个Loop共用一个Choreographer对象。下图为Choreographer的定义和结构

![Choreographer对象](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/Choreographer.png)

Choreographer 的工作机制：

1. 使用者首先通过 postCallback 在 Choreographer 中设置的自己回调函数：
  * CALLBACK_INPUT：优先级最高，和输入事件处理有关。
  * CALLBACK_ANIMATION：优先级其次，和Animation的处理有关。
  * CALLBACK_TRAVERSAL：优先级最低，和UI等控件绘制有关。
1. 当 Choreographer 接收到 VSYNC 信号时，Choreographer 会调用 doFrame 函数依次对上述接口进行回调，从而进行渲染。doFrame 的执行效率（次数、频率）也就是我们需要的显示性能数据。

![doFrame 函数](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/doFame.png)

其中 skippedFrames 记录了 jitterNanos 这段时间 doFrame 错过了多少个 VSYNC 信号，即跳过了多少帧。

由于对于绝大多数应用在没有丢帧的情况下会针对每一次 VSYNC 信号执行一次 doFrame（），而 VSYNC 绝大多数情况下每秒会触发 60 次，因此获取了skippedFrames这个参数我们可以反向计算得出 SM 的数值：

![SM](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/SM.png)

但是skippedFrames的获取并不是那么的直接，Choreographer 源码中本身就有输出的方案：

![lOG](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/skippedFramesLog.png)

唯一阻碍我们获取数值的是：skippedFrames 的数值只有大于 SKIPPED_FRAME_WARNING_LIMIT 才会输出相关的警告。而 SKIPPED_FRAME_WARNING_LIMIT 的数值可以由系统参数 debug.choreographer.skipwarning 来设定。在初始条件下，系统中不存在 debug.choreographer.skipwarning 参数，SKIPPED_FRAME_WARNING_LIMIT 将取默认值 30。因此，正常情况下，我们能够看见上诉 Log 出现的机会极少。

可行的方法是修改（设定）系统属性 debug.choreographer.skipwarning 为 1，Logcat 中将打印出每一次丢帧的Log。需要说明的是，由于为 SKIPPED_FRAME_WARNING_LIMIT 赋值的代码段由 Zygote 在系统启动阶段加载，而其他应用都是在拷贝复用 Zygote 中的设定，因此设定系统属性后需要重启 Zygote 才能使得上述设定生效。具体的设置方法如下：

![ADDlOG](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/Zygote.png)

设定完成以后，我们可以直接通过 Logcat 中的信息得到系统中所有应用的绘制丢帧信息，包括丢帧发生的时间以及连续丢帧的数量。从而我们就可以获取SM值。

## 4.SM存在的优缺点
### 4.1优点

可以获取系统中所有应用各自的绘制丢帧情况（丢帧发生的时间以及连续丢帧的数量）。

### 4.2缺点

1. 需要系统授权 “Adb Root” 权限，用于修改系统属性

1. 由于 Logcat 信息的滞后性，只能在测试完成后对于丢帧信息进行统计分析，而无法进行实时处理。

1. 由于其基础数据取自 Choreographer，若某些 Surface 的绘制不依赖于 Choreographer ，则这些指标无法衡量该 Surface 的显示性能。

## 5. GT是如何实现SM插件的
### 5.1流畅度模块的代码结构

流畅度插件核心思想：通过Choreographer输出的log信息获取跳帧数据。

**SMActivity.java**：插件的入口类，通过预设环境来实现log打印操作

**SMLogService.java**：过滤出当前进程的丢帧值

**SMServiceHelper.java**：来进行数据处理。流畅度值为60减去1s内的跳帧数。

### 5.2 简要流程
1. 执行setprop debug.choreographer.skipwarning 1

1. 执行getprop debug.choreographer.skipwarning判断，为1则可以进行测试

1. 执行adb logcat -v time -s Choreographer:I *:S

1. 过滤获取当前pid丢帧值

1. 数据处理得到sm值

## 5.3 代码流程
１、SMActivity.java：执行setprop debug.choreographer.skipwarning 1

![write](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/WRITE.png)

2、SMActivity.java：执行getprop debug.choreographer.skipwarning判断，为1则可以进行测试

![check](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/CHECK.png)

3、SMLogService.java：执行adb logcat -v time -s Choreographer:I *:S并且过滤获取当前pid丢帧值

![printlog](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/LOG.png)

４、 SMServiceHelper.java、SMDataService.java数据处理得到sm值

![SM1](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/DATA1.png)

![SM2](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/images/DATA2.png)

**参考文献：**

[GT源码下载](https://github.com/TencentOpen/GT)

[GT流畅度测试](https://testerhome.com/topics/4770)

[当我们讨论流畅度的时候，我们究竟在说什么？](http://blog.csdn.net/xiaosongluo/article/details/51212296)

[如何量化Android应用的“卡”？---流畅度原理&定义篇](http://mp.weixin.qq.com/s?__biz=MzA3NTYzODYzMg==&mid=208258190&idx=2&sn=22af4f01a6090599da3dca4c44f0f396&scene=2&from=timeline&isappinstalled=0#rd)

[如何准确评测Android应用的流畅度？ ](http://mp.weixin.qq.com/s?__biz=MzA3NTYzODYzMg==&mid=209682379&idx=1&sn=d43adbdc22235450e9de0ae7fbd46ff0&scene=2&from=timeline&isappinstalled=0#rd)

[GT开篇文——从快速评估Android应用的流畅度说起 ](http://mp.weixin.qq.com/s?__biz=MzA5ODI1NzczNg==&mid=207394534&idx=1&sn=71f93ebf0feb55880ddb641918049344&scene=5#rd)

[优化安卓应用内存的神秘方法以及背后的原理，一般人我不告诉他 ](http://mp.weixin.qq.com/s?__biz=MzA3NTYzODYzMg==&mid=212495002&idx=1&sn=711b7c4ea863e77972f6b1be943a4133&scene=5&srcid=MJXfT5YQ6EbPada4covs#rd)

[GT流畅度测试-Choreographer](www.350351.com/plus/view.php?aid=460704)
