`#!/usr/bin/env python  `

_指出这个文件中的代码用什么可执行程序去运行它,当系统看到这一行的时候，首先会到env设置里查找python的安装路径，再调用对应路径下的解释器程序完成操作。_

`import sys`

_利用import语句输入sys模块,sys模块包含了与Python解释器和它的环境有关的函数。_

`import os`

os 模块提供了一个统一的操作系统接口函数, 这些接口函数通常是平台指定的,os 模块能在不同操作系统平台如 nt 或 posix中的特定函数间自动切换,从而能实现跨平台操作

`try:`

	`import ujson as json`

`except:`

	`import json`

_导入ujson作为json，如果出现异常就导入json_

`''' Split user space traces into monotonic increasing chunk and merge again based on time'''`

_将用户空间跟踪分解为单调递增块，并基于时间重新合并_

`def clock_backward(event, thread_latest):`

`#Checks whether the timestamp is smaller than any previous event for the same pid`

_检查当前事件的时间戳是否小于之前同一PID的所有事件_

	`cur_pid = event['pid']`

        _利用字典获取当前事件的pid_

	`cur_timestamp = event['time']`

        _利用字典获取当前事件的时间戳_

	`if(cur_pid in thread_latest):`

         _如果在thread_latest里存在相同时间戳的事件_

		`return thread_latest[cur_pid] > cur_timestamp`

                 _如果小于，则返回true，否则返回false_                    _ ？？？？？？thread_latest是什么？？？？？？_

	`return False	`


`print "Split: " + sys.argv[1]`                                      _ ？？？？？？sys.argv[1]应该传入什么？？？？？？_

_打印“Split:XXXXXXXXXXXX”,XXXXX为sys.argv[1]_

`thread_latest = {}`

_定义一个空的字典thread_latest_

`prev_timestamp = 0`

_设置之前的时间戳是0_

`count = 0`

`input_filename_split = sys.argv[1].split("/")`

_将sys.argv[1]根据/进行拆分，保存到input_filename_split中，当sys.argv[1]为/home/ll/document/user/log时_


`input_file_depth = len(input_filename_split)`

_计算input_filename_split的长度，保存到input_file_depth中，为6_

`#print sys.argv[1], "file depth:", input_file_depth`

`user_directory = input_filename_split[input_file_depth-2]`

_保存文件的上级目录到user_directory中，为user_

`user_raw_file = input_filename_split[input_file_depth-1]`

_保存文件名到user_raw_file中，为log_

`if not os.path.exists(user_directory):`
	`os.mkdir(user_directory)`

_如果系统不存在user_directory，则创建目录user_directory，即创建user_

`output_filename = user_directory +"/"+ user_raw_file`

_将输出文件名设置为user_directory/user_raw_file，即user/log_

`output_file = open(output_filename + "_"+str(count)+".split", "w")`

_以w的形式获取output_file，即user/log_0.split_

`print "input file:" , sys.argv[1], "output file:", output_filename`

_打印input file:/home/ll/document/user/logoutput file:user/log_

`input_file = open(sys.argv[1], "r")`

_以读的方式打开/home/ll/document/user/log_

```
for line in input_file:
#	print line
	event = json.loads(line)
	cur_timestamp = event['time']
	cur_pid = event['pid']
	if(cur_timestamp < prev_timestamp):# Both clock backwards and another new application could trigger this
		if(clock_backward(event, thread_latest)): # triggered by clock backwards
			print "Clock is backward for " + sys.argv[1] + " cur: ", cur_timestamp, "prev: ", prev_timestamp
			exit() # Temprorarily comment out for testing purpose
		output_file.flush()
		output_file.close()
		count += 1
		output_file = open(output_filename + "_"+str(count)+".split", "w")
	output_file.write(line)
	thread_latest[cur_pid] = cur_timestamp
	prev_timestamp = cur_timestamp

output_file.flush()
output_file.close()
```
