# 基于Framework层对Android应用性能分析

## 摘要

移动应用市场竞争激烈，应用的性能直接关乎到用户的体验和选择。为了提高和保持应用的质量，开发人员需要了解影响性能的位置并进行优化。本文是基于Android系统的Framework层进行应用性能分析，通过在Framework层的关键代码位置添加Log，找到应用异步调用的关键路径。。。。。

关键词：

## 0引言

 （研究背景以及创新点 ）

## 1 Android 背景

### 1.1 FrameWork层介绍  

### 1.2 异步任务处理机制

## 2 目标

## 3 设计概述

## 4 详细设计方案

### 4.1 点击事件
http://blog.csdn.net/baidu_23287903/article/details/52032035
简介点击事件的四种实现方式
几种实现方式都是调用framework的onClick，所以添加log的位置为：

### 4.2 消息处理
Handler线程传递消息机制解析，并确定添加Log的位置

### 4.3 子线程开启器的五种方式

#### 4.3.1 Thread
http://blog.csdn.net/kesalin/article/details/37659547/   Thread开启的流程=》确定添加Log的位置
#### 4.3.2  handlerThread

#### 4.3.3 TntentService

#### 4.3.4 AsyncTask

#### 4.3.5 ThreadPool

### 4.4 界面刷新

## 5 实验结果

### 5.1 自己写的测试用例

### 5.2 OPENTHOS中startMenu的分析

## 6 结语

参考文献：







