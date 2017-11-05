
# AndroStep：Android Storage Performance Analysis Tool
智能手机上的Android应用产生了独特的IO请求，目前现存的IO工作负载生成器和跟踪捕捉工具都不是为Android App设计的，鉴于此设计了一种Android存储性能分析工具，专门用于描述和分析Android设备的IO子系统。

## 具体介绍
Android IO栈由四部分组成：1）DBMS(数据库管系统)；2）文件系统；3）IO守护进程；4）IO调度器。    
在Android 4.0.4（ICS）中分别对应的是SQLite、EXT4、mmqcd进程以及CFQ调度器（完全公平IO队列）。    

其中SQLite占据了写操作中80%的部分，其有着一些独特的IO特性：1）由fsync()产生的4KB随机写；2）对小（小于12KB）且短寿命文件的频繁创建和删除。    
因此一些现有的工作负载生成以及跟踪捕获工具都对Android不太适合。    

AndroStep主要是由两部分组成：Mobibench（工作负载生成）以及Mobile Storage Analyzer(MOST，工作负载分析)。Mobibench是一个Android App，产生例如：随机or顺序IO，同步or缓存IO。 

## 结论
[Mobile benchmark tool(mobibench)](https://github.com/ESOS-Lab/Mobibench)    
[Mobile Storage Analyzer](https://github.com/ESOS-Lab/MOST)    
论文中描述的工具在github上，有具体的使用教程，在进行进一步调研后测试使用    


# Buffered FUSE：optimising the Android IO stack for user-level filesystem
描述了Android具体的文件系统结构，分析FUSE导致的IO开销，并进行了改进。     
提出的缓存FUSE的关键技术有三点：1）将FUSE IO 大小扩大；2）FUSE写缓存；3）独立管理线程，提供时间驱动的FUSE缓存同步。    
最后试验出一组最优性能的配置组合，获取最大的性能提升：使用缓存FUSE，底层文件系统为XFS，IO调度设置为dead-line调度。    

## 具体介绍
Android系统最重要的IO部分就是两个分区/data以及/sdcard，两个分区的IO特性不太相同。/data中存储的是文本文件，例如：SQLite数据库；/sdcard中存储的是多媒体文件，例如：MP3、图片、视频等。因此两个目录呈现的IO特性不太一样，前者产生小而多的文件写操作，而后者产生大文件写操作，因此Android在这两个分区中使用的文件系统不太一样。    
+ 早期：/data使用EXT4，/sdcard使用VFAT    
这里的VFAT主要是因为其是嵌入式多媒体设备的标准，在为了兼容性的目的下，即使存在缺陷也还是让/sdcard分区使用VFAT文件系统    
+ 近来：/data使用EXT4，/sdcard在EXT4上加了一层FUSE
因为两者底层使用相同的EXT4文件系统，因此/sdcard也成为了/data的一个子目录，使得分区空间能够自由调度。另外为了保持兼容性的特征，在EXT4文件系统上加了一层FUSE。    

实际上目前两个分区的IO都会存在过度的开销，但是原因不太一样。具体来说/sdcard部分的IO栈有着四个部分：1）FUSE；2）本地文件系统；3）块设备的IO调度器；4）底层eMMC存储。     

这篇论文中主要描述/sdcard中的原因以及改进。    
/sdcard中的问题在于FUSE，主要原因在于FUSE，比如写入一个大小为512KB的文件，具体的流程如下：    
+ 用户调用write()产生写系统调用，VFS转发给具体的FUSE层进行操作
+ FUSE将一个大的写请求划分为多个小的写单元插入到自己的请求队列中（默认4KB大小）
+ FUSE库读取请求队列，并将这些写请求通过EXT4文件系统写入到磁盘

因此问题在于将一个大的文件转换为多个小文件进行写入，使得整个过程存在多次内核态至用户态的上下文切换。

文中描述了一个带有缓存区的FUSE，即在上面的FUSE库读取请求队列后，不像原来直接通过EXT4文件系统写入磁盘，而是将具体的请求放入到新加入的缓冲区中，之后存在一个管理线程定时刷新缓冲区内容到底层文件系统。在FUSE的缓冲区中利用并发方式对IO请求进行处理，从而有效利用手机CPU多线程的特性。

文中最后对Android目前提供的5种底层文件系统（EXT4、XFS、F2FS、BTRFS以及NILFS2）、三个标准的IO调度器（CFQ、deadline和noop）以及文中提出的bufferedFUSE进行了不同的组合的测试，最优的结果是bufferedFUSE、XFS以及deadline调度器，IO性能相比目前手机的基本的FUSE、EXT4、CFQ调度器组合提高了470%。
>cfq：完全公平I/O队列，平衡性好，但是性能不行。 
noop：无视寻道时间直接按照顺序执行IO，实际上闪存的寻道时间很短，因此noop明显提升性能。 
deadline：保证先出现的I/O请求有最短的延迟，数据读取比数据写入优先级更高，大幅改善卡顿。



## 结论
从这篇论文看来，/sdcard最根本的问题在这篇论文中已经有了解决，不过还是想调研一下关于FUSE为什么要进行大的写请求的分割的操作。     
目前看来/data部分的问题可能更难解决。     


# On the IO characteristics of the SQLite Transactions    
文章中是在SQLite事务方面的研究，事实上SQLite就是/data上IO性能的一个大的问题所在。提出了一种模式匹配算法，能够从并行的多个App应用产生的交错混杂的IO请求而导致的随机IO踪迹中，识别出SQLite事务。
因此能够对SQLite在Android IO中产生的问题排除噪音部分，能够更清楚的看到SQLite的问题并进而解决。     
文中并没有提出解决的措施，其实是在提出问题，根据算法找出的SQLite记录，从中发现了几个重要的特征：
+ SQLite事务的IO行为很低效    
+ 手机的暂停与唤醒特性会导致SQLite事务产生过分的长时间事务延迟
+ SQLite经常以一个奇怪的方式使用    
即一些SQLite事务异常大
+ SQLite事务中频繁的fdatasync()调用，使得EXT4日志记录及其低效

## 结论    
文中指出了目前Android IO中/data部分存在的问题，准备对这部分进行调研，探寻有无优化方法。


# F2FS：A New File System Designed for Flash Storage in Mobile
这是一篇PPT，描述了samsung公司为手机中的Flash存储而新提出的文件系统F2FS。    
具体来说是为了解决传统的EXT4在Android上使用的Flash这种底层存储设备中一些问题。EXT4是为了磁盘设计的，因此对于磁盘部分有着更多优化，但是这对于Flash并不适用，另外EXT4文件系统的设计没有考虑到Flash的特性。

文中很多没有理解，跟硬件比较有关，还需要继续阅读，但是简单的来说F2FS相比于传统的EXT4文件系统，对于小文件的读写性能上有了较大提升。因此前面所说/data目录下的存储数据格式对于F2FS更实用，也更能提升性能。


# 总结
目前有几个方面需要调研：    
+ /sdcard的FUSE部分为什么需要将大的写请求分割为小的写请求
+ SQLite为何会导致性能问题的产生，是否可以进行优化
+ 传统EXT4与F2FS有什么不同，对两种文件系统进行深入理解

另外在调研过程中，发现有人提出Android中binder存在的问题，即具体的手机服务（例如手机电量查询等）由位于用户态的Context Manager进行管理（也是Binder的一部分），但是当App进行请求时还是需要走内核态的binder部分走，存在多次的上下文切换问题，可能导致效率下降，考虑是否可以进行优化，但是目前存在问题即Binder部分会对发起请求的进程进行权限的检查，如果在优化中能够保证Binder的权限不产生问题，这是需要考虑的一个方面。因此在下周对Binder这部分的内容也进行一些调研，了解具体情况。
