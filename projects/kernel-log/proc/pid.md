# proc
## [pid]
### 1. attr（Problem）
目录文件。记录进程的安全属性，可以读取or设置（SELinux）。只有在内核中配置了CONFIG_SECURITY参数后才能提供。
#### 1.1 current
当前进程的安全属性
#### 1.2 exec
随后的execve调用的安全属性
#### 1.3 fscreate
被进程调用open、mkdir、symlink、mknod创建出来的文件的安全属性
#### 1.4 keycreate

???

#### 1.5 prev
上次执行前的上下文，即调用此进程的上下文
#### 1.6 sockcreate
被这个进程创建的socket使用的上下文

### 2. autogroup
记录当前进程的自动进程组信息。执行setsid系统调用时创建新的进程组；当其创建子进程时，子进程也属于此进程组；当进程组中最后一个进程退出时，自动进程组随之销毁。
[index : kernel/git/torvalds/linux.git（autogroup commit信息）](http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=5091faa449ee0b7d73bc296a93bca9540fc51d0a)
```
#(example)
#cat /proc/1/autogroup
/autogroup-2 nice 0
```

### 3. auxv
二进制信息。记录ELF文件的解释信息，是启动动态链接器从而执行程序的必要信息。具体参数值可在```/usr/include/elf.h```中找到对照信息以及具体含义

### 4. cgroup
记录当前进程属于哪些子系统，子系统是cgroup的资源控制系统。cgroup用来对一组进程所占用的资源做限制、统计、隔离。
以下参数的解释来自于Docker
```
#(example)
#cat /proc/1/cgroup
10:hugetlb:/user.slice/user-1000.slice/session-c2.scope //hugetlb大页使用配置控制
9:memory:/init.scope        //可以设定cgroup中任务对内存使用量的限定，并且自动生成这些任务对内存资源使用情况的报告
8:cpuset:/        //可以为cgroup中的任务分配独立的CPU（针对多处理器系统）和内存
7:pids:/init.scope
6:net_cls:/        //通过使用等级识别符标记网络数据包，从而允许Linux流量控制程序识别从具体cgroup中生成的数据包
5:freezer:/        //可以挂起或回复cgroup中的任务
4:blkio:/init.scope        //可以为块设备设定I/O限制
3:cpu,cpuacct:/init.scope        //cpu用于使用调度程序控制任务对CPU的使用；cpuacct用于自动生成cgroup中任务对CPU资源使用情况的报告
2:devices:/init.scope        //用于开启or关闭任务对设备的访问
1:name=systemd:/init.scope
```

### 5. clear_refs
此文件只能由进程的所有者进行写入操作，不能被读取。
当一个非零数写入其中时，会清除相应的进程的所有的PG_referenced和PAGE_ACCESSED标志。可以用来计算进程使用了多少内存。

### 6. cmdline
记录命令行参数
```
#(example)
#cat /proc/cmdline
/sbin/init
```

### 7. comm
记录启动此进程的可执行文件名称
```
#(example)
#cat /proc/1/comm
systemd
```

### 8. coredump_filter
指定当前进程出现coredump时要转储的内存段（另外，系统默认不产生coredump文件，因此当需要的时候要打开core文件的限制）。
文件内容是一个32位的16进制数，通过低7位来指定七个内存段的转储与否：
+ bit 0 ：anonymous private memory（匿名私有内存段）    
+ bit 1 ：anonymous shared memory（匿名共享内存段）    
+ bit 2 ：file-backed private memory（file-backed 私有内存段）    
+ bit 3 ：file-backed shared memory（file-bakced 共享内存段）    
+ bit 4 ：ELF header pages in file-backed private memory areas (it iseffective only if the bit 2 is cleared)（ELF 文件映射，只有在bit 2 复位的时候才起作用）    
+ bit 5 ：hugetlb private memory（大页面私有内存）    
+ bit 6 ：hugetlb shared memory（大页面共享内存）    

```
#(example)
#cat /proc/1/coredump_filter
00000033

#将其换算为二进制：00110011
#根据上面的bit描述来看，当出现coredump需要转储匿名私有内存段、匿名共享内存段、大页面私有内存段 以及 大页面共享内存段
```


### 9. cpuset（Problem）
confine processes to processor and memory node subsets，即基于cgroup的cpu使用限制配置
```
#(example)
#cat /proc/1/cpuset
/  
```

### 10. cwd
软链接文件，指向了进程当前的工作目录
```
#(example)
#ls -l /proc/1/cwd
lrwxrwxrwx 1 root root 0 Jan  8 05:51 cwd -> /
```

### 11. environ
记录此进程的环境变量内容
```
#(example)
#cat /proc/1/environ
TERM=linux
```

### 12. exe
软链接文件，指向了正在执行文件
```

```

### 13. fd
是一个目录。记录了进程打开的所有文件，每个文件以其文件描述符号码为名称的软链接表示，这些软链接指明了具体的文件，pipe,  device, socket等的位置
```
#(example)
#ls -l /proc/1/fd
total 0
lrwx------ 1 root root 64 Jan  8 05:47 0 -> /dev/null
lrwx------ 1 root root 64 Jan  8 05:47 1 -> /dev/null
lr-x------ 1 root root 64 Jan  8 05:53 10 -> /proc/1/mountinfo
lr-x------ 1 root root 64 Jan  8 05:53 11 -> anon_inode:inotify
lr-x------ 1 root root 64 Jan  8 05:53 12 -> /proc/swaps
lrwx------ 1 root root 64 Jan  8 05:53 13 -> socket:[9910]
..．
lrwx------ 1 root root 64 Jan  8 05:53 34 -> socket:[9938]
lrwx------ 1 root root 64 Jan  8 05:53 35 -> anon_inode:[timerfd]
lr-x------ 1 root root 64 Jan  8 05:53 36 -> /dev/autofs
lr-x------ 1 root root 64 Jan  8 05:53 37 -> pipe:[9973]
lrwx------ 1 root root 64 Jan  8 05:53 38 -> socket:[11334]
lrwx------ 1 root root 64 Jan  8 05:53 39 -> anon_inode:[timerfd]
lrwx------ 1 root root 64 Jan  8 05:53 4 -> anon_inode:[eventpoll]
...
lrwx------ 1 root root 64 Jan  8 05:53 9 -> anon_inode:[eventpoll]
```

### 14. fdinfo
目录文件，已打开文件的对应信息，具体各参数如下：
+ pos    
  文件偏移量
+ flags    
  对应file结构体中的f_flags字段，表示文件的访问权限
+ mnt_id    
  文件描述符号码

```
#(example)
#ls -l /proc/1/fdinfo
total 0
-r-------- 1 root root 0 Jan  8 05:57 0
-r-------- 1 root root 0 Jan  8 05:57 1
-r-------- 1 root root 0 Jan  8 05:57 10
...
-r-------- 1 root root 0 Jan  8 05:57 9

#(example)
#cat /proc/1/fdinfo/8
pos:    0
flags:    02004002
mnt_id:    8
```

### 15. io
读写字节数目以及读写系统调用次数。
```
#(example)
#cat /proc/1/io
rchar: 50720173        //读出的总字节数，read或pread的长度总和
wchar: 2260304522        //写入的粽子节数，write或pwrite的长度总和
syscr: 52300        //read或pread的总调用次数
syscw: 552278        //write或pwrite的总调用次数
read_bytes: 109913088        //实际从磁盘中读取的字节数
write_bytes: 2237005824        //实际写入到磁盘中的字节数
cancelled_write_bytes: 6557696        //由于截断pagecache导致应该发生而没有发生的写入字节数（可能为负数）
```

### 16.limits
记录此进程的运行环境的各项限制值，包括硬限制、软限制等
```
#(example)
#cat /proc/1/limits
Limit(限制名称)          Soft Limit(软限制)   Hard Limit(硬限制)    Units(单位)     
Max cpu time              unlimited            unlimited            seconds   
Max file size             unlimited            unlimited            bytes     
Max data size             unlimited            unlimited            bytes     
Max stack size            8388608              unlimited            bytes     
Max core file size        unlimited            unlimited            bytes     
Max resident set          unlimited            unlimited            bytes     
Max processes             15716                15716                processes 
Max open files            65536                65536                files     
Max locked memory         65536                65536                bytes     
Max address space         unlimited            unlimited            bytes     
Max file locks            unlimited            unlimited            locks     
Max pending signals       15716                15716                signals   
Max msgqueue size         819200               819200               bytes     
Max nice priority         0                    0                    
Max realtime priority     0                    0                    
Max realtime timeout      unlimited            unlimited            us 
```

### 17. map_files
目录文件。内容为以虚拟内存地址范围命名的软链接文件，指明了可执行文件和所加载的所有库文件
```
#(example)
#ls -l /proc/1/map_files
total 0
lr-------- 1 root root 64 Jan  8 06:07 5635f4a42000-5635f4b2a000 -> /usr/lib/systemd/systemd
lr-------- 1 root root 64 Jan  8 06:07 5635f4b2b000-5635f4b50000 -> /usr/lib/systemd/systemd
lr-------- 1 root root 64 Jan  8 06:07 5635f4b50000-5635f4b51000 -> /usr/lib/systemd/systemd
lr-------- 1 root root 64 Jan  8 06:07 7fa7e9798000-7fa7e979c000 -> /usr/lib/libattr.so.1.1.0
...
lr-------- 1 root root 64 Jan  8 06:07 7fa7ec947000-7fa7ec96a000 -> /usr/lib/ld-2.24.so
lr-------- 1 root root 64 Jan  8 06:07 7fa7ecb69000-7fa7ecb6a000 -> /usr/lib/ld-2.24.so
lr-------- 1 root root 64 Jan  8 06:07 7fa7ecb6a000-7fa7ecb6b000 -> /usr/lib/ld-2.24.so

```

### 18. maps
以文本形式描述的进程运行内存内存图，与当前进程有关联的所有可执行文件和库文件在虚拟内存地址中的映射区域、访问权限等参数形成的列表。
具体参数如下：	
+ address        
  进程占用的地址空间    
+ perms        
  访问权限集    
  r=read; w=write; x=execute; s=shared; p=private（copy on write）    
+ offset        
  文件偏移量    
+ dev        
  设备号（主设备号：次设备号）    
+ inode        
  文件具体的inode号。    
  0表示没有inode关联互内存区域
```
#(example)
#cat /proc/1/maps
#address                  perms  offset  dev  inode
559235185000-55923526d000 r-xp 00000000 08:01 799480                     /usr/lib/systemd/systemd
55923526e000-559235293000 r--p 000e8000 08:01 799480                     /usr/lib/systemd/systemd
559235293000-559235294000 rw-p 0010d000 08:01 799480                     /usr/lib/systemd/systemd
...
7fc1fcdeb000-7fc1fcdec000 r--p 00022000 08:01 789676                     /usr/lib/ld-2.24.so
7fc1fcdec000-7fc1fcded000 rw-p 00023000 08:01 789676                     /usr/lib/ld-2.24.so
7fc1fcded000-7fc1fcdee000 rw-p 00000000 00:00 0 
7ffc5f05c000-7ffc5f07d000 rw-p 00000000 00:00 0                          [stack]
7ffc5f148000-7ffc5f14a000 r--p 00000000 00:00 0                          [vvar]
7ffc5f14a000-7ffc5f14c000 r-xp 00000000 00:00 0                          [vdso]
ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]
```

### 19. mem（Problem）
进程虚拟内存，在进行I/O操作前需要调用lseek()移至有效偏移量
```
#(example)
#cat /proc/1/mem
Input/output error
```

### 20. mountinfo
文件系统的挂载信息，具体各项参数如下：
+ (1) mount ID     
  挂载的唯一标识符
+ (2) parent ID     
  父挂载标识符
+ (3) major:minor         
  设备号（主：次）
+ (4) root    
  挂载的文件系统的根目录
+ (5) mount point    
  挂载点
+ (6) mount options    
  挂载参数
+ (7) optional fields    
  不定数量的形式为tag[:value]格式的信息
+ (8) separator
  标记optional fields项结束
+ (9) filesystem type    
  文件系统名称，以type[.subtype]的形式记录
+ (10) mount source    
  文件系统的信息
+ (11) super options    
  对于super block（超级块）的参数
```
#(example)
#cat /proc/1/mountinfo
#1 2  3   4 5     6                               7        8 9    10   11
16 20 0:4 / /proc rw,nosuid,nodev,noexec,relatime shared:5 - proc proc rw
17 20 0:16 / /sys rw,nosuid,nodev,noexec,relatime shared:6 - sysfs sys rw
18 20 0:6 / /dev rw,nosuid,relatime shared:2 - devtmpfs dev rw,size=2011756k,nr_inodes=502939,mode=755
19 20 0:17 / /run rw,nosuid,nodev,relatime shared:11 - tmpfs run rw,mode=755
...
72 19 0:39 / /run/user/0 rw,nosuid,nodev,relatime shared:28 - tmpfs tmpfs rw,size=403260k,mode=700
74 20 0:40 / /mnt/hgfs rw,nosuid,nodev,relatime shared:29 - fuse.vmhgfs-fuse vmhgfs-fuse rw,user_id=0,group_id=0,allow_other
```

### 21. mounts
当前进程的文件系统挂载信息
```
#(example)
#cat /proc/1/mounts
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
sys /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0
dev /dev devtmpfs rw,nosuid,relatime,size=2011756k,nr_inodes=502939,mode=755 0 0
run /run tmpfs rw,nosuid,nodev,relatime,mode=755 0 0
...
tmpfs /run/user/0 tmpfs rw,nosuid,nodev,relatime,size=403260k,mode=700 0 0
vmhgfs-fuse /mnt/hgfs fuse.vmhgfs-fuse rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other 0 0
```

### 22. mountstats
当前进程挂载信息记录，具体参数信息如下：
+ (1) 挂载设备名    
+ (2) 挂载点    
+ (3) 文件系统种类    
+ (4) 选项和配置信息    

```
#(example)
#cat /proc/1/mountstats
#      （1）            （2）      （3）  （4）
device proc mounted on /proc with fstype proc
device sys mounted on /sys with fstype sysfs
device dev mounted on /dev with fstype devtmpfs
...
device vmware-vmblock mounted on /run/vmblock-fuse with fstype fuse.vmware-vmblock
device fusectl mounted on /sys/fs/fuse/connections with fstype fusectl
device tmpfs mounted on /run/user/0 with fstype tmpfs
device vmhgfs-fuse mounted on /mnt/hgfs with fstype fuse.vmhgfs-fuse
```

### 23. net（Problem）
目录文件。进程网络相关信息

TODO：net目录下各文件

### 24. ns
目录文件，记录当前进程所属的namespace
```
#(example)
#ls -l /proc/1/ns
total 0
lrwxrwxrwx 1 root root 0 Jan  8 04:53 cgroup -> cgroup:[4026531835]
lrwxrwxrwx 1 root root 0 Jan  8 04:53 ipc -> ipc:[4026531839]
lrwxrwxrwx 1 root root 0 Jan  8 04:53 mnt -> mnt:[4026531840]
lrwxrwxrwx 1 root root 0 Jan  8 04:53 net -> net:[4026531957]
lrwxrwxrwx 1 root root 0 Jan  8 04:53 pid -> pid:[4026531836]
lrwxrwxrwx 1 root root 0 Jan  8 04:53 uts -> uts:[4026531838]
```

### 25. numa_maps
NUMA的内存映射，记录了进程的内存区域正在被哪一个节点使用的信息。具体参数信息如下：
+ (1) 起始地址    
+ (2) 对于当前内存区域的memory policy（用于numa架构中）    
  Memory policy：In the Linux kernel, "memory policy" determines from which node the kernel will allocate memory in a NUMA system or in an emulated NUMA system.  Linux has supported platforms with Non-Uniform Memory Access architectur.
+ (3) 不固定的信息    
  N<node>=<pages>  node使用了多少个page    
  file=<filename>  内存映射的文件名    
  heap  表示内存区域用于堆    
  stack  表示内存区域用于堆栈    
  huge  大内存区域    
  anon=<pages>  范围内的匿名page数    
  dirty=<pages>  “脏页”数    
  mapped=<pages>  已映射page数(只有在数目与anon、dirty数目不同时才会显示)    
  mapmax=<count>  最大映射数    
  swapcache=<count>  被分配给交换设备的page数    
  active=<pages>  活页数    
  writeback=<pages>  当前写入到磁盘中的page数    

```
#(example)
#cat /proc/1/numa_maps
#(1)         (2)     (3)
559235185000 default file=/usr/lib/systemd/systemd mapped=218 mapmax=3 active=142 N0=218 kernelpagesize_kB=4
55923526e000 default file=/usr/lib/systemd/systemd anon=37 dirty=37 mapmax=2 N0=37 kernelpagesize_kB=4
559235293000 default file=/usr/lib/systemd/systemd anon=1 dirty=1 mapmax=2 N0=1 kernelpagesize_kB=4
...
7fc1fcdeb000 default file=/usr/lib/ld-2.24.so anon=1 dirty=1 mapmax=2 N0=1 kernelpagesize_kB=4
7fc1fcdec000 default file=/usr/lib/ld-2.24.so anon=1 dirty=1 N0=1 kernelpagesize_kB=4
7fc1fcded000 default anon=1 dirty=1 N0=1 kernelpagesize_kB=4
7ffc5f05b000 default stack anon=6 dirty=6 mapmax=2 N0=6 kernelpagesize_kB=4
7ffc5f148000 default
7ffc5f14a000 default
```

### 26. oom_adj
出现OOM时进程被kill的权值。范围为[-17,15]，越小意味着越不容易被kill。可以向其中写入数据进行更改
```
#(example)
#cat /proc/1/oom_adj
0
```

### 27. oom_score
出现OOM时进程被kill的分值，即出现OOM的时候哪个进程会被内核选择杀死，数值范围为[0,1000]，badness越高越容易被kill，0表示不会被选择kill，1000则表示总是被kill。
```
#(example)
#cat /proc/1/oom_score
0
```

### 28. oom_score_adj
用于调整oom_score中所记录的值。
```
#(example)
#cat /proc/1/oom_score_adj
0
```

### 29. pagemap
通过读取该文件，从而查看用户态进程每个虚拟页映射到的物理页。


### 30. personality
记录进程执行域。因为可能是较为敏感的信息，所以只有文件所有者可以读取。
```
#(example)
#cat /proc/1/personality
00000000
```

### 31. root
软链接文件，指向根目录

### 32. sched
进程调度信息，大多数字段计算方法在sched.c和sched_fair.c文件中。

se.avg的结构是 struct sched_avg  in include/linux/sched.h中，用于smp调度统计

```
/*
 * The load_avg/util_avg accumulates an infinite geometric series
 * (see __update_load_avg() in kernel/sched/fair.c).
 *
 * [load_avg definition]
 *
 *   load_avg = runnable% * scale_load_down(load)
 *
 * where runnable% is the time ratio that a sched_entity is runnable.
 * For cfs_rq, it is the aggregated load_avg of all runnable and
 * blocked sched_entities.
 *
 * load_avg may also take frequency scaling into account:
 *
 *   load_avg = runnable% * scale_load_down(load) * freq%
 *
 * where freq% is the CPU frequency normalized to the highest frequency.
 *
 * [util_avg definition]
 *
 *   util_avg = running% * SCHED_CAPACITY_SCALE
 *
 * where running% is the time ratio that a sched_entity is running on
 * a CPU. For cfs_rq, it is the aggregated util_avg of all runnable
 * and blocked sched_entities.
 *
 * util_avg may also factor frequency scaling and CPU capacity scaling:
 *
 *   util_avg = running% * SCHED_CAPACITY_SCALE * freq% * capacity%
* where freq% is the same as above, and capacity% is the CPU capacity
 * normalized to the greatest capacity (due to uarch differences, etc).
 *
 * N.B., the above ratios (runnable%, running%, freq%, and capacity%)
 * themselves are in the range of [0, 1]. To do fixed point arithmetics,
 * we therefore scale them to as large a range as necessary. This is for
 * example reflected by util_avg's SCHED_CAPACITY_SCALE.
 *
 * [Overflow issue]
 *
 * The 64-bit load_sum can have 4353082796 (=2^64/47742/88761) entities
 * with the highest load (=88761), always runnable on a single cfs_rq,
 * and should not overflow as the number already hits PID_MAX_LIMIT.
 *
 * For all other cases (including 32-bit kernels), struct load_weight's
 * weight will overflow first before we do, because:
 *
 *    Max(load_avg) <= Max(load.weight)
 *
 * Then it is the load_weight's responsibility to consider overflow
 * issues.
 */
struct sched_avg {
        u64 last_update_time, load_sum;
        u32 util_sum, period_contrib;
        unsigned long load_avg, util_avg;
};

```





```
#(example)
#cat /proc/1/sched
systemd (1, #threads: 1)
-------------------------------------------------------------------
se.exec_start                                :      10641651.970868  //此进程最近被调度到的开始执行时刻
se.vruntime                                  :           139.854055  //虚拟运行时间
se.sum_exec_runtime                          :          1162.274514  //累计运行的物理时间
se.nr_migrations                             :                  206  //需要迁移当前进程到其他cpu时累加此字段
nr_switches                                  :                 1105  //主动切换和被动切换的累计次数
nr_voluntary_switches                        :                  883  //主动切换次数（由于prev->state为不可运行状态引起的切换）
nr_involuntary_switches                      :                  222  //被动切换次数
se.load.weight                               :              1048576   //该se的load
se.avg.load_sum                              :               556434   //smp下的ready态进程的负载累计和???
se.avg.util_sum                              :               402117   //smp下的ready+block态进程的负载累计和???
se.avg.load_avg                              :                   11   //smp下的ready态进程的负载均值???
se.avg.util_avg                              :                    8  //smp下的ready+block态进程的负载均值???
se.avg.last_update_time                      :       10641651970868  //smp下的对avg的上次更新时间
policy                                       :                    0  //调度策略，0表示normal
prio                                         :                  120  //优先级(nice=0)
clock-delta                                  :                  200  //cpu_clock函数的执行开销
mm->numa_scan_seq                            :                    0  //进行numa balance扫描的频率 
numa_pages_migrated                          :                    0  //进行了numa迁移的页个数
numa_preferred_nid                           :                   -1  //
total_numa_faults                            :                    0  //属于numa faults的次数。                           numa_faults is an array split into four regions:
                        faults_memory, faults_cpu, faults_memory_buffer, faults_cpu_buffer
                        in this precise order.
current_node=0, numa_group_id=0
numa_faults node=0 task_private=0 task_shared=0 group_private=0 group_shared=0
```

### 33. schedstat
调度状态信息。总共三个数据，具体解释如下：
+ 累计运行的物理时间，同```/proc/<pid>/sched```文件中的se.sum_exec_runtime/1000000    
+ 累计在就绪队列里的等待时间    
+ 主动与被动切换的累计次数，同```/proc/<pid>/sched```文件中的nr_switches    

```
#(example)
#cat /proc/1/schedstat
1162274514 174247328 1105
```

### 34. smaps
在Linux内核 2.6.16中引入了一个系统内存接口特性，位于/proc/$pid/目录下的smaps文件中 ，记录进程内存中所有的映射情况，类似于详细信息版本的/proc/[pid]/maps
（该文件只有在开启了内核的CONFIG_MMU选项了才会产生）

```
#(example)
#cat /proc/1/smaps
559235185000-55923526d000 r-xp 00000000 08:01 799480                    /usr/lib/systemd/systemd   //该虚拟内存段的开始和结束位置 r--s内存段的权限，最后一位p代表私有，s代表共享
                           // 00000000 该虚拟内存段在对应的映射文件中的偏移量
                           // 08:01  文件的主设备和次设备号 
                           // 799480  被映射到虚拟内存的文件的索引节点号 
                           // ...systemd 被映射到虚拟内存的文件名称.
                           // 后面带(deleted)的是内存数据，可以被销毁。
Size:                928 kB   // 映射区域的总大小, 是进程使用内存空间，并不一定实际分配了内存(VSS) 
Rss:                 872 kB   // 当前驻留于内存中的大小，即实际内存的占用量(不需要缺页中断就可以使用的) 。不包括已经交换出去的代码
Pss:                 409 kB   // 是平摊计算后的使用内存(有些内存会和其他进程共享，例如mmap进来的) , Private Rss，映射到内存的页面中仅由进程单独使用的量
Shared_Clean:        860 kB  //驻留在内存中与其他内存共享部分的“干净页面”（未改写）大小
Shared_Dirty:          0 kB  //驻留在内存中与其他内存共享部分的“赃页”（已改写）大小
Private_Clean:        12 kB  //驻留在内存中私有的“干净页面”大小
Private_Dirty:         0 kB  //驻留在内存中私有的“赃页”大小
Referenced:          872 kB  //标记为访问和使用的内存大小
Anonymous:             0 kB  //不来自于文件的内存大小
AnonHugePages:         0 kB  //不来自于文件的大页内存大小
ShmemPmdMapped:        0 kB  //shows the ammount of shared (shmem/tmpfs) memory backed by huge pages.   
Shared_Hugetlb:        0 kB  //show the ammounts of memory backed by hugetlbfs page which is not counted in "RSS"
Private_Hugetlb:       0 kB //show the ammounts of memory backed by hugetlbfs page which is not counted in "PSS"
Swap:                  0 kB //shows how much would-be-anonymous memory is also used, but out on swap. For shmem mappings, "Swap" includes also the size of the mapped (and not replaced by copy-on-write) part of the underlying shmem object out on swap.
SwapPss:               0 kB //shows proportional swap share of this mapping. Unlike "Swap", this does not take into account swapped out page of underlying shmem objects.
KernelPageSize:        4 kB //内核页大小
MMUPageSize:           4 kB //MMU页大小
Locked:                0 kB  //indicates whether the mapping is locked in memory or not.
VmFlags: rd ex mr mw me dw 
  rd - readable 
  wr - writeable 
  ex - executable 
  sh - shared 
  mr - may read 
  mw - may write 
  me - may execute 
  ms - may share 
  gd - stack segment growns down 
  pf - pure PFN range 
  dw - disabled write to the mapped file 
  lo - pages are locked in memory 
  io - memory mapped I/O area 
  sr - sequential read advise provided 
  rr - random read advise provided 
  dc - do not copy area on fork 
  de - do not expand area on remapping 
  ac - area is accountable 
  nr - swap space is not reserved for the area 
  ht - area uses huge tlb pages 
  ar - architecture specific flag 
  dd - do not include area into core dump 
  sd - soft-dirty flag 
  mm - mixed map area 
  hg - huge page advise flag 
  nh - no-huge page advise flag 
  mg - mergable advise flag 
...
```

### 35. stack
记录进程的内核堆栈的调试信息
```
#(example)
#cat /proc/1/stack
[<ffffffff81252f2b>] ep_poll+0x27b/0x350
[<ffffffff8125443e>] SyS_epoll_wait+0xce/0xf0
[<ffffffff815f8032>] entry_SYSCALL_64_fastpath+0x1a/0xa4
[<ffffffffffffffff>] 0xffffffffffffffff
```

### 36. stat
当前进程的所有状态信息。各项参数解释请参照[PROC系列之---/proc/pid/stat](http://blog.csdn.net/zjl_1026_2001/article/details/2294067) 
```
#(example)
#cat /proc/6873/stat
6873 (a.out) R 6723 6873 6723 34819 6873 8388608 77 0 0 0 41958 31 0 0 25 0 3 0 5882654 1409024 56 4294967295 134512640 134513720 3215579040 0 2097798 0 0 0 0 0 0 0 17 0 0 0

pid=6873 进程(包括轻量级进程，即线程)号
comm=a.out 应用程序或命令的名字
task_state=R 任务的状态，R:runnign, S:sleeping (TASK_INTERRUPTIBLE), D:disk sleep (TASK_UNINTERRUPTIBLE), T: stopped, T:tracing stop,Z:zombie, X:dead
ppid=6723 父进程ID
pgid=6873 线程组号
sid=6723 c该任务所在的会话组ID
tty_nr=34819(pts/3) 该任务的tty终端的设备号，INT（34817/256）=主设备号，（34817-主设备号）=次设备号
tty_pgrp=6873 终端的进程组号，当前运行在该任务所在终端的前台任务(包括shell 应用程序)的PID。
task->flags=8388608 进程标志位，查看该任务的特性
min_flt=77 该任务不需要从硬盘拷数据而发生的缺页（次缺页）的次数
cmin_flt=0 累计的该任务的所有的waited-for进程曾经发生的次缺页的次数目
maj_flt=0 该任务需要从硬盘拷数据而发生的缺页（主缺页）的次数
cmaj_flt=0 累计的该任务的所有的waited-for进程曾经发生的主缺页的次数目
utime=1587 该任务在用户态运行的时间，单位为jiffies
stime=1 该任务在核心态运行的时间，单位为jiffies
cutime=0 累计的该任务的所有的waited-for进程曾经在用户态运行的时间，单位为jiffies
cstime=0 累计的该任务的所有的waited-for进程曾经在核心态运行的时间，单位为jiffies
priority=25 任务的动态优先级
nice=0 任务的静态优先级
num_threads=3 该任务所在的线程组里线程的个数
it_real_value=0 由于计时间隔导致的下一个 SIGALRM 发送进程的时延，以 jiffy 为单位.
start_time=5882654 该任务启动的时间，单位为jiffies
vsize=1409024（page） 该任务的虚拟地址空间大小
rss=56(page) 该任务当前驻留物理地址空间的大小
Number of pages the process has in real memory,minu 3 for administrative purpose.
这些页可能用于代码，数据和栈。
rlim=4294967295（bytes） 该任务能驻留物理地址空间的最大值
start_code=134512640 该任务在虚拟地址空间的代码段的起始地址
end_code=134513720 该任务在虚拟地址空间的代码段的结束地址
start_stack=3215579040 该任务在虚拟地址空间的栈的结束地址
kstkesp=0 esp(32 位堆栈指针) 的当前值, 与在进程的内核堆栈页得到的一致.
kstkeip=2097798 指向将要执行的指令的指针, EIP(32 位指令指针)的当前值.
pendingsig=0 待处理信号的位图，记录发送给进程的普通信号
block_sig=0 阻塞信号的位图
sigign=0 忽略的信号的位图
sigcatch=082985 被俘获的信号的位图
wchan=0 如果该进程是睡眠状态，该值给出调度的调用点
nswap 被swapped的页数，当前没用
cnswap 所有子进程被swapped的页数的和，当前没用
exit_signal=17 该进程结束时，向父进程所发送的信号
task_cpu(task)=0 运行在哪个CPU上
task_rt_priority=0 实时进程的相对优先级别
task_policy=0 进程的调度策略，0=非实时进程，1=FIFO实时进程；2=RR实时进程  
```

### 37. statm
记录内存使用方面的信息，具体各项参数信息如下：
+ size (same as VmSize in /proc/[pid]/status）    
  程序内存总大小
+ resident (same as VmRSS in /proc/[pid]/status)    
  实际使用物理内存大小
+ share (from shared mappings)    
  共享页面数量
+ text (code)    
  代码段大小
+ lib (library)    
  库文件大小
+ data data + stack    
  数据段与堆栈段大小总和
+ dt (dirty pages)    
  “脏页”数量
```
#(example)
#cat /proc/1/statm
#size resident share text lib data dt
33733   1607   1302  232  0   4403  0
```

### 38. status
进程的各种信息（进程id、凭证、内存使用量、信号等等）
```
#(example)
#cat /proc/1/status
Name:    systemd        /*产生此进程的命令*/
Umask:    0000
State:    S (sleeping)        /*进程的当前状态*/
Tgid:    1        /*进程组id号*/
Ngid:    0
Pid:    1        /*进程id号*/
PPid:    0
TracerPid:    0
Uid:    0    0    0    0
Gid:    0    0    0    0
FDSize:    64        /*目前已分配文件描述符个数*/
Groups:
NStgid:    1
NSpid:    1
NSpgid:    1
NSsid:    1
VmPeak:      200468 kB        /*虚拟内存峰值*/
VmSize:      134932 kB        /*虚拟内存大小*/
VmLck:           0 kB        /*已锁虚拟内存大小*/
VmPin:           0 kB
VmHWM:        6428 kB        /*实际使用物理内存峰值（即进程的“高水位”）*/
VmRSS:        6428 kB        /*实际使用物理内存大小*/
RssAnon:        1220 kB
RssFile:        5208 kB
RssShmem:           0 kB
VmData:       17476 kB        /*数据段大小*/
VmStk:         136 kB        /*堆栈段大小*/
VmExe:         928 kB        /*文本段大小*/
VmLib:        7176 kB        /*共享库大小*/
VmPTE:         124 kB        /*页表项大小*/
VmPMD:          12 kB
VmSwap:           0 kB
HugetlbPages:           0 kB
Threads:    1        /*进程中所含线程数量*/
SigQ:    0/15716
SigPnd:    0000000000000000
ShdPnd:    0000000000000000
SigBlk:    7be3c0fe28014a03
SigIgn:    0000000000001000
SigCgt:    00000001800004ec
CapInh:    0000000000000000
CapPrm:    0000003fffffffff
CapEff:    0000003fffffffff
CapBnd:    0000003fffffffff
CapAmb:    0000000000000000
Seccomp:    0
Cpus_allowed:    ffffffff,ffffffff,ffffffff,ffffffff
Cpus_allowed_list:    0-127
Mems_allowed:    00000000,00000001
Mems_allowed_list:    0
voluntary_ctxt_switches:    885
nonvoluntary_ctxt_switches:    222
```

### 39. syscall
用于记录系统调用，时间顺序为从文件末尾至文件开头。
```
#(example)
#cat /proc/1/syscall
232 0x4 0x7ffc5f07bc50 0x36 0xffffffff 0x431bde82d7b634db 0xc60 0x7ffc5f07bc40 0x7fc1fba23dd3
```
其中```0x7fc1fba23dd3```这种类型的数表示内存地址，而对于一些类似于```232```这样的数可能表示数组索引（文件描述符），也可能表示系统调用号。


### 40. task
目录文件。进程包含的线程，其内容为各个目录文件，以线程的ID命名，代表各个线程

### 41. timerslack_ns
当前进程的定时器延迟时间，单位为纳秒（nanoseconds）
```
#(example)
#cat /proc/1/timerslack_ns
50000
```

### 42. wchan
如果当前进程处于睡眠状态，记录引起调度的调用函数
```
#(example)
#cat /proc/1/wchan
ep_poll
```
