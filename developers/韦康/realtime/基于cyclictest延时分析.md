#通过cyclictest分析延时
##说明
我做了这样一个实验，利用cyclictest循环做测试，这个时候打开了ftrace中function_graph追踪器，并且设定了追踪的id，此时产生了关于cyclictest的一系列追踪数据。从这些数据如何分析出cyclictest那些延迟很大的点产生的原因（ftrace的开启会对延迟造成很大的影响，但影响是对每次测量都存在的，因此那些偏离了平均水平很大的点仍然有值得研究的意义。关于cyclictest测延时，简单的来说就是利用定时器睡眠，唤醒时的实际时间与理论时间相见即为延迟。  
##实验基本步骤
1.获取cyclictest(安装rt-tests)套件
```
apt-get install rt-tests
```
2.运行cyclictest
```
sudo cyclictest
```
这个时候不出意外，cyclictest会一直运行，大致的效果如下：
```
root@thu-Lenovo-IdeaPad-Y580:/home/thu# cyclictest
# /dev/cpu_dma_latency set to 0us
policy: other/other: loadavg: 0.97 1.02 1.18 4/545 3576           
T: 0 ( 3566) P: 0 I:1000 C:   9751 Min:     11 Act:   16 Avg:   13 Max:     216
```
如果不是这样子的话，关了重来，多试几次总会出现的。。。  
3.获取pid
```
ps -all
```
找到cyclictest此时运行的pid,这个pid在后面我们追踪某个进程的时候会用到  
4.设置追踪器并进行追踪
```
cd /sys/kernel/debug/tracing
echo function_graph > current_tracer
echo pid > set_ftrace_pid 
echo 1 > tracing_on 
```
若干分钟之后,就可以查看trace数据了
```
echo 0 > tracing_on
vim trace
```
大致这样，等一会就会产生一大堆的trace信息，这里的trace信息可能不包含最坏的点，但是延时总是有不同的，在trace信息应该也有差异。  
##遇到的问题
1.由于没有对function进行过滤，所以函数多到看不过来，在这种情况下给分析带来了很大的困难，仅仅一次测量就有上万的函数，基本上无法分析。  
2.如果全部函数都追踪不可行，我们选择一些函数去追踪，那我们该选择那些函数呢？如果选择的不够好，会不会造成每次信息类似？  
3.想分析linux为什么有时候会产生较大的延时，采用这种思路正确吗？
##实验数据
恩，这里提供了一些trace的数据，大致就一分钟不到的数据（至于里面执行了多少次测试，可以通过统计SyS_nanosleep次数大致的预估）。  
[cyclictest_trace.log
](https://github.com/openthos/research-analysis/blob/master/developers/%E9%9F%A6%E5%BA%B7/realtime/cyclictest_trace.log)
