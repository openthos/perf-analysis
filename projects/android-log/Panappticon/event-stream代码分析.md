# event-stream代码分析
## 1、kernel log 解析
1. m

    * 编译event-decompressor.c minilzo/minilzo.c生成目标文件event-decompressor

    * 编译event-decoder.c生成目标文件event-decoder

1. event-read-sorted

    * 运行event-read，排序？？？

1. event-read

    * 依次运行event-decompressor、event-decoder、event-printer

1. 使用流程
    * ./m  警告不用去管它
    * cat ../EventLoggingServer/bin/5284047f4ffb4e04824a2fd1d1f0cd62/kernel/1505200252970778 | ./event-read-sorted

1. event-fork-extracter

    * 输入：标准输入，多个文件名
    * 如果写死为[‘/home/xhl/mygit/panappticon/tools/panappticon-tools/EventLoggingServer/bin/5284047f4ffb4e04824a2fd1d1f0cd62/kernel/1505200252970778.txt’]可以执行但没有输出
    
    * 输出：标准输出
    
    **测试代码**
      ```
      xhl@xhl-SMBIOS:~$ python
      >>> import sys
      >>> import subprocess
      >>> f = open('/home/xhl/mygit/panappticon/tools/panappticon-tools/
      EventLoggingServer/bin/5284047f4ffb4e04824a2fd1d1f0cd62/kernel/1505200252970778.txt', 'r')
      >>> a = ["egrep"]
      >>> args = ["FORK|THREAD_NAME"]
      >>> a.extend(args)
      >>> a
      ['egrep', 'FORK|THREAD_NAME']
      >>> p = subprocess.Popen(['egrep', 'FORK|THREAD_NAME'], stdin=f, stdout=subprocess.PIPE)
      >>> p.stdout
      <open file '<fdopen>', mode 'rb' at 0x7f880cbad540>  这是什么意思？？？为什么执行下一条语句后没有输出？？？？
      >>> sys.stdout.writelines(p.stdout)
      >>> 
      ```
      **问题：<open file '<fdopen>', mode 'rb' at 0x7f880cbad540>  这是什么意思？？？为什么执行下一条语句后没有输出？？？？**
      
     **测试代码**（用网站提供的数据可以运行）
     ```
     filenames = ['/home/xhl/2012-study/3c0e6a88c8c5f30f0d0ca1bf7412cab6/kernel/2012-10-31.json/2012-10-31.json']
     ```
     **结论：该文件提取的是整理好的json格式的kernel数据的FORK和THREAD_NAME记录**
    
1. event-merger-splitter(压缩文件为压缩包，与网站提供的数据打包方式一致，包括命名)

    * 输入：标准输入，多个文件名
    
    * 输出：通过path参数指定
    
1. event-timestamp-fixer
1. events.h
1. events.py
1. kernel_analysis.py
## 2、user log 解析
1. panappticon-tools/event-stream/user_space_traces/user_trace_process/parse.c

    * 解析user二进制文件

1. 使用流程
    * gcc -o parse parse.c    编译parse.c生成目标文件parse
    * cat ../../../EventLoggingServer/bin/5284047f4ffb4e04824a2fd1d1f0cd62/user/1505199593553371 | ./parse

## 3、关键路径构建
1. ComputeDependencies.py
```
import sys
import Event
from EventHandlerMap import event_handler_map
            from EventHandlers import *
from Global import Global
from EventReordering import ReorderEvents

cat ../EventLoggingServer/bin/5284047f4ffb4e04824a2fd1d1f0cd62/kernel/1505200252970778 | python kernel_analysis.py
ImportError: No module named numpy
首先python2.7：sudo apt-get install python-numpy

其次python3.4：sudo apt-get install python3-numpy

然后分别进入各版本的shell 测试import numpy是否成功。

ImportError: No module named matplotlib.pyplot


    sudo apt-get install python-matplotlib  

cat ../EventLoggingServer/bin/5284047f4ffb4e04824a2fd1d1f0cd62/kernel/1505200252970778 | ./event-read-sorted|./event-timestamp-fixer

```
