# procfs
## sys
Access to dynamically-configurable kernel options under /proc/sys. 
Under /proc/sys appear directories representing the areas of kernel, containing readable and writable virtual files.
For example, a commonly referenced virtual file is /proc/sys/net/ipv4/ip_forward, because it is necessary for routing firewalls or tunnels. The file contains either a '1' or a '0': if it is 1, the IPv4 stack forwards packets not meant for the local host, if it is 0 then it does not.

目录下的文件不仅能提供系统的有关信息，而且还允许用户立即停止或开启内核的某些特性及功能。

sysctl -a 也可以查看


### abi 
### crypto  
### debug
### dev
device specific information 
### fs

### kernel
This directory reflects general kernel behaviors and the contents will be dependent upon your configuration. 

#### acct
该文件有三个可配置值，（resume，suspend，timeout）

resume %：如果系统已经停止记帐，则文件系统的空闲空间超过该百分值时就开始进行进程记帐；
suspend%：如果文件系统的空闲空间低于该百分值时则停止进行进程记帐；
timeout：检查文件系统可用空间的间隔时间，单位为秒。	
默认4 2 30：
如果包含日志的文件系统上只有少于 2% 的可用空间，则这些值会使记帐停止，如果有 4% 或更多可用空间，则再次启动记帐。每 30 秒做一次检查。
> 多数UNIX系统提供了一个执行进程记帐的选项。当被启动时，内核每次在一个进程终止时写一个记帐记录。这些记帐记录一般是命令名的少量二进制数据、使用的CPU时间量、用户ID和组ID、开始时间，等等。

[Linux下用户组、文件权限详解](http://www.cnblogs.com/123-/p/4189072.html)

#### acpi_video_flags
See Doc*/kernel/power/video.txt, it allows mode of video boot to be set during run time.

#### auto_msgmni
This variable has no effect and may be removed in future kernel
releases. Reading it always returns 0.
Up to Linux 3.17, it enabled/disabled automatic recomputing of msgmni
upon memory add/remove or upon ipc namespace creation/removal.
Echoing "1" into this file enabled msgmni automatic recomputing.
Echoing "0" turned it off. auto_msgmni default value was 1.

#### bootloader_type
X86 only 

x86 bootloader identification

This gives the bootloader type number as indicated by the bootloader,
shifted left by 4, and OR'd with the low four bits of the bootloader
version.  The reason for this encoding is that this used to match the
type_of_loader field in the kernel header; the encoding is kept for
backwards compatibility.  That is, if the full bootloader type number
is 0x15 and the full version number is 0x234, this file will contain
the value 340 = 0x154.

See the type_of_loader and ext_loader_type fields in
Documentation/x86/boot.txt for additional information.

#### bootloader_version
X86 only 

x86 bootloader version

The complete bootloader version number.  In the example above, this
file will contain the value 564 = 0x234.

See the type_of_loader and ext_loader_ver fields in
Documentation/x86/boot.txt for additional information.


#### cad_pid


#### cap_last_cap

Highest valid capability of the running kernel.  Exports
CAP_LAST_CAP from the kernel.


#### compat-log
#### core_pattern
#### core_pipe_limit
#### core_uses_pid
#### ctrl-alt-del
该文件有一个二进制值，该值控制系统在接收到 ctrl+alt+delete 按键组合时如何反应。这两个值表示： 

0：捕获 ctrl+alt+delete，并将其送至 pid为cad_pid的进程。这将允许系统可以完美地关闭和重启，就好象您输入 shutdown 命令一样。

1：不捕获 ctrl+alt+delete，将执行非干净的关闭，就好象直接关闭电源一样。	0

#### dmesg_restrict
#### domainname
该文件用于配置网络域名。它没有缺省值，也许已经设置了域名，也许没有设置。

```
[root@localhost kernel]# cat domainname 
(none)

```
#### ftrace_dump_on_oops
#### ftrace_enabled
#### hardlockup_all_cpu_backtrace
#### hardlockup_panic
#### hostname
该文件用于配置主机名。

```
[root@localhost kernel]# cat hostname 
localhost.localdomain

```


#### io_delay_type
#### kexec_load_disabled
#### keys
#### kptr_restrict
#### kstack_depth_to_print
#### latencytop
#### max_lock_depth
#### modprobe
#### modules_disabled
#### msgmax
该文件指定了从一个进程发送到另一个进程的消息的最大长度。进程间的消息传递是在内核的内存中进行，不会交换到磁盘上，所以如果增加该值，则将增加操作系统所使用的内存数量。单位：字节	8192

#### msgmnb
该文件指定在一个消息队列中最大的字节数。单位：字节	16384

#### msgmni
该文件指定消息队列标识的最大数目.

#### msg_next_id

#### ngroups_max
每个用户最大的组数	65536

#### nmi_watchdog
NMI watchdog(non maskable interrupt)又称硬件watchdog，用于检测OS是否hang，系统硬件定期产生一个NMI，而每个NMI调用内核查看其中断数量，如果一段时间(10秒)后其数量没有显著增长，则判定系统已经hung，接下来启用panic机制即重启OS，如果开启了Kdump还会产生crash dump文件；
APIC(advanced programmable interrupt controller)：高级可编程中断控制器，默认内置于各个x86CPU中，在SMP中用于CPU间的中断；比较高档的主板配备有IO-APIC，负责收集硬件设备的中断请求并转发给APIC；
要使用NMI Watchdog必须先激活APIC，SMP内核默认启动
该参数有2个选项：0不激活；1/2激活，有的硬件支持1有的支持2；

#### ns_last_pid
#### numa_balancing
#### numa_balancing_scan_delay_ms
#### numa_balancing_scan_period_max_ms
#### numa_balancing_scan_period_min_ms
#### numa_balancing_scan_size_mb
#### osrelease
操作系统的版本

```
[root@localhost kernel]# cat osrelease 
4.8.6-300.fc25.x86_64

```

#### ostype
操作系统的类型	Linux

#### overflowgid
#### overflowuid
#### panic
当内核panic时是否重启，0不重启，非0值表示N秒后重启

[关于panic](http://blog.csdn.net/ylyuanlu/article/details/9115159)

#### panic_on_io_nmi
#### panic_on_oops
当系统发生oops或BUG时，所采取的措施，

0：继续运行

1：系统拖延几分钟，让klogd记录oops的输出，然后panics。如果/proc/sys/kernel/panic这时不为空，则系统重启。

#### panic_on_rcu_stall
#### panic_on_stackoverflow
#### panic_on_unrecovered_nmi
#### panic_on_warn
#### perf_cpu_time_max_percent
#### perf_event_max_contexts_per_stack
#### perf_event_max_sample_rate
#### perf_event_max_stack
#### perf_event_mlock_kb
#### perf_event_paranoid
#### pid_max
系统最大pid值，在大型系统里可适当调大

#### poweroff_cmd
#### print-fatal-signals
#### printk
文件有四个数字值，它们根据日志记录消息的重要性，定义将其发送到何处。关于不同日志级别的更多信息，请阅读 syslog(2) 联机帮助页。该文件的四个值为： 

控制台日志级别：优先级高于该值的消息将被打印至控制台

缺省的消息日志级别：将用该优先级来打印没有优先级的消息

最低的控制台日志级别：控制台日志级别可被设置的最小值（最高优先级）

缺省的控制台日志级别：控制台日志级别的缺省值


```
[root@localhost kernel]# cat printk
4	4	1	7

```


#### printk_delay
#### printk_devkmsg
#### printk_ratelimit
过多的printk的消息会是控制台崩溃，甚至有可能是系统日志文件溢出。该文件给出了执行printk语句的频率，过高的频率会降低整个系统的运行速度。缺省时不能超过5秒，以防止 DOS的攻击。	

5
#### printk_ratelimit_burst
在ratelimiting前，所发送的信息

#### pty
[Linux中tty、pty、pts的概念区别](http://blog.sina.com.cn/s/blog_638ac15c01012e0v.html)
##### max
所能分配的PTY的最多个数
##### nr
当前分配的pty的个数
##### reserve


#### random
#### randomize_va_space
#### real-root-dev
#### sched_autogroup_enabled
#### sched_cfs_bandwidth_slice_us
#### sched_child_runs_first
#### sched_domain
#### sched_latency_ns
#### sched_migration_cost_ns
#### sched_min_granularity_ns
#### sched_nr_migrate
#### sched_rr_timeslice_ms
#### sched_rt_period_us
#### sched_rt_runtime_us
#### sched_schedstats
#### sched_shares_window_ns
#### sched_time_avg_ms
#### sched_tunable_scaling
#### sched_wakeup_granularity_ns
#### sem
#### sem_next_id
#### sg-big-buff
#### shmall
#### shmmax
#### shmmni
#### shm_next_id
#### shm_rmid_forced
#### softlockup_all_cpu_backtrace
#### softlockup_panic
#### soft_watchdog
#### stack_tracer_enabled
#### sysctl_writes_strict
#### sysrq
#### tainted
#### threads-max
系统允许的最大线程数
justin_$ more threads-max
774028
Linux无法直接控制单个进程可拥有的线程数，但有参考公式max = VM/stack_size，默认stack为8k，可通过降低stack大小或增加虚拟内存来调大每个进程可拥有的最大线程数；
#### timer_migration
#### traceoff_on_warning
#### tracepoint_printk
#### unknown_nmi_panic
#### unprivileged_bpf_disabled
#### usermodehelper
#### version
#### watchdog
#### watchdog_cpumask
#### watchdog_thresh
#### yama


### net
/proc/sys/net/子目录更是与网络息息相关，我们可以通过设置此目录下的某些文件来开启与网络应用相关的特殊功能，同时，也可以通过设置这个目录下的某些文件来保护我们的网络安全。

 The interface to the networking parts of the kernel is located in /proc/sys/net. The following table shows all possible subdirectories. You may see only some of them, depending on your kernel's configuration. Our main focus will be on IP networking since AX15, X.25, and DEC Net are only minor players in the Linux world. Should you wish review the online documentation and the kernel source to get a detailed view of the parameters for those protocols not covered here. In this section we'll discuss the subdirectories listed above. As default values are suitable for most needs, there is no need to change these values.

The interface  to  the  networking  parts  of  the  kernel  is  located  in
/proc/sys/net. The following table shows all possible subdirectories.  You may
see only some of them, depending on your kernel's configuration.


#### core
Network core options

##### bpf_jit_enable
基于时间规则的编译器，用于基于PCAP（packet capture library）并使用伯克利包过滤器（Berkeley Packet Filter，如tcpdump）的用户工具，可以大幅提升复杂规则的处理性能。
0：禁止
1：开启
2：开启并请求编译器将跟踪数据时间写入内核日志

##### bpf_jit_harden
##### busy_poll
默认对网络设备进行poll和select操作的超时时间(us)，具体数值最好以sockets数量而定


##### busy_read
默认读取在设备帧队列上数据帧的超时时间(us)，推荐值：50

##### default_qdisc
##### dev_weight
Work quantum for packet processing scheduler. The default value is 64.


##### flow_limit_cpu_bitmap
##### flow_limit_table_len
##### max_skb_frags

##### message_burst
A higher message_cost factor, results in fewer messages that will be written.
设置每十秒写入多少次请求警告；此设置可以用来防止DOS攻击
##### message_cost
 These parameters are used to limit the warning messages written to the kernel log from the networking code. They enforce a rate limit to make a denial-of-service attack impossible.  Message_burst controls when messages will be dropped. The default settings limit warning messages to one every five seconds.
 设置每一个警告的度量值，缺省为5，当用来防止DOS攻击时设置为0
##### netdev_budget
每次软中断处理的网络包个数

##### netdev_max_backlog
Maximum number of packets, queued on the INPUT side, when the interface receives packets faster than kernel can process them.
设置当个别接口接收包的速度快于内核处理速度时允许的最在的包序列，缺省为300；
```
cat netdev_max_backlog 
1000

```

##### netdev_rss_key
##### netdev_tstamp_prequeue
##### optmem_max
Maximum ancillary buffer size allowed per socket. Ancillary data is a sequence of struct cmsghdr structures with appended data.
设置每个socket的最大补助缓存大小,
表示每个socket所允许的最大缓冲区的大小(字节)

##### rmem_default
The default setting of the socket receive buffer in bytes.

##### rmem_max
The maximum receive socket buffer size in bytes.

##### rps_sock_flow_entries
##### somaxconn
##### tstamp_allow_data
##### warnings
##### wmem_default
The default setting (in bytes) of the socket send buffer.

##### wmem_max
The maximum send socket buffer size in bytes.

##### xfrm_acq_expires
##### xfrm_aevent_etime
##### xfrm_aevent_rseqth
##### xfrm_larval_drop


#### ipv4

##### cipso_cache_bucket_size
cipso_cache_enable
cipso_rbm_optfmt
cipso_rbm_strictvalid
##### conf
fib_multipath_use_neigh
fwmark_reflect
##### icmp_echo_ignore_all
##### icmp_echo_ignore_broadcasts
设置内核不应答icmp echo包，或指定的广播，值为0是允许回应，值为1是禁止；
Turn on (1) or off (0), if the kernel should ignore all ICMP ECHO requests, or just those to broadcast and multicast addresses.

Please note that if you accept ICMP echo requests with a broadcast/multicast destination address your network may be used as an exploder for denial of service packet flooding attacks to other hosts.

##### icmp_errors_use_inbound_ifaddr


##### icmp_ignore_bogus_error_responses
默认值是0.
某些路由器违背RFC1122标准，其对广播帧发送伪造的响应来应答。这种违背行为通常会被以告警的方式记录在系统日志中。如果该选项设置为True，内核不会记录这种警告信息。(我个人而言推荐设置为1)

icmp_msgs_burst
icmp_msgs_per_sec
##### icmp_ratelimit
限制发向特定目标的匹配icmp_ratemask的ICMP数据报的最大速率。0表示没有任何限制，否则表示jiffies数据单位中允许发送的个数。(如果在icmp_ratemask进行相应的设置Echo Request的标志位掩码设置为1,那么就可以很容易地做到ping回应的速度限制了)

icmp_ratemask
igmp_link_local_mcast_reports
igmp_max_memberships
igmp_max_msf
igmp_qrv
##### inet_peer_maxttl
##### inet_peer_minttl
##### inet_peer_threshold
INET对端存储器某个合适值，当超过该阀值条目将被丢弃。该阀值同样决定生存时间以及废物收集通过的时间间隔。条目越多﹐存活期越低﹐GC 间隔越短

##### ip_default_ttl
默认值为 64.
表示IP数据报的Time To Live值(在网络传递中,每经过一"跳",该值减少1,当ttl为0的时候，丢弃该包.该值越大,即在网络上可以经过的路由器设备的数量越多,但一个错误的包，也会越发浪费生存周期.根据目前的实际情形而看，设置为32已经足够普通网络访问Internet的需求了)

##### ip_dynaddr
默认值是0,
假如甚至为非0值,那么将支持动态地址.如果是设置为>1的值,将在动态地址改写的时候发一条内核消息。(如要用动态界面位址做 dail-on-demand ﹐那就设定它。一旦请求界面起来之
后﹐所有看不到回应的本地 TCP socket 都会重新捆绑(rebound)﹐以获得正确的位址。
假如遇到该网络界面的连线不工作﹐但重新再试一次却又可以的情形﹐设定这个可解决这
个问题。)


ip_early_demux
##### ip_forward
Enable or disable forwarding of IP packages between interfaces. Changing this value resets all other parameters to their default values. They differ if the kernel is configured as host or router.

ip_forward_use_pmtu

#### ipfrag_high_thresh
##### ipfrag_low_thresh

用来组装分段的IP包的最大内存量。两个文件分别表示用于重组IP分段的内存分配最低值和最高值，一旦达到最高内存分配值，其它分段将被丢弃，直到达到最低内存(ipfrag_low_thresh 见下文)分配值。

(根据我个人理解,就是达到最高后,就"关门打狗",直到处理到最低值的时候才又开门放分段的ip包进来处理.如果最高/最低差距过小,很可能很快又达到限制又开始丢弃包;而设置过大,又会造成某段时间丢包时间持续过久.因此需要适当地考虑,默认值中给出的最低/最高比率值为3/4.此外补充说明,kernel中,对内存的使用单位,都是以byte为单位的.当TCP数据包传输发生错误时，开始碎片整理。有效的数据包保留在内存，同时损坏的数据包被转发。我在1G内存的NAT机器上,分别设置最低为262144,最高为393216)


ipfrag_max_dist
ipfrag_secret_interval
##### ipfrag_time
保存一个IP分片在内存中的时间。
##### ip_local_port_range
Range of ports used by TCP and UDP to choose the local port. Contains two numbers, the first number is the lowest port, the second number the highest local port. Default is 1024-4999. Should be changed to 32768-61000 for high-usage systems.

定于TCP和UDP使用的本地端口范围，第一个数是开始，第二个数是最后端口号，默认值依赖于系统中可用的内存数：

\> 128Mb 32768-61000

1024-4999 or even less.

该值决定了活动连接的数量，也就是系统可以并发的连接数(做nat的时候,我将它设置为了1024 65530 工作正常)

ip_local_reserved_ports
ip_nonlocal_bind
##### ip_no_pmtu_disc
默认值为FALSE(0)
关闭路径MTU探测(典型的瓶颈原理,一次成功的传输中,mtu是由网络上最"窄"的位置决定的.如果IP层有一个数据报要传，而且数据的长度比链路层的MTU还大，那么IP层就需要进行分片（fragmentation），把数据报分成若干片，这样每一片都小于MTU。



```
16Mb/ s令牌网(IBM)　　17914
4Mb/ s令牌网(IEEE 802.5)　4464
FDDI　　　　　　　　　 4352
以太网　　　　　　　　 1500
IEEE 802.3/802.2　　　　　1492
X.25　　　　　　　　　　576
点对点(低延时)　　　　　296
```




##### neigh
ping_group_range
##### route
tcp_abort_on_overflow
tcp_adv_win_scale
tcp_allowed_congestion_control
tcp_app_win
tcp_autocorking
tcp_available_congestion_control
tcp_base_mss
tcp_challenge_ack_limit
tcp_congestion_control
tcp_dsack
tcp_early_retrans
##### tcp_ecn

 This file controls the use of the ECN bit in the IPv4 headers, this is a new feature about Explicit Congestion Notification, but some routers and firewalls block traffic that has this bit set, so it could be necessary to echo 0 to /proc/sys/net/ipv4/tcp_ecn, if you want to talk to this sites. For more info you could read RFC2481.
 
tcp_ecn_fallback
tcp_fack
tcp_fastopen
tcp_fastopen_key
tcp_fin_timeout
tcp_frto
tcp_fwmark_accept
tcp_invalid_ratelimit
tcp_keepalive_intvl
tcp_keepalive_probes
tcp_keepalive_time
tcp_limit_output_bytes
tcp_low_latency
tcp_max_orphans
tcp_max_reordering
tcp_max_syn_backlog
tcp_max_tw_buckets
tcp_mem
tcp_min_rtt_wlen
tcp_min_tso_segs
tcp_moderate_rcvbuf
tcp_mtu_probing
tcp_no_metrics_save
tcp_notsent_lowat
tcp_orphan_retries
tcp_pacing_ca_ratio
tcp_pacing_ss_ratio
tcp_probe_interval
tcp_probe_threshold
tcp_recovery
tcp_reordering
tcp_retrans_collapse
##### tcp_retries1
Defines how often an answer to a TCP connection request is retransmitted before giving up.


##### tcp_retries2
Defines how often a TCP packet is retransmitted before giving up.


tcp_rfc1337
tcp_rmem
tcp_sack
tcp_slow_start_after_idle
tcp_stdurg
tcp_synack_retries
tcp_syncookies
tcp_syn_retries
tcp_thin_dupack
tcp_thin_linear_timeouts
tcp_timestamps
tcp_tso_win_divisor
tcp_tw_recycle
tcp_tw_reuse
tcp_window_scaling
tcp_wmem
tcp_workaround_signed_windows
udp_mem
udp_rmem_min
udp_wmem_min
xfrm4_gc_thresh


#### ipv6
#### netfilter
#### nf_conntrack_max
#### unix


### sunrpc
### vm
