# procfs
## proc
### meminfo
meminfo:机器的内存使用信息
```
(example)
cat /proc/meminfo
MemTotal:        8098644 kB   所有可用RAM大小 （即物理内存减去一些预留位和内核的二进制代码大小）
MemFree:         2256520 kB   LowFree与HighFree的总和，被系统留着未使用的物理内存。(MemTotal-MemFree)就是已被用掉的内存。
MemAvailable:    5212720 kB   (3.14+) An estimate of how much memory is available for starting new applications, without swapping.有些应用程序会根据系统的可用内存大小自动调整内存申请的多少，所以需要一个记录当前可用内存数量的统计值，MemFree并不适用，因为MemFree不能代表全部可用的内存，系统中有些内存虽然已被使用但是可以回收的，比如cache/buffer、slab都有一部分可以回收，所以这部分可回收的内存加上MemFree才是系统可用的内存，即MemAvailable。/proc/meminfo中的MemAvailable是内核使用特定的算法估算出来的，要注意这是一个估计值，并不精确。
Buffers:          764376 kB   Memory in buffer cache, so relatively temporary storage for raw disk blocks. This shouldn't get very large.　用来给文件做缓冲大小
Cached:          2582784 kB   Memory in the pagecache (Diskcache and Shared Memory)．　被高速缓冲存储器（cache memory）用的内存的大小
SwapCached:            0 kB   Memory that is present within main memory, but also in the swapfile. (If memory is needed this area does not need to be swapped out AGAIN because it is already in the swapfile. This saves I/O and increases performance if machine runs short on memory.)　被高速缓冲存储器（cache memory）用的交换空间的大小 已经被交换出来的内存，但仍然被存放在swapfile中。用来在需要的时候很快的被替换而不需要再次打开I/O端口
Active:          3916628 kB   Memory that has been used more recently and usually not swapped out or reclaimed．　在活跃使用中的缓冲或高速缓冲存储器页面文件的大小
Inactive:        1416784 kB　　Memory that has not been used recently and can be swapped out or reclaimed．
Active(anon):    1989080 kB　　Anonymous memory that has been used more recently and usually not swapped out
Inactive(anon):   455696 kB　　Anonymous memory that has not been used recently and can be swapped out
Active(file):    1927548 kB　　Pagecache memory that has been used more recently and usually not reclaimed until needed
Inactive(file):   961088 kB　　Pagecache memory that can be reclaimed without huge performance impact．
Unevictable:         176 kB　　Unevictable pages can't be swapped out for a variety of reasons
Mlocked:             176 kB　　Pages locked to memory using the mlock() system call. Mlocked pages are also Unevictable.
SwapTotal:       2928636 kB   交换空间的总大小
SwapFree:        2928636 kB　　The remaining swap space available
Dirty:               232 kB   等待被写回到磁盘的内存大小
Writeback:             0 kB   正在被写回到磁盘的内存大小
AnonPages:       1986424 kB   未映射页的内存大小
Mapped:           949956 kB   设备和文件等映射的大小
Shmem:            458552 kB   Total used shared memory (shared between several processes, thus including RAM disks, SYS-V-IPC and BSD like SHMEM)
Slab:             368420 kB   内核数据结构缓存的大小，可以减少申请和释放内存带来的消耗
SReclaimable:     320980 kB   可收回Slab的大小
SUnreclaim:        47440 kB   The part of the Slab that can't be reclaimed under memory pressure
KernelStack:       11392 kB   The memory the kernel stack uses. This is not reclaimable.
PageTables:        54132 kB   管理内存分页页面的索引表的大小
NFS_Unstable:          0 kB   NFS pages sent to the server, but not yet commited to the storage
Bounce:                0 kB   Memory used for block device bounce buffers
WritebackTmp:          0 kB   Memory used by FUSE for temporary writeback buffers
CommitLimit:     6977956 kB   Based on the overcommit ratio ('vm.overcommit_ratio'), this is the total amount of  memory currently available to be allocated on the system. This limit is only adhered to if strict overcommit accounting is enabled (mode 2 in 'vm.overcommit_memory'). The CommitLimit is calculated with the following formula: CommitLimit = ('vm.overcommit_ratio' * Physical RAM) + Swap 
Committed_AS:    7573536 kB   An estimate of how much RAM you would need to make a 99.99% guarantee that there never is OOM (out of memory) for this workload.
VmallocTotal:   34359738367 kB   可以vmalloc虚拟内存大小
VmallocUsed:      308296 kB      amount of vmalloc area which is used
VmallocChunk:   34358947836 kB   largest contiguous block of vmalloc area which is free
HardwareCorrupted:     0 kB      The amount of RAM the kernel identified as corrupted / not working
AnonHugePages:    739328 kB    Non-file backed huge pages mapped into userspace page tables
CmaTotal:              0 kB    (3.5+) Total CMA(Contiguous Memory Allocator)  Memory
CmaFree:               0 kB    (3.5+) Free CMA(Contiguous Memory Allocator) Memory
HugePages_Total:       0       Number of hugepages being allocated by the kernel (Defined with vm.nr_hugepages). 系统当前总共拥有的HugePages数目。
HugePages_Free:        0       The number of hugepages not being allocated by a process. 系统当前总共拥有的空闲HugePages数目。
HugePages_Rsvd:        0       The number of hugepages for which a commitment to allocate from the pool has been made, but no allocation has yet been made.系统当前总共保留的HugePages数目，更具体点就是指程序已经向系统申请，但是由于程序还没有实质的HugePages读写操作，因此系统尚未实际分配给程序的HugePages数目。
HugePages_Surp:        0       指超过系统设定的常驻HugePages数目的数目。
Hugepagesize:       2048 kB    The size of a hugepage (usually 2MB on an Intel based system)
DirectMap4k:      162640 kB    The amount of memory being mapped to standard 4k pages
DirectMap2M:     7100416 kB    The amount of memory being mapped to hugepages (usually 2MB in size)
DirectMap1G:     1048576 kB    The amount of memory being mapped to hugepages (usually 1GB in size)
```

### stat
stat:实时追踪自系统上次启动以来的多种统计信息
```
(example)
cat /proc/stat
cpu  2018907 8270 2713334 37434321 169720 0 4332 0 0 0   

The very first "cpu" line aggregates the numbers in all of the other "cpuN" lines.
十个值分别表示以1/100（jiffies）秒为单位的统计值(依次为：user（用户态时间）、nice（nice值为负的进程所占用的CPU时间）、system（核心）、idle（除硬盘IO等待时间以外其它等待时间）、iowait、irq（硬中断时间）、softirq（软中断时间）steal 在guest运行模式下被其他OS偷占用的时间、guest 在guest运行模式下guest OS运行时间 、guest_nice 被niced的在guest运行模式下guest OS运行时间 

user: normal processes executing in user mode
nice: niced processes executing in user mode
system: processes executing in kernel mode
idle: twiddling thumbs
iowait: waiting for I/O to complete
irq: servicing interrupts
softirq: servicing softirqs
steal: (2.6.11+) Stolen time, which is the time spent in other operating systems when running in a virtualized environment
guest: (2.6.24+) Time spent running a virtual CPU for guest operating systems under the control of the Linux kernel.
guest_nice:(2.6.33) Time spent running a niced guest (virtual CPU for guest operating systems under the control of the Linux kernel).

cpu0 515361 2314 683293 9322930 39474 0 1482 0 0 0
cpu1 508524 1140 679219 9351987 51097 0 760 0 0 0
cpu2 499244 2783 675439 9372749 42000 0 1973 0 0 0
cpu3 495776 2032 675382 9386654 37147 0 116 0 0 0

每个具体CPU的10个统计值


intr 772741507 22 11 0 0 0 0 0 0 1 0 0 0 2 0 0 0 0 0 59 311201 0 0 0 0 0 0 0 107111 542126 3240772 8530961 21 591 663 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ...      
中断的信息，第一个为自系统启动以来，发生的所有的中断的次数；然后每个数对应一个特定的中断自系统启动以来所发生的次数

ctxt 4042696239   自系统启动以来CPU发生的上下文交换的次数
btime 1483494110  从系统启动到现在为止的时间，单位为秒
processes 19373   系统启动以来所创建的任务的个数目(total_forks)
procs_running 1   当前运行队列的任务的数目
procs_blocked 0   当前被阻塞的任务的数目
softirq 48508837 5 18240586 21946 3278362 596054 0 18229 16346722 0 10006933
```

### swaps 
swaps:系统上的交换分区及其空间利用信息，如果有多个交换分区的话，则会每个交换分区的信息分别存储于/proc/swap目录中的单独文件中，而其优先级数字越低，被使用到的可能性越大
```
(example)
cat /proc/swaps
Filename		Type		Size	  Used 	Priority
/dev/sda6   partition	 2928636	  0	     -1
```

### cmdline
cmdline:在启动时传递至内核的相关参数信息,这些信息通常由lilo或grub等启动管理工具进行传递
```
(example)
cat /proc/cmdline
BOOT_IMAGE=/vmlinuz-4.2.0-42-generic root=UUID=600a1c05-f70e-475b-9cc6-0579a3756133 ro quiet splash vt.handoff=7
```
### uptime
uptime:系统上次启动以来的运行时间，如下所示，其第一个数字表示系统运行时间，第二个数字表示系统空闲时间，单位是秒
```
(example)
cat /proc/uptime
110815.76 394338.98
```
### version
version:系统运行的内核版本号
```
(example)
cat /proc/version
Linux version 4.2.0-42-generic (buildd@lgw01-54) (gcc version 5.2.1 20151010 (Ubuntu 5.2.1-22ubuntu2) ) #49-Ubuntu SMP Tue Jun 28 21:26:26 UTC 2016
```
### mounts
mounts:系统当前挂载的所有文件系统.第一列表示挂载的设备，第二列表示在当前目录树中的挂载点，第三点表示当前文件系统的类型，第四列表示挂载属性（ro或者rw），第五列和第六列用来匹配/etc/mtab文件中的转储（dump）属性
```
(example)
cat /proc/mounts
sysfs      /sys  sysfs rw,nosuid,nodev,noexec,relatime 0 0
proc       /proc proc rw,nosuid,nodev,noexec,relatime 0 0
udev       /dev devtmpfs rw,nosuid,relatime,size=4031008k,nr_inodes=1007752,mode=755 0 0
devpts     /dev/pts devpts rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000 0 0
tmpfs      /run tmpfs rw,nosuid,noexec,relatime,size=809868k,mode=755 0 0
/dev/sda1  /ext4 rw,relatime,errors=remount-ro,data=ordered 0 0
securityfs /sys/kernel/security securityfs rw,nosuid,nodev,noexec,relatime 0 0
tmpfs      /dev/shm tmpfs rw,nosuid,nodev 0 0
tmpfs      /run/lock tmpfs rw,nosuid,nodev,noexec,relatime,size=5120k 0 0
tmpfs      /sys/fs/cgroup tmpfs rw,mode=755 0 0
cgroup     /sys/fs/cgroup/systemd cgroup rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/lib/systemd/systemd-cgroups-agent,name=systemd 0 0
pstore     /sys/fs/pstore pstore rw,nosuid,nodev,noexec,relatime 0 0
cgroup     /sys/fs/cgroup/hugetlb cgroup rw,nosuid,nodev,noexec,relatime,hugetlb,release_agent=/run/cgmanager/agents/cgm-release-agent.hugetlb 0 0
...
systemd-1  /proc/sys/fs/binfmt_misc autofs rw,relatime,fd=22,pgrp=1,timeout=0,minproto=5,maxproto=5,direct 0 0
mqueue     /dev/mqueue mqueue rw,relatime 0 0
hugetlbfs  /dev/hugepages hugetlbfs rw,relatime 0 0
debugfs    /sys/kernel/debug debugfs rw,relatime 0 0
fusectl    /sys/fs/fuse/connections fusectl rw,relatime 0 0
/dev/sda8  /var ext4 rw,relatime,data=ordered 0 0
...
cgmfs      /run/cgmanager/fs tmpfs rw,relatime,size=100k,mode=755 0 0
binfmt_misc /proc/sys/fs/binfmt_misc binfmt_misc rw,relatime 0 0
tmpfs      /run/user/1000 tmpfs rw,nosuid,nodev,relatime,size=809868k,mode=700,uid=1000,gid=1000 0 0
gvfsd-fuse /run/user/1000/gvfs fuse.gvfsd-fuse rw,nosuid,nodev,relatime,user_id=1000,group_id=1000 0 0
```
### modules
modules:当前装入内核的所有模块名称列表，可以由lsmod命令使用，也可以直接查看；如下所示，其中第一列表示模块名，第二列表示此模块占用内存空间大小，第三列表示此模块有多少实例被装入，第四列表示此模块依赖于其它哪些模块，第五列表示此模块的装载状态（Live：已经装入；Loading：正在装入；Unloading：正在卸载），第六列表示此模块在内核内存（kernel memory）中的偏移量
```
(example)
cat /proc/modules
pci_stub 16384 1 - Live 0x0000000000000000
vboxpci 24576 0 - Live 0x0000000000000000 (OE)
vboxnetadp 28672 0 - Live 0x0000000000000000 (OE)
vboxnetflt 28672 0 - Live 0x0000000000000000 (OE)
vboxdrv 454656 3 vboxpci,vboxnetadp,vboxnetflt, Live 0x0000000000000000 (OE)
binfmt_misc 20480 1 - Live 0x0000000000000000
intel_rapl 20480 0 - Live 0x0000000000000000
x86_pkg_temp_thermal 16384 0 - Live 0x0000000000000000
intel_powerclamp 16384 0 - Live 0x0000000000000000
coretemp 16384 0 - Live 0x0000000000000000
kvm_intel 167936 0 - Live 0x0000000000000000
kvm 516096 1 kvm_intel, Live 0x0000000000000000
snd_hda_codec_hdmi 49152 1 - Live 0x0000000000000000
snd_hda_codec_realtek 86016 1 - Live 0x0000000000000000
crct10dif_pclmul 16384 0 - Live 0x0000000000000000
snd_hda_codec_generic 77824 1 snd_hda_codec_realtek, Live 0x0000000000000000
crc32_pclmul 16384 0 - Live 0x0000000000000000
snd_hda_intel 36864 7 - Live 0x0000000000000000
dcdbas 16384 0 - Live 0x0000000000000000
snd_hda_codec 135168 4 snd_hda_codec_hdmi,snd_hda_codec_realtek,snd_hda_codec_generic,snd_hda_intel, Live 0x0000000000000000
snd_hda_core 65536 5 snd_hda_codec_hdmi,snd_hda_codec_realtek,snd_hda_codec_generic,snd_hda_intel,snd_hda_codec, Live 0x0000000000000000
dell_smm_hwmon 16384 0 - Live 0x0000000000000000
snd_hwdep 16384 1 snd_hda_codec, Live 0x0000000000000000
sb_edac 28672 0 - Live 0x0000000000000000
aesni_intel 167936 0 - Live 0x0000000000000000
snd_pcm 106496 5 snd_hda_codec_hdmi,snd_hda_intel,snd_hda_codec,snd_hda_core, Live 0x0000000000000000
snd_seq_midi 16384 0 - Live 0x0000000000000000
snd_seq_midi_event 16384 1 snd_seq_midi, Live 0x0000000000000000
aes_x86_64 20480 1 aesni_intel, Live 0x0000000000000000
lrw 16384 1 aesni_intel, Live 0x0000000000000000
snd_rawmidi 32768 1 snd_seq_midi, Live 0x0000000000000000
gf128mul 16384 1 lrw, Live 0x0000000000000000
snd_seq 69632 2 snd_seq_midi,snd_seq_midi_event, Live 0x0000000000000000
edac_core 53248 1 sb_edac, Live 0x0000000000000000
glue_helper 16384 1 aesni_intel, Live 0x0000000000000000
snd_seq_device 16384 3 snd_seq_midi,snd_rawmidi,snd_seq, Live 0x0000000000000000
snd_timer 32768 2 snd_pcm,snd_seq, Live 0x0000000000000000
snd 81920 24 snd_hda_codec_hdmi,snd_hda_codec_realtek,snd_hda_codec_generic,snd_hda_intel,snd_hda_codec,snd_hwdep,snd_pcm,snd_rawmidi,snd_seq,snd_seq_device,snd_timer, Live 0x0000000000000000
ablk_helper 16384 1 aesni_intel, Live 0x0000000000000000
input_leds 16384 0 - Live 0x0000000000000000
soundcore 16384 1 snd, Live 0x0000000000000000
cryptd 20480 2 aesni_intel,ablk_helper, Live 0x0000000000000000
serio_raw 16384 0 - Live 0x0000000000000000
lpc_ich 24576 0 - Live 0x0000000000000000
shpchp 36864 0 - Live 0x0000000000000000
8250_fintek 16384 0 - Live 0x0000000000000000
mei_me 36864 0 - Live 0x0000000000000000
mei 98304 1 mei_me, Live 0x0000000000000000
mac_hid 16384 0 - Live 0x0000000000000000
parport_pc 32768 0 - Live 0x0000000000000000
ppdev 20480 0 - Live 0x0000000000000000
lp 20480 0 - Live 0x0000000000000000
parport 49152 3 parport_pc,ppdev,lp, Live 0x0000000000000000
autofs4 40960 2 - Live 0x0000000000000000
hid_generic 16384 0 - Live 0x0000000000000000
usbhid 49152 0 - Live 0x0000000000000000
hid 118784 2 hid_generic,usbhid, Live 0x0000000000000000
nouveau 1388544 4 - Live 0x0000000000000000
psmouse 126976 0 - Live 0x0000000000000000
mxm_wmi 16384 1 nouveau, Live 0x0000000000000000
video 40960 1 nouveau, Live 0x0000000000000000
i2c_algo_bit 16384 1 nouveau, Live 0x0000000000000000
ttm 94208 1 nouveau, Live 0x0000000000000000
drm_kms_helper 131072 1 nouveau, Live 0x0000000000000000
e1000e 237568 0 - Live 0x0000000000000000
drm 360448 7 nouveau,ttm,drm_kms_helper, Live 0x0000000000000000
ptp 20480 1 e1000e, Live 0x0000000000000000
ahci 36864 9 - Live 0x0000000000000000
pps_core 20480 1 ptp, Live 0x0000000000000000
libahci 32768 1 ahci, Live 0x0000000000000000
wmi 20480 2 nouveau,mxm_wmi, Live 0x0000000000000000

```
### diskstats

diskstats:查看出具体的磁盘IO压力

每列参数的含义：

Column1 主设备号

Column2 次设备号

Column3 设备名称：sda为整个硬盘的统计信息，sda1为第一个分区的统计信息，ramdisk设备为通过软件将RAM当做硬盘来使用的一项技术。

Column4 成功完成读磁盘的总次数

Column5 成功完成合并读磁盘的总次数,为了效率可能会合并相邻的读和写

Column6 成功完成读扇区的总次数

Column7 所有读操作所花费的毫秒数 （用__make_request()到end_that_request_last()测量）。

Column8 成功完成写磁盘的总次数

Column9 成功完成合并写磁盘的总次数 

Column10 成功完成写扇区的总次数

Column11 所有写操作所花费的毫秒数 （用__make_request()到end_that_request_last()测量）。

Column12 正在处理的输入/输出请求数 -- -I/O的当前进度，只有这个域可以是0。当请求被交给适当的request_queue_t时增加，当请求完成时减小

Column13 正在处理的输入/输出花的时间（毫秒），这个字段是Column12的一个累加值. 只要Column12不为0, 这个域会增长。

Column14 正在处理的输入/输出操作花费的加权毫秒数,这可以提供I/O完成时间和可能积累的积压的简单测量。
```
ll@ll-pc:~$ cat /proc/diskstats
   1       0 ram0 0 0 0 0 0 0 0 0 0 0 0
   ...
   7       0 loop0 0 0 0 0 0 0 0 0 0 0 0

  11       0 sr0 0 0 0 0 0 0 0 0 0 0 0
   8       0 sda 379781 9055 19064906 2750192 3807693 3646522 308304394 94060300 0 14625908 96816640
   8       1 sda1 6655 3440 82328 32324 12895 86785 797856 186964 0 70092 219284
   8       2 sda2 5 0 10 56 0 0 0 0 0 56 56
   ...
```
### cpuinfo

cpuinfo:查看系统中CPU的提供商和相关配置信息
```
ll@ll-pc:~$ cat /proc/cpuinfo
processor	: 0      逻辑处理器的id。对于单核处理器，则可认为是其CPU编号，对于多核处理器则可以是物理核、或者使用超线程技术虚拟的逻辑核
vendor_id	: GenuineIntel　　CPU制造商
cpu family	: 6　　　CPU产品系列代号
model		: 63　　　　CPU属于其系列中的哪一代的代号
model name	: Intel(R) Xeon(R) CPU E5-1603 v3 @ 2.80GHz　　CPU属于的名字及其编号、主频
stepping	: 2　　　　CPU属于制作更新版本
microcode	: 0x27
cpu MHz		: 1199.953　　　CPU的实际使用主频
cache size	: 10240 KB　　　CPU二级缓存大小
physical id	: 0　　　 物理封装的处理器的id
siblings	: 4　　　　位于相同物理封装的处理器中的逻辑处理器的数量
core id		: 0　　　　每个核心的id
cpu cores	: 4　　　　位于相同物理封装的处理器中的内核数量
apicid		: 0　　　　用来区分不同逻辑核的编号，系统中每个逻辑核的此编号必然不同，此编号不一定连续
initial apicid	: 0
fpu		: yes　　　　　 是否具有浮点运算单元（Floating Point Unit）
fpu_exception	: yes　是否支持浮点计算异常
cpuid level	: 15　　　　执行cpuid指令前，eax寄存器中的值，根据不同的值cpuid指令会返回不同的内容
wp		: yes　　　　表明当前CPU是否在内核态支持对用户空间的写保护（Write Protection）
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm arat epb pln pts dtherm tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc　 当前CPU支持的功能
bugs		:
bogomips	: 5587.00　　　　在系统内核启动时粗略测算的CPU速度（Million Instructions Per Second）
clflush size	: 64　　　　每次刷新缓存的大小单位
cache_alignment	: 64　　　　缓存地址对齐单位
address sizes	: 46 bits physical, 48 bits virtual　　　　可访问地址空间位数
power management:　　　对能源管理的支持
```
### crypto
crypto:系统上已安装的内核使用的密码算法及每个算法的详细信息列表
```
ll@ll-pc:~$ cat /proc/crypto
name         : crct10dif
driver       : crct10dif-pclmul
module       : crct10dif_pclmul
priority     : 200
refcnt       : 1
selftest     : passed
internal     : no
type         : shash
blocksize    : 1
digestsize   : 2
```
### loadavg

loadavg:查看CPU的平均负载（可运行的进程的平均数）

每列参数的含义：

Column1 系统5分钟内的平均负载

Column2 系统10分钟内的平均负载

Column3 系统15分钟内的平均负载

Column4 正在运行的进程数／进程总数

Column5 最近运行的进程ID号

```
ll@ll-pc:~$ cat /proc/loadavg
0.39 0.31 0.37 1/564 14180
```
### locks
locks:保存当前由内核锁定的文件的相关信息，包含内核内部的调试数据；

每列参数的含义：

Column1:每个锁定占据一行，且具有一个惟一的编号；

Column2:表示当前锁定使用的锁定类别，POSIX表示目前较新类型的文件锁，由lockf系统调用产生，FLOCK是传统的UNIX文件锁，由flock系统调用产生；

Column3:通常有两种类型，ADVISORY表示不允许其他用户锁定此文件，但允许读取，MANDATORY表示此文件锁定期间不允许其他用户任何形式的访问；

Column4: reveals whether the lock is allowing the holder `READ` or `WRITE` access to the file. 

Column5: shows the ID of the process holding the lock.

Column6: shows the ID of the file being locked, format of `*MAJOR-DEVICE*:*MINOR-DEVICE*:*INODE-NUMBER*`

Column7-8: shows the start and end of the file's locked region.

```
ll@ll-pc:~$ cat /proc/locks
1: POSIX  ADVISORY  WRITE 13735 08:08:5123677 0 EOF
...
4: POSIX  ADVISORY  READ  6750 08:08:5120480 128 128
5: POSIX  ADVISORY  READ  6750 08:08:5112051 1073741826 1073742335
6: POSIX  ADVISORY  WRITE 4749 00:29:43 1 3
7: POSIX  ADVISORY  WRITE 1461 08:06:786449 0 EOF
8: POSIX  ADVISORY  READ  1249 08:08:5111973 128 128
9: POSIX  ADVISORY  READ  1249 08:08:5111971 1073741826 1073742335
...
27: FLOCK  ADVISORY  WRITE 679 00:13:774 0 EOF
```
### slabinfo
slabinfo:slab缓存信息

每列参数的含义：

name:slab对象名称；

active_objs: currently active objects 活跃的对象个数；

num_objs: total number of available objects 总的对象个数；

objsize:  size of each object 每个对象的大小，以字节为单位；

objperslab:每个slab包含的对象数目；

pageperslab：一个slab占几个page内存页

limit(tunables)：每个 CPU 可以缓存的对象的最大数量；

batchcount(tunables)：当缓存为空时转换到每个 CPU 缓存中全局缓存对象的最大数量；

sharedfactor(tunables)：说明了对称多处理器（Symmetric MultiProcessing，SMP）系统的共享行为；

active_slabs(slabdata)：活跃的slab数目；

num_slabs(slabdata)：总的slab数目；

sharedavail(slabdata)：共享的可用的slab数量；

```
root@ll-pc:/home/ll# cat /proc/slabinfo
slabinfo - version: 2.1
# name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab> : tunables <limit> <batchcount> <sharedfactor> : slabdata <active_slabs> <num_slabs> <sharedavail>
ext4_groupinfo_1k     60     60    136   30    1 : tunables    0    0    0 : slabdata      2      2      0
kvm_async_pf           0      0    136   30    1 : tunables    0    0    0 : slabdata      0      0      0
kvm_vcpu               0      0  16832    1    8 : tunables    0    0    0 : slabdata      0      0      0
kvm_mmu_page_header      0      0    168   24    1 : tunables    0    0    0 : slabdata      0      0      0
...
fuse_request          40     40    400   20    2 : tunables    0    0    0 : slabdata      2      2      0
fuse_inode            21     21    768   21    4 : tunables    0    0    0 : slabdata      1      1      0
...
dma-kmalloc-8192       0      0   8192    4    8 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-4096       0      0   4096    8    8 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-2048       0      0   2048   16    8 : tunables    0    0    0 : slabdata      0      0      0
...
dma-kmalloc-96         0      0     96   42    1 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-8192         160    168   8192    4    8 : tunables    0    0    0 : slabdata     42     42      0
...
kmalloc-16          8192   8192     16  256    1 : tunables    0    0    0 : slabdata     32     32      0
kmalloc-8           7680   7680      8  512    1 : tunables    0    0    0 : slabdata     15     15      0
kmem_cache_node      320    320     64   64    1 : tunables    0    0    0 : slabdata      5      5      0
kmem_cache           144    144    256   16    1 : tunables    0    0    0 : slabdata      9      9      0
```
### vmstat
vmstat:虚拟内存的统计信息
```
ll@ll-pc:~$ cat /proc/vmstat
nr_free_pages 758873    (2.6.31+) num of free pages
nr_alloc_batch 2111      (3.12+)
nr_inactive_anon 122602  (2.6.28+)
nr_active_anon 317429  (2.6.28+)
nr_inactive_file 255048 (2.6.28+)
nr_active_file 465424 (2.6.28+)
nr_unevictable 8 (2.6.28+)
nr_mlock 8  (2.6.28+)
nr_anon_pages 418771 (2.6.18+)
nr_mapped 116198     (2.6.0+)  映射到文件的页数
nr_file_pages 742674   (2.6.18+)
nr_dirty 45        (2.6.0+)     脏页数
nr_writeback 0     (2.6.0+)     回写页数
nr_slab_reclaimable 62287   (2.6.19+)
nr_slab_unreclaimable 13769 (2.6.19+)
nr_page_table_pages 10729    (2.6.0+) 分配到页表的页数
nr_kernel_stack 565     (2.6.32+)  Amount of memory allocated to kernel stacks.
nr_unstable 0           (2.6.0+) 不稳定页数
nr_bounce 0               (2.6.12+)
nr_vmscan_write 99770    (2.6.19+)
nr_vmscan_immediate_reclaim 1822   (3.2+)
nr_writeback_temp 0    (2.6.26+)
nr_isolated_anon 0      (2.6.32+)
nr_isolated_file 0      (2.6.32+)
nr_shmem 17239          (2.6.32+)  Pages used by shmem and tmpfs  
nr_dirtied 46018008    (2.6.37+) 
nr_written 36541457     (2.6.37+)
nr_pages_scanned 0       (3.17+)
numa_hit 6580129889     (2.6.18+)
numa_miss 0              (2.6.18+)
numa_foreign 0          (2.6.18+)
numa_interleave 21466   (2.6.18+)
numa_local 6580129889   (2.6.18+)
numa_other 0            (2.6.18+)
workingset_refault 860623  (3.15+)
workingset_activate 170829 (3.15+)
workingset_nodereclaim 0   (3.15+)
nr_anon_transparent_hugepages 452 (2.6.38+)
nr_free_cma 0              (3.7+)  Number of free CMA (Contiguous Memory Allocator) pages.
nr_dirty_threshold 288917  (2.6.37+)
nr_dirty_background_threshold 144458  (2.6.37+)
pgpgin 10909442       (2.6.0+)    从启动到现在读入的内存页数
pgpgout 156048718     (2.6.0+)    从启动到现在换出的内存页数
pswpin 9959           (2.6.0+)    从启动到现在读入的交换分区页数
pswpout 99732         (2.6.0+)    从启动到现在换出的交换分区页数
pgalloc_dma 2         (2.6.5+)    从启动到现在DMA存储区分配的页数
pgalloc_dma32 2058878682 (2.6.16+) 
pgalloc_normal 4839797005  (2.6.5+)  从启动到现在普通存储区分配的页数
pgalloc_movable 0   (2.6.5+) 
pgfree 6952846439   (2.6.0+)      从启动到现在释放的页数
pgactivate 22881709  (2.6.0+)     从启动到现在激活的页数
pgdeactivate 4047307  (2.6.0+) 	  从启动到现在去激活的页数
pgfault 5037086029   (2.6.0+)     从启动到现在二级页面错误数
pgmajfault 45336    (2.6.0+)      从启动到现在一级页面错误数
pgrefill_dma 0      (2.6.5+)      从启动到现在DMA存储区再填充的页面数
pgrefill_dma32 1175394  (2.6.16+) 
pgrefill_normal 2365597  (2.6.5+) 从启动到现在普通存储区再填充的页面数
pgrefill_movable 0    (2.6.32+) 
pgsteal_kswapd_dma 0   (3.4+) 
pgsteal_kswapd_dma32 1026794  (3.4+) 
pgsteal_kswapd_normal 2225851  (3.4+) 
pgsteal_kswapd_movable 0    (3.4+) 
pgsteal_direct_dma 0     (3.4+) 
pgsteal_direct_dma32 703834    (3.4+) 
pgsteal_direct_normal 2102082   (3.4+) 
pgsteal_direct_high             (3.4+)
pgsteal_direct_movable 0        (2.6.23+)
pgscan_kswapd_dma 0           (2.6.5+)  从启动到现在kswapd后台进程扫描的DMA存储区页面数
pgscan_kswapd_dma32 1084856  (2.6.16+)
pgscan_kswapd_normal 2319341 (2.6.5+)    从启动到现在kswapd后台进程扫描的普通存储区页面数
pgscan_kswapd_high 
pgscan_kswapd_movable 0        (2.6.23+)
pgscan_direct_dma 0         (2.6.16+)     从启动到现在DMA存储区被直接回收的页面数
pgscan_direct_dma32 766894   (2.6.16+)
pgscan_direct_normal 2245562   (2.6.16+)   从启动到现在普通存储区被直接回收的页面数
pgscan_direct_movable 0    (2.6.23+)
pgscan_direct_throttle 0     (3.6+)
zone_reclaim_failed 0        (2.6.31+)
pginodesteal 991442      (2.6.0+)  从启动到现在通过释放i节点回收的页面数
slabs_scanned 3341778    (2.6.5+) 从启动到现在被扫描的切片数
kswapd_inodesteal 258271  (2.6.0+)    从启动到现在由kswapd通过释放i节点回收的页面数
kswapd_low_wmark_hit_quickly 225 (2.6.33+)
kswapd_high_wmark_hit_quickly 361 (2.6.33+)
pageoutrun 917   (2.6.0+)  从启动到现在通过kswapd调用来回收的页面数
allocstall 32657  (2.6.0+)  从启动到现在请求直接回收的页面数
pgrotated 99986   (2.6.0+) 从启动到现在轮换的页面数
drop_pagecache 0   (3.15+)
drop_slab 0        (3.15+)
numa_pte_updates 0  (3.8+)
numa_huge_pte_updates 0   (3.18+)
numa_hint_faults 0    (3.8+)
numa_hint_faults_local 0 (3.8+)
numa_pages_migrated 0   (3.8+)
pgmigrate_success 50263574  (3.8+)
pgmigrate_fail 2851         (3.8+)
compact_migrate_scanned 77311606  (3.8+)
compact_free_scanned 1549639477   (3.8+)
compact_isolated 105711345        (3.8+)
compact_stall 205520         (2.6.35+) 
compact_fail 26260           (2.6.35+) 
compact_success 179260        (2.6.35+) 
htlb_buddy_alloc_success 0   (2.6.26+) 
htlb_buddy_alloc_fail 0    (2.6.26+) 
unevictable_pgs_culled 1   (2.6.28+) 
unevictable_pgs_scanned 0  (2.6.28+) 
unevictable_pgs_rescued 810  (2.6.28+) 
unevictable_pgs_mlocked 818   (2.6.28+) 
unevictable_pgs_munlocked 810   (2.6.28+) 
unevictable_pgs_cleared 0     (2.6.28+) 
unevictable_pgs_stranded 0    (2.6.28+) 
thp_fault_alloc 359080     (2.6.39+)
thp_fault_fallback 8833    (2.6.39+)
thp_collapse_alloc 252296   (2.6.39+)
thp_collapse_alloc_failed 17021  (2.6.39+)
thp_split 252170             (2.6.39+)
thp_zero_page_alloc 11        (3.8+)
thp_zero_page_alloc_failed 0   (3.8+)
balloon_inflate 0         (3.18+)
balloon_deflate 0         (3.18+)
balloon_migrate 0         (3.18+)
nr_tlb_remote_flush (3.12+)
nr_tlb_remote_flush_received (3.12+)
nr_tlb_local_flush_all (3.12+)
nr_tlb_local_flush_one (3.12+)
vmacache_find_calls (3.16+)
vmacache_find_hits (3.16+)
vmacache_full_flushes (3.19+)
```
### zoneinfo
zoneinfo:  (2.6.13+)
```
ll@ll-pc:~$ cat /proc/zoneinfo
Node 0, zone      DMA
  pages free     3965
        min      33
        low      41
        high     49
        scanned  0
        spanned  4095
        present  3988
        managed  3967
    nr_free_pages 3965
    nr_alloc_batch 8
    nr_inactive_anon 0
    nr_active_anon 0
    nr_inactive_file 0
    nr_active_file 0
    nr_unevictable 0
    nr_mlock     0
    nr_anon_pages 0
    nr_mapped    0
    nr_file_pages 0
    nr_dirty     0
    nr_writeback 0
    nr_slab_reclaimable 0
    nr_slab_unreclaimable 2
    nr_page_table_pages 0
    nr_kernel_stack 0
    nr_unstable  0
    nr_bounce    0
    nr_vmscan_write 0
    nr_vmscan_immediate_reclaim 0
    nr_writeback_temp 0
    nr_isolated_anon 0
    nr_isolated_file 0
    nr_shmem     0
    nr_dirtied   0
    nr_written   0
    nr_pages_scanned 0
    numa_hit     1
    numa_miss    0
    numa_foreign 0
    numa_interleave 0
    numa_local   1
    numa_other   0
    workingset_refault 0
    workingset_activate 0
    workingset_nodereclaim 0
    nr_anon_transparent_hugepages 0
    nr_free_cma  0
        protection: (0, 2354, 7857, 7857)
  pagesets
    cpu: 0
              count: 0
              high:  0
              batch: 1
  vm stats threshold: 6
    cpu: 1
              count: 0
              high:  0
              batch: 1
  vm stats threshold: 6
    cpu: 2
              count: 0
              high:  0
              batch: 1
  vm stats threshold: 6
    cpu: 3
              count: 0
              high:  0
              batch: 1
  vm stats threshold: 6
  all_unreclaimable: 1
  start_pfn:         1
  inactive_ratio:    1
Node 0, zone    DMA32
  pages free     193604
        min      5053
        low      6316
        high     7579
        scanned  0
        spanned  1044480
        present  632016
        managed  611980
    nr_free_pages 193604
    nr_alloc_batch 1262
    nr_inactive_anon 47471
    nr_active_anon 154598
    nr_inactive_file 55282
    nr_active_file 132184
    nr_unevictable 0
    nr_mlock     0
    nr_anon_pages 196003
    nr_mapped    39899
    nr_file_pages 193621
    nr_dirty     12
    nr_writeback 0
    nr_slab_reclaimable 18989
    nr_slab_unreclaimable 3273
    nr_page_table_pages 2765
    nr_kernel_stack 144
    nr_unstable  0
    nr_bounce    0
    nr_vmscan_write 44143
    nr_vmscan_immediate_reclaim 4
    nr_writeback_temp 0
    nr_isolated_anon 0
    nr_isolated_file 0
    nr_shmem     5540
    nr_dirtied   14141327
    nr_written   11309675
    nr_pages_scanned 0
    numa_hit     1957754666
    numa_miss    0
    numa_foreign 0
    numa_interleave 0
    numa_local   1957754666
    numa_other   0
    workingset_refault 221551
    workingset_activate 41733
    workingset_nodereclaim 0
    nr_anon_transparent_hugepages 156
    nr_free_cma  0
        protection: (0, 0, 5502, 5502)
  pagesets
    cpu: 0
              count: 177
              high:  186
              batch: 31
  vm stats threshold: 36
    cpu: 1
              count: 166
              high:  186
              batch: 31
  vm stats threshold: 36
    cpu: 2
              count: 121
              high:  186
              batch: 31
  vm stats threshold: 36
    cpu: 3
              count: 180
              high:  186
              batch: 31
  vm stats threshold: 36
  all_unreclaimable: 0
  start_pfn:         4096
  inactive_ratio:    4
Node 0, zone   Normal
  pages free     557816
        min      11809
        low      14761
        high     17713
        scanned  0
        spanned  1441792
        present  1441792
        managed  1408701
    nr_free_pages 557816
    nr_alloc_batch 519
    nr_inactive_anon 75131
    nr_active_anon 166887
    nr_inactive_file 199764
    nr_active_file 333243
    nr_unevictable 8
    nr_mlock     8
    nr_anon_pages 226315
    nr_mapped    76299
    nr_file_pages 549054
    nr_dirty     42
    nr_writeback 0
    nr_slab_reclaimable 43302
    nr_slab_unreclaimable 10478
    nr_page_table_pages 7966
    nr_kernel_stack 421
    nr_unstable  0
    nr_bounce    0
    nr_vmscan_write 55627
    nr_vmscan_immediate_reclaim 1818
    nr_writeback_temp 0
    nr_isolated_anon 0
    nr_isolated_file 0
    nr_shmem     11699
    nr_dirtied   31881796
    nr_written   25234633
    nr_pages_scanned 0
    numa_hit     4622485788
    numa_miss    0
    numa_foreign 0
    numa_interleave 21466
    numa_local   4622485788
    numa_other   0
    workingset_refault 639073
    workingset_activate 129096
    workingset_nodereclaim 0
    nr_anon_transparent_hugepages 296
    nr_free_cma  0
        protection: (0, 0, 0, 0)
  pagesets
    cpu: 0
              count: 137
              high:  186
              batch: 31
  vm stats threshold: 42
    cpu: 1
              count: 141
              high:  186
              batch: 31
  vm stats threshold: 42
    cpu: 2
              count: 162
              high:  186
              batch: 31
  vm stats threshold: 42
    cpu: 3
              count: 170
              high:  186
              batch: 31
  vm stats threshold: 42
  all_unreclaimable: 0
  start_pfn:         1048576
  inactive_ratio:    7
info
```
