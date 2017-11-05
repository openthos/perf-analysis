# EventLogging代码分析

## 1、StartupReceiver.java

监听手机的开机广播，一旦接受到，开启ServerService服务

## 2、ServerService.java   

1. 创建UserSpaceServer实例mUserServer并调用其start()方法开启该线程

1. 创建KernelEventServer实例mKernelServer并调用start()方法开启该线程
  
1. 动态注册一个batterybroadcastIntentReceiver，如果手机处于充电或者满电的状态，就动态注册一个networkbroadcastReceiver，并将
NetworkListenerRegistered赋值为true，如果手机不处于充电状态，并且注册了networkbroadcastReceiver，就撤销注册，并将
NetworkListenerRegistered赋值为false

1. 当收到网络已连接的广播，networkbroadcastReceiver创建SendFiles实例mSender，如果存储记录的文件存在并且网络为wifi，将mSender作为参数传入Thread构造方法中创建Thread实例，并调用start（）开启线程

## 3、UserSpaceServer.java
UserSpaceServer继承于Thread，创建一个1234端口，将ServerWorker作为参数传入Thread构造方法中创建Thread实例，并调用start（）开启线程，

## 4、ServerWorker.java
将用户空间记录写入BufferQueue中

## 5、KernelEventServer.java
KernelEventServer继承于Thread，从/proc/event_logging下读取内核数据，写入BufferQueue中

## 6、SendFiles.java
创建LogUploader对象mUploader，并调用其send方法发送用户和内核记录

## 7、LogUploader.java
将用户和内核记录发送到服务端，如果失败了，获取Writer对象mWriter，调用其writeToFile方法保存到sdcard中

## 5、Writer.java
将用户和内核数据保存在sdcard中

## 9、EventLoggingActivity.java
包含一个按钮用来开启和关闭ServerService

## 8、ConfigChange.java

## 10、SystemInfo.java



