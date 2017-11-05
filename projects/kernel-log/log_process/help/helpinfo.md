#帮助信息
##1.挂载debugfs
ftrace 在内核态工作，用户通过 debugfs 接口来控制和使用 ftrace ，要使用debugfs 接口必须先挂载debugfs
```
mount -t debugfs nodev /sys/kernel/debug
```
##2.在创建traceLog目录
* 将openSchedEvents.sh,closeSchedEvents.sh,logProcess2.py,plot.py拷贝到该目录下
* 给这4个文件添加可执行权限
```
chmod a+x *.sh
chmod a+x *.py
```
##3.在traceLog目录下创建bugEmu目录
将模拟bug的代码存放在该目录下,例如将如下代码保存到sleep_bug.c，放在traceLog/bugEmu下
```
#include<stdio.h>
#include<unistd.h>
int main(){
 printf("program start...");
 sleep(10); 
 printf("program end...");
 return 0;
}
```
* 编译C程序
```
gcc sleep_bug.c -o sleep_bug
```
##4.打开ftrace中events/sched事件追踪器
```
root@thu-Lenovo-IdeaPad-Y580:/home/thu/traceLog# source openSchedEvents.sh 
```
##５.运行测试程序
```
root@thu-Lenovo-IdeaPad-Y580:/home/thu/traceLog/bugEmu# ./sleep_bug
```
##６.等待程序结束后关闭追踪器并且保存记录
```
root@thu-Lenovo-IdeaPad-Y580:/home/thu/traceLog#source closeSchedEvents.sh sleep_bug
该命令有一个脚本参数，为运行结束的程序名，这里为sleep_bug
在脚本中会将记录保存到/home/thu/traceLog目录下，sleep_bug.select_log为筛选sleep_bug进程后的记录
```

##7.处理log信息的脚本调用
```
root@thu-Lenovo-IdeaPad-Y580:/home/thu/traceLog# python logProcess2.py sleep_bug.select_log  0 10000000
该脚本的作用是统计某个特定进程的运行时间，睡眠时间，阻塞时间
logProcess.py 为python脚本名
sleep_bug.select_bug为需要分析记录的路径名称
0：为开始时间点
10000000：为结束时间点
```
