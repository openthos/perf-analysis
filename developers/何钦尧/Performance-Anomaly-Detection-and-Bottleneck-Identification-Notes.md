# Performance Anomaly Detection and Bottleneck Identification

本文提供了一个关于性能异常检测和诊断的方法的一个综述，将已有的方法按照如下的标准进行了归类。

* detection goals
* nature of application and systems
* system observability
* detection methods

## Introduction

在大型系统中的性能异常和故障会造成大量的损失。

## Background

Performance Anomaly的种类：

* Point
* Collective
* Contextual
* Pattern

Performance Bottleneck：

* Resource Saturation

## Related Works

* Online performance anomaly prediction and prevention for complex distributed systems 博士论文
* Adaptive system anomaly prediction for large-scale hosting infrastructures，adaptive runtime anomaly prediction，context aware，sample every two second，inject various fault to cause anomaly，监测的指标列表，比较和几种传统的方法
* Online anomaly prediction for robust cluster systems，Bayes learning，online alert，inject fault
* Workload-aware anomaly detection for web applications, local outlier factor, dynamic workload, inject fault
* An lof-based adaptive anomaly detection scheme for cloud computing, contextual anomalies, adaptive, knowledge based, malicious port scan
* Ensemble of bayesian predictors and decision trees for proactive failure management in cloud computing systems, unsupervised combine with supervised
* A hybrid anomaly detection framework in cloud computing using one-class and two-class support vector machines, semi-supervised, fault injection program, which is able to randomly inject four major types with 17 sub-types, CPU usage, process creation, task switching activity, memory and swap space utilization, paging and page faults, interrupts, network activity, I/O and data transfer, power management



fault injection 方法：

* Causes of failure in web applications
* Model-driven system capacity planning under workload burstiness
* Ranking the importance of alerts for problem determination in large computer systems
* PeerWatch: a fault detection and diagnosis tool for virtualized consolidation systems

四类：

* CPU intensive loop
* memory leak
* disk I/O error
* network anomaly