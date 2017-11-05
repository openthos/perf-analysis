# EventLoggingServer代码分析
## 1、compile.sh

注意：首先需要在EventLoggingServer目录下创建bin目录

编译src/servers/*.java src/servers/reach/*.java src/common/*.java文件，将class文件放到bin目录下，并将该目录下的所有文件打成jar包

## 2、 BaseServer.java
定义了listenSocket方法，供具体Server继承

## 3、 BaseWorker.java
基本工作线程

## 4、 Definition.java
定义端口

## 5、 PrefixParser.java
解析前缀

## 6、Collector.java和CollectorWorker.java
具体实现的Server

最终log收集在bin目录下
