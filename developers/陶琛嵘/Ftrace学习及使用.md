# 对ftrace的调研及理解
ftrace由function trace而来，一开始功能单一，但是由于它的部分实现能够被其他的trace工具所用，因此ftrace逐渐成为一个trace的框架，具体来说这个框架有着四个部分：
+ A. 在函数的入口地址放置一个probe点，用于调用probe函数实现追踪的功能
+ B. 设置具体的probe函数，进行信息的获取
+ C. 将具体的log信息打印在ring buffer中
+ D. 用户通过debugfs访问ring buffer中的内容，从而得到追踪的log信息

![image](https://github.com/openthos/research-analysis/blob/master/developers/%E9%99%B6%E7%90%9B%E5%B5%98/ftrace%E6%A1%86%E6%9E%B6.jpg)

其中C、D部分是被其他追踪器经常使用的部分，因此我们可以看到ftrace中的那些工具无论如何进行追踪，我们读取log信息的方法都是一样的。
而对于ftrace中A、B部分如何实现，将ftrace中的工具分为了两类：
>Ftrace是一类trace的工具集合，包含function trace、schedule latency等tracer，另外还有着基于tracepoint的event tracing
 
以上的两类工具：tracer和event tracing，区别就在于A、B两个部分如何实现，即如何放置probe点以及如何调用具体的probe函数

## 1. tracer
其利用了gcc中的Mcount机制，解释如下：
>通过在编译和链接你的程序的时候（使用 -pg 编译和链接选项），gcc 在你应用程序的每个函数中都加入了一个名为mcount ( or "_mcount" , or "__mcount" , 依赖于编译器或操作系统)的函数，也就是说你的应用程序里的每一个函数都会调用mcount, 而mcount 会在内存中保存一张函数调用图，并通过函数调用堆栈的形式查找子函数和父函数的地址。这张调用图也保存了所有与函数相关的调用时间，调用次数等等的所有信息。

简单理解，这就是一种代码插装技术，在gcc中使用，在编译出的汇编代码中插入了具体的调用mcount的语句。  
tracer的实现正是利用了gcc的这项技术，平时的gcc编译时，mcount都是使用的libc中定义好的mcount，但是在编译内核代码的时候是不会链接到libc的，因此tracer选择自己实现具体的mcount函数，就可以在几乎所有的函数的开头处调用自己的mcount函数，从而实现追踪的目的。

现在的Linux发行版中的内核基本上编译时都带有了-pg选项，即都将具体的tracer编译了进去，从而在使用时不需要重新编译，平时tracer都设置为nop，在汇编代码中执行不产生任何结果，从而使用时不会因为mcount造成太多的资源消耗。而在使用时，会动态地将mcount替换为希望使用的追踪器实现的probe函数，达到追踪的功能。

## 2. event tracing
event tracing是基于tracepoint机制实现的，tracepoint比ftrace更早，而event tracing其实就是利用了tracepoint机制获取probe点以及注册probe函数，即A、B部分，之后通过ftrace中的C、D部分来进行log信息的记录以及用户的读取。   
tracepoint相比于gcc的mcount，在一开始定义函数的时候就需要将具体probe点放在函数中，即编写代码时就需要考虑是否要进行追踪，这里的probe点就是一个调用函数，其具体的逻辑会去检测是否注册了相对应的probe函数，注册了才会去调用进行信息的追踪以及写入到ringbuffer中。

可以自己定义自己想要的event tracing的事件追踪，即自己完成probe点以及probe函数的部分，需要在想要追踪的函数中加入probe点（tracepoint），另外自己实现probe函数（其中需要包括写入ringbuffer中的数据的格式等等）。内核中为了方便操作，也为了已有的event tracing中不要存在太多相似功能的代码，对于probe函数的注册、注销等代码采用了宏的方式，让宏自动展开成具有相似性的代码，这个宏就是```TRACE_EVENT```，在各个编译时要包含的头文件中会将对宏进行新的转化完成相应功能，从而方便自动展开。  
例如，位于include/tracepoint中的转化为：
```c
#define TRACE_EVENT(name, proto, args, struct, assign, print)  DECLARE_TRACE(name, PARAMS(proto), PARAMS(args))
```
这里用于生成注册和注销probe函数的代码，另外还生成了tracepoint处所要调用函数的代码（这里函数实现了查询probe函数是否注册，从而根据是否注册决定调用probe函数or继续执行代码的逻辑）。而位于include/trace/Define_trace.h文件中的转化为：
```
#undef TRACE_EVENT
#define TRACE_EVENT(name, proto, args, tstruct, assign, print)  DEFINE_TRACE(name)
```
即先对TRACE_EVENT进行undef，然后再重新进行定义，从而将TRACE_EVENT转换成了别的代码。
**TRACE_EVENT实际上就是event tracing的核心。**


#使用
### 编译阶段
**PS：实际上只要将debugfs挂载即可，不需要重新编译内核**

下载内核 4.4.52版本，解压，拷贝到/usr/src中，改名为linux-headers-4.4.52  
make menuconfig 出错，没有curses.h头文件，需要装ncurses-dev  
```sudo apt-get install ncurses-dev```  
配置选项，首先使用```make localmodconfig```  
```make menuconfig``` ，在load中将刚刚make localmodconfig生成的.config载入并查看是否需要添加支持，然后保存退出  
修改kernel/trace/Makefile，将```KBUILD_CFLAGS = $($(CC_FLAGS_FTRACE),,$(ORIG_CFLAGS)中的$CC_FLAGS_FTRACE```去掉，实际上就是保留ORIG_CFLAGS中的-pg选项，用于激活ftrace的支持

```make -j4```开始编译
编译完成，大小为4G

挂载debugfs文件系统，目录位于/sys/kernel/debug中  
当编译激活了ftrace，会在其中生成tracing目录，进入其中，里面是控制ftrace的一些选项


### 使用
ftrace是很多trace的集合，包含了function trace、schedule latency这些tracer，还有基于tracepoint的event tracing，而各种tracer与event tracing之间的使用方式也不同。

#### 1. tracer
```cd /sys/kernel/debug/tracing```
具体有哪些可用的tracer可以通过```cat ./available_tracers```看到

使用步骤：
+ 使用的时候需要将具体需要使用的tracer的名称填入到```./current_tracer```，从而选中具体的tracer
```shell-script
echo 具体的tracer名称 > ./current_tracer
```
+ 开启trace追踪
```shell-script
echo 1 > ./tracing_on
```
+ 清空```./trace```中上次追踪的log信息
```shell-script
echo 0 > ./trace
```
+ 执行想要追踪的程序
+ 关闭trace追踪
```shell-script
echo 0 > ./tracing_on
```
+ 将追踪结果读取出来，数据会被记录在log上
```shell-script
cat ./trace > log_info
```

#### 2.event tracing
使用步骤与tracer类似，不过将```./current_tracer```中的tracer名称改为nop，即不使用任何tracer
在```/sys/kernel/debug/tracing/events/```目录下有着许多event，其中可以选择自己想要追踪的进行开启，例如对于调度方面的追踪可以在```/sys/kernel/debug/tracing/events/sched/```目录下开启，操作语句为
```shell-script
echo 1 > ./events/sched/enable
```
之后进行与tracer中相同的操作步骤，即开启追踪后进行程序的执行，之后关闭，并通过```/sys/kernel/debug/tracing/trace```文件将log信息读取出来
