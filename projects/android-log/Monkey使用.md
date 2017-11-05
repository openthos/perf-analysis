## Monkey

### 什么是Monkey

 - Monkey测试是Android平台自动化测试的一种手段，通过Monkey程序模拟用户触摸屏幕、滑动Trackball、按键等操作来对设备上的程序进行压力测试，检测程序多久的时间会发生异常
 - Monkey程序由Android系统自带，使用Java语言写成，在Android文件系统中的存放路径是：/system/framework/monkey.jar
 - Monkey.jar程序是由一个名为“monkey”的Shell脚本来启动执行，shell脚本在Android文件系统中的存放路径是：/system/bin/monkey
### Monkey的特征

 - 测试的对象仅为应用程序包，有一定的局限性
 - Monky测试使用的事件流数据流是随机的，不能进行自定义
 - 可对Test的对象，事件数量，类型，频率等进行设置
 
## Monkey使用及参数说明

### Monkey使用示例

 - 启动Monkey：adb shell monkey [options] 
 - 测试示例：adb shell monkey --throttle 500  --ignore-crashes --ignore-timeouts --monitor-native-crashes -v 500 -p  com.kingsoft.email

### Monkey各参数解析

 - options：这个是配置monkey的设置,例如,指定启动那个包,不指定将会随机启动所有程序
 - -p：参数-p用于约束限制，用此参数指定一个或多个包
  + 指定一个包：adb shell monkey -p com.htc.Weather -v 100
  + 指定多个包：adb shell monkey -p com.htc.Weather –p com.htc.pdfreader  -p com.htc.photo.widgets -v -v -v 100
  + 不指定包：adb shell monkey 100 //Monkey随机启动APP并发送100个随机事件
 - -v：用于指定反馈信息级别（信息级别就是日志的详细程度），总共分3个级别，一个 -v 为较低级别，三个 -v 打印的信息最为全面
 - -s：用于指定伪随机数生成器的seed值，如果seed相同，则两次Monkey测试所产生的事件序列也相同的
  + 如果需要两次测试的事件是相同的，可以指定 -s 参数为特定值
 - --throttle <毫秒>：用于指定用户操作（即事件）间的时延，单位是毫秒
 - --ignore-crashes：用于指定当应用程序崩溃时（Force& Close错误），Monkey是否停止运行。如果使用此参数，即使应用程序崩溃，Monkey依然会发送事件
 - --ignore-timeouts：用于指定当应用程序发生ANR（Application No Responding）错误时，Monkey是否停止运行。如果使用此参数，即使应用程序发生ANR错误，Monkey依然会发送事件
 - --monitor-native-crashes：指定是否监视并报告应用程序发生崩溃的本地代码
 - --pct-touch ｛+百分比｝：调整触摸事件的百分比
 - --pct-motion ｛+百分比｝：调整动作事件的百分比
 - --pct-trackball ｛+百分比｝：调整轨迹事件的百分比
 - --pct-nav ｛+百分比｝：调整“基本”导航事件的百分比（导航事件由来自方向输入设备的up/down/left/right组成）
 - --pct-majornav ｛+百分比｝：调整“主要”导航事件的百分比（中间按键、回退按键、菜单按键）
 - --pct-appswitch ｛+百分比｝：调整启动Activity的百分比
 - --pct-anyevent ｛+百分比｝：调整其它类型事件的百分比
 
 ## 脚本执行Monkey
  - befoTest.shell
 ```
 #!/bin/bash
set -x
#把测试的log保存到txt文件中
./Test.shell 2>&1 | tee ./test_log.txt
 ```
  - Test.shell
  ```
  #!/bin/bash
set -x
#adb shell monkey [options]
#adb shell monkey -v 1000
# 循环执行2次
for j in $(seq 1 2)
do
	dir=$(adb  shell  ls  /data/data)
	for i in $dir
	do
	     #对	data/data下的所有包进行测试 
	     echo $i
	     adb shell monkey --throttle 500  --ignore-crashes --ignore-timeouts --monitor-native-crashes -v 500 -p  $i
	     sleep 1
	done   
done
  ```
