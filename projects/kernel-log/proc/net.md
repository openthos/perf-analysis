#proc
##net
###sockstat
**explanation:**列出使用的tcp/udp/raw/pac/syc_cookies的数量  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat sockstat
sockets: used 595
TCP: inuse 1 orphan 0 tw 0 alloc 2 mem 0
UDP: inuse 5 mem 3
UDPLITE: inuse 0
RAW: inuse 0
FRAG: inuse 0 memory 0
```
###sockstat6
**explanation:**IPV6协议下sockstat状态信息  
###icmp
**explanation:**记录icmp链接状态信息  
local_address本地地址端口  
rem_address远程地址端口  
st连接状态  
tx_queue发送队列  
rx_queue接收队列    
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat icmp
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode ref pointer drops
```
###icmp6
**explanation:** 记录IPv6下icmp链接状态信息,同icmp  
###anycast6
**explanation:**在网卡上新配置一个IPv6地址，就会在 /proc/net/anycast6下生成一个对应的任播地址  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# echo 1 > /proc/sys/net/ipv6/conf/all/forwarding
root@weikang-VirtualBox:/proc/net# cat anycast6
2    enp0s3          fe800000000000000000000000000000     1
```
###dev_mcast
**explanation:**Defined in /usr/src/linux/net/core/dev_mcast.c,显示网络设备二层（数据链路层）多播地址  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat dev_mcast 
indx interface_name  dmi_u dmi_g dmi_address
2    enp0s3          1     0     01005e000001
2    enp0s3          1     0     333300000001
2    enp0s3          1     0     3333ff5ce16b
2    enp0s3          1     0     01005e0000fb
2    enp0s3          1     0     3333000000fb
2    enp0s3          2     0     333300000002
2    enp0s3          1     0     3333ff000000
```
###dev
**explanation:**记录网卡相关信息  
Receive表示收包,Transmit表示收包  
bytes表示收发的字节数  
packets表示收发正确的包量  
errs表示收发错误的包量  
drop表示收发丢弃的包量  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
enp0s3: 183382080  145110    0    0    0     0          0         0  1667024   25211    0    0    0     0       0          0
    lo:  118582     723    0    0    0     0          0         0   118582     723    0    0    0     0       0          0

```
###igmp
**explanation:**记录IGMP分组情况  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat igmp
Idx	Device    : Count Querier	Group    Users Timer	Reporter
1	lo        :     1      V3
				010000E0     1 0:00000000		0
2	enp0s3    :     2      V3
				FB0000E0     1 0:00000000		0
				010000E0     1 0:00000000		0
```
###igmp6
**explanation:** IPV6下的IGMP分组信息，同igmp相同
###ip_mr_cache
**explanation:**

**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat ip_mr_cache
Group    Origin   Iif     Pkts    Bytes    Wrong Oifs
```
###tcp
**explanation:** 记录tcp的状态链接信息  
local_address本地地址端口  
rem_address远程地址端口  
st连接状态  
tx_queue发送队列  
rx_queue接收队列   
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat tcp
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode                                                     
   0: 0101007F:0035 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 15443 1 ffff88007a448780 100 0 0 10 0 
```
###tcp6
**explanation:**记录IPV6下tcp的状态链接信息,同tcp
###udp
**explanation:**记录udp的连接状态信息  
local_address本地地址端口  
rem_address远程地址端口  
st连接状态  
tx_queue发送队列  
rx_queue接收队列  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat udp
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode ref pointer drops             
   45: 00000000:EB13 00000000:0000 07 00000000:00000000 00:00000000 00000000   111        0 14190 2 ffff88007cab23c0 0         
  335: 0101007F:0035 00000000:0000 07 00000000:00000000 00:00000000 00000000     0        0 15442 2 ffff88007cab3680 0         
  350: 00000000:0044 00000000:0000 07 00000000:00000000 00:00000000 00000000     0        0 15376 2 ffff88007cab32c0 0         
  515: 00000000:14E9 00000000:0000 07 00000000:00000000 00:00000000 00000000   111        0 14188 2 ffff88007cab2780 0         
  913: 00000000:0277 00000000:0000 07 00000000:00000000 00:00000000 00000000     0        0 14904 2 ffff88007cab2b40 0         
```
###udp6
**explanation:**记录IPV6下的udp的连接状态信息,同udp
###packet
**explanation:** 记录链路层套接字信息  
**example:**
```bash
sk       RefCnt Type Proto  Iface R Rmem   User   Inode
ffff88007974e000 3      3    0003   2     1 0      0      15375 
```
###arp
**explanation:**记录arp表的信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat arp
IP address       HW type     Flags       HW address            Mask     Device
10.0.2.2         0x1         0x2         52:54:00:12:35:02     *        enp0s3
```
###udplite
**explanation:**记录udp-lite报文链接状态信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat udplite
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode ref pointer drops             
```
###udplite6
**explanation:**记录IPV6中udp-lite报文状态链接状态信息
###protocols
**explanation:**各种协议初始化时状态信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat protocols
protocol  size sockets  memory press maxhdr  slab module     cl co di ac io in de sh ss gs se re sp bi br ha uh gp em
PACKET    1408      1      -1   NI       0   no   kernel      n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n
PINGv6    1088      0      -1   NI       0   yes  kernel      y  y  y  n  n  y  n  n  y  y  y  y  n  y  y  y  y  y  n
RAWv6     1088      1      -1   NI       0   yes  kernel      y  y  y  n  y  y  y  n  y  y  y  y  n  y  y  y  y  n  n
UDPLITEv6 1080      0      -1   NI       0   yes  kernel      y  y  y  n  y  y  y  n  y  y  y  y  n  n  y  y  y  y  n
UDPv6     1080      2       3   NI       0   yes  kernel      y  y  y  n  y  n  y  n  y  y  y  y  n  n  y  y  y  y  n
TCPv6     2056      1       0   no     304   yes  kernel      y  y  y  y  y  y  y  y  y  y  y  y  y  n  y  y  y  y  y
UNIX      1024    512      -1   NI       0   yes  kernel      n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n
UDP-Lite   920      0      -1   NI       0   yes  kernel      y  y  y  n  y  y  y  n  y  y  y  y  y  n  y  y  y  y  n
PING       880      0      -1   NI       0   yes  kernel      y  y  y  n  n  y  n  n  y  y  y  y  n  y  y  y  y  y  n
RAW        888      0      -1   NI       0   yes  kernel      y  y  y  n  y  y  y  n  y  y  y  y  n  y  y  y  y  n  n
UDP        920      5       3   NI       0   yes  kernel      y  y  y  n  y  n  y  n  y  y  y  y  y  n  y  y  y  y  n
TCP       1896      1       0   no     304   yes  kernel      y  y  y  y  y  y  y  y  y  y  y  y  y  n  y  y  y  y  y
NETLINK   1128     41      -1   NI       0   no   kernel      n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n  n
```
###netstat
**explanation:**网络流量的多种统计  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat netstat
TcpExt: SyncookiesSent SyncookiesRecv SyncookiesFailed EmbryonicRsts PruneCalled RcvPruned OfoPruned OutOfWindowIcmps LockDroppedIcmps ArpFilter TW TWRecycled TWKilled PAWSPassive PAWSActive PAWSEstab DelayedACKs DelayedACKLocked DelayedACKLost ListenOverflows ListenDrops TCPPrequeued TCPDirectCopyFromBacklog TCPDirectCopyFromPrequeue TCPPrequeueDropped TCPHPHits TCPHPHitsToUser TCPPureAcks TCPHPAcks TCPRenoRecovery TCPSackRecovery TCPSACKReneging TCPFACKReorder TCPSACKReorder TCPRenoReorder TCPTSReorder TCPFullUndo TCPPartialUndo TCPDSACKUndo TCPLossUndo TCPLostRetransmit TCPRenoFailures TCPSackFailures TCPLossFailures TCPFastRetrans TCPForwardRetrans TCPSlowStartRetrans TCPTimeouts TCPLossProbes TCPLossProbeRecovery TCPRenoRecoveryFail TCPSackRecoveryFail TCPSchedulerFailed TCPRcvCollapsed TCPDSACKOldSent TCPDSACKOfoSent TCPDSACKRecv TCPDSACKOfoRecv TCPAbortOnData TCPAbortOnClose TCPAbortOnMemory TCPAbortOnTimeout TCPAbortOnLinger TCPAbortFailed TCPMemoryPressures TCPSACKDiscard TCPDSACKIgnoredOld TCPDSACKIgnoredNoUndo TCPSpuriousRTOs TCPMD5NotFound TCPMD5Unexpected TCPSackShifted TCPSackMerged TCPSackShiftFallback TCPBacklogDrop TCPMinTTLDrop TCPDeferAcceptDrop IPReversePathFilter TCPTimeWaitOverflow TCPReqQFullDoCookies TCPReqQFullDrop TCPRetransFail TCPRcvCoalesce TCPOFOQueue TCPOFODrop TCPOFOMerge TCPChallengeACK TCPSYNChallenge TCPFastOpenActive TCPFastOpenActiveFail TCPFastOpenPassive TCPFastOpenPassiveFail TCPFastOpenListenOverflow TCPFastOpenCookieReqd TCPSpuriousRtxHostQueues BusyPollRxPackets TCPAutoCorking TCPFromZeroWindowAdv TCPToZeroWindowAdv TCPWantZeroWindowAdv TCPSynRetrans TCPOrigDataSent TCPHystartTrainDetect TCPHystartTrainCwnd TCPHystartDelayDetect TCPHystartDelayCwnd TCPACKSkippedSynRecv TCPACKSkippedPAWS TCPACKSkippedSeq TCPACKSkippedFinWait2 TCPACKSkippedTimeWait TCPACKSkippedChallenge TCPWinProbe TCPKeepAlive TCPMTUPFail TCPMTUPSuccess
TcpExt: 0 0 0 0 0 0 0 0 0 0 55 0 0 0 0 0 82 1 0 0 0 0 0 0 0 22682 0 407 435 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 14 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 952 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 63 563 0 0 0 0 0 0 0 0 0 0 0 281 0 0
IpExt: InNoRoutes InTruncatedPkts InMcastPkts OutMcastPkts InBcastPkts OutBcastPkts InOctets OutOctets InMcastOctets OutMcastOctets InBcastOctets OutBcastOctets InCsumErrors InNoECTPkts InECT1Pkts InECT0Pkts InCEPkts
IpExt: 0 0 28 30 6 6 176920959 1489946 2979 3059 284 284 0 148324 0 0 0
```
###snmp
**explanation:**This file holds the ASCII data needed for the IP, ICMP, TCP,and UDP management information bases for an SNMP agent  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat snmp
Ip: Forwarding DefaultTTL InReceives InHdrErrors InAddrErrors ForwDatagrams InUnknownProtos InDiscards InDelivers OutRequests OutDiscards OutNoRoutes ReasmTimeout ReasmReqds ReasmOKs ReasmFails FragOKs FragFails FragCreates
Ip: 2 64 27315 0 2 0 0 0 27313 27184 0 0 0 0 0 0 0 0 0
Icmp: InMsgs InErrors InCsumErrors InDestUnreachs InTimeExcds InParmProbs InSrcQuenchs InRedirects InEchos InEchoReps InTimestamps InTimestampReps InAddrMasks InAddrMaskReps OutMsgs OutErrors OutDestUnreachs OutTimeExcds OutParmProbs OutSrcQuenchs OutRedirects OutEchos OutEchoReps OutTimestamps OutTimestampReps OutAddrMasks OutAddrMaskReps
Icmp: 1176 0 0 0 0 0 0 0 0 1176 0 0 0 0 1191 0 15 0 0 0 0 1176 0 0 0 0 0
IcmpMsg: InType0 OutType3 OutType8
IcmpMsg: 1176 15 1176
Tcp: RtoAlgorithm RtoMin RtoMax MaxConn ActiveOpens PassiveOpens AttemptFails EstabResets CurrEstab InSegs OutSegs RetransSegs InErrs OutRsts InCsumErrors
Tcp: 1 200 120000 -1 110 0 2 2 0 24936 24754 45 0 36 0
Udp: InDatagrams NoPorts InErrors OutDatagrams RcvbufErrors SndbufErrors InCsumErrors IgnoredMulti
Udp: 1168 15 0 1203 0 0 0 6
UdpLite: InDatagrams NoPorts InErrors OutDatagrams RcvbufErrors SndbufErrors InCsumErrors IgnoredMulti
UdpLite: 0 0 0 0 0 0 0 0
```
###snmp6
**explanation:**记录IPV6协议下的snmp信息，同snmp
###netlink
**explanation:**网络链接状态信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat netlink
sk       Eth Pid    Groups   Rmem     Wmem     Dump     Locks     Drops     Inode
ffff88007a417800 0   2061   00000440 0        0        0 2        0        20587   
ffff88007880a800 0   2191   00000440 0        0        0 2        0        20988   
ffff88007974d000 0   918    00000440 0        0        0 2        0        15440   
ffff88007837c000 0   2428   00000440 0        0        0 2        0        23793   
ffff880078809800 0   2177   00000440 0        0        0 2        0        20907   
ffff88007a414800 0   2230   00000440 0        0        0 2        0        21045   
ffff880079e2f000 0   3901   00000110 0        0        0 2        0        40180   
ffff88007c89b800 0   0      00000000 0        0        0 2        0        13      
ffff8800343bc800 0   591    00000440 0        0        0 2        0        14464   
ffff8800343be000 0   1174405816 00000551 0        0        0 2        0        14769   
ffff88007768b800 0   708    00000111 0        0        0 2        0        14192   
ffff88007cb5c800 4   0      00000000 0        0        0 2        0        8809    
ffff8800766d1800 7   0      00000000 0        0        0 2        0        8752    
ffff88007cab7000 9   0      00000000 0        0        0 2        0        8732    
ffff880035714000 9   3454409777 00000000 0        0        0 2        0        9450    
ffff880035a9d000 9   1      00000001 0        0        0 2        0        9445    
ffff88007cab6000 10  0      00000000 0        0        0 2        0        7034    
ffff88007c9cf000 11  0      00000000 0        0        0 2        0        22      
ffff880078809000 15  2151   00000002 0        0        0 2        0        20772   
ffff880079be7000 15  581    00000002 0        0        0 2        0        12790   
ffff880077750800 15  1539   00000002 0        0        0 2        0        18763   
ffff880077688800 15  3927673515 00000002 0        0        0 2        0        12792   
ffff88007b1d9000 15  2772290905 00000002 0        0        0 2        0        18084   
ffff88007a539800 15  2658774851 00000002 0        0        0 2        0        15124   
ffff88007a679800 15  3449462575 00000002 0        0        0 2        0        15279   
ffff880077688000 15  3362128625 00000002 0        0        0 2        0        12791   
ffff88007a415800 15  3064462079 00000002 0        0        0 2        0        20406   
ffff880077689000 15  3452902476 00000002 0        0        0 2        0        12793   
ffff88007b1d8800 15  1443   00000002 0        0        0 2        0        17936   
ffff88007b1d8000 15  1461   00000002 0        0        0 2        0        18074   
ffff8800343bd000 15  2217805145 00000002 0        0        0 2        0        14768   
ffff88007b1da800 15  3248516844 00000002 0        0        0 2        0        18086   
ffff8800343be800 15  698    00000002 0        0        0 2        0        14874   
ffff88007a416000 15  2125   00000002 0        0        0 2        0        20567   
ffff88007a415000 15  2006   00000002 0        0        0 2        0        19931   
ffff8800343bd800 15  696    00000002 0        0        0 2        0        14695   
ffff88007880b000 15  2133   00000002 0        0        0 2        0        21002   
ffff880035a9e800 15  2164447732 00000001 0        0        0 2        0        9188    
ffff88007b1d9800 15  1894   00000002 0        0        0 2        0        19750   
ffff88007880b800 15  4164148241 00000002 0        0        0 2        0        21003   
ffff88007a538000 15  863    00000002 0        0        0 2        0        14998   
ffff880035a9f800 15  1      00000002 0        0        0 2        0        9180    
ffff88007880a000 15  2164   00000002 0        0        0 2        0        20816   
ffff88007a53a800 15  1746   00000002 0        0        0 2        0        19067   
ffff88007b1da000 15  3604806126 00000002 0        0        0 2        0        18085   
ffff88007c934800 15  0      00000000 0        0        0 2        0        15      
ffff88007c9fa800 16  0      00000000 0        0        0 2        0        30      
ffff880079be7800 16  585    00000002 0        0        0 2        0        12757   
ffff88007c9f8800 18  0      00000000 0        0        0 2        0        25      
```
###raw
**explanation:** 原始套接字信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat raw
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode ref pointer drops
   1: 00000000:0001 00000000:0000 07 00000000:00000000 00:00000000 00000000  1000        0 40488 2 ffff88007cabc700 0
```
###raw6
**explanation:**IPV6下原始套接字信息,同row信息
###route
**explanation:**记录路由信息   
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat route
Iface	Destination	Gateway 	Flags	RefCnt	Use	Metric	Mask		MTU	Window	IRTT                                                       
enp0s3	00000000	0202000A	0003	0	0	100	00000000	0	0	0                                                                           
enp0s3	0002000A	00000000	0001	0	0	100	00FFFFFF	0	0	0                                                                           
enp0s3	0000FEA9	00000000	0001	0	0	1000	0000FFFF	0	0	0                                                              
```
###fib_trie
**explanation:**路由查找数据结构(前缀树)  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat fib_trie
Main:
  +-- 0.0.0.0/0 3 0 5
     +-- 0.0.0.0/4 2 0 2
        |-- 0.0.0.0
           /0 universe UNICAST
        +-- 10.0.2.0/24 2 0 2
           +-- 10.0.2.0/28 2 0 2
              |-- 10.0.2.0
                 /32 link BROADCAST
                 /24 link UNICAST
              |-- 10.0.2.15
                 /32 host LOCAL
           |-- 10.0.2.255
              /32 link BROADCAST
     +-- 127.0.0.0/8 2 0 2
        +-- 127.0.0.0/31 1 0 0
           |-- 127.0.0.0
              /32 link BROADCAST
              /8 host LOCAL
           |-- 127.0.0.1
              /32 host LOCAL
        |-- 127.255.255.255
           /32 link BROADCAST
     |-- 169.254.0.0
        /16 link UNICAST
Local:
  +-- 0.0.0.0/0 3 0 5
     +-- 0.0.0.0/4 2 0 2
        |-- 0.0.0.0
           /0 universe UNICAST
        +-- 10.0.2.0/24 2 0 2
           +-- 10.0.2.0/28 2 0 2
              |-- 10.0.2.0
                 /32 link BROADCAST
                 /24 link UNICAST
              |-- 10.0.2.15
                 /32 host LOCAL
           |-- 10.0.2.255
              /32 link BROADCAST
     +-- 127.0.0.0/8 2 0 2
        +-- 127.0.0.0/31 1 0 0
           |-- 127.0.0.0
              /32 link BROADCAST
              /8 host LOCAL
           |-- 127.0.0.1
              /32 host LOCAL
        |-- 127.255.255.255
           /32 link BROADCAST
     |-- 169.254.0.0
        /16 link UNICAST
```
###fib_triestat
**explanation:**路由查找数据结构信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat fib_triestat 
Basic info: size of leaf: 48 bytes, size of tnode: 40 bytes.
Main:
	Aver depth:     2.75
	Max depth:      4
	Leaves:         8
	Prefixes:       10
	Internal nodes: 6
	  1: 1  2: 4  3: 1
	Pointers: 26
Null ptrs: 13
Total size: 2  kB

Counters:
---------
gets = 9112
backtracks = 0
semantic match passed = 9110
semantic match miss = 0
null node hit= 5756
skipped node resize = 0

Local:
	Aver depth:     2.75
	Max depth:      4
	Leaves:         8
	Prefixes:       10
	Internal nodes: 6
	  1: 1  2: 4  3: 1
	Pointers: 26
Null ptrs: 13
Total size: 2  kB

Counters:
---------
gets = 9112
backtracks = 0
semantic match passed = 9110
semantic match miss = 0
null node hit= 5756
skipped node resize = 0
```
###softnet_stat
**explanation:**记录了内核收包丢包信息  
第一列为该CPU所接收到的所有数据包，有些内核输出的是每秒钟接受的数据包数  
第二列为该CPU缺省queue满的时候, 所删除的包的个数，有些内核输出的是每秒钟丢掉的数据包数  
第三列表示time_squeeze, 就是说,一次的软中断的触发还不能处理完目前已经接收的数据,因而要设置下轮软中断,time_squeeze 就表示设置的次数  
最后一列，cpu冲突次数  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat softnet_stat 
00006bad 00000000 00000004 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
```
###wireless
**explanation:**记录无线网卡的相关信息  
**example:**
```bash
Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE
 face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 22
```
###xfrm_stat
**explanation:**与安全相关的一个框架  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat xfrm_stat
XfrmInError             	0
XfrmInBufferError       	0
XfrmInHdrError          	0
XfrmInNoStates          	0
XfrmInStateProtoError   	0
XfrmInStateModeError    	0
XfrmInStateSeqError     	0
XfrmInStateExpired      	0
XfrmInStateMismatch     	0
XfrmInStateInvalid      	0
XfrmInTmplMismatch      	0
XfrmInNoPols            	0
XfrmInPolBlock          	0
XfrmInPolError          	0
XfrmOutError            	0
XfrmOutBundleGenError   	0
XfrmOutBundleCheckError 	0
XfrmOutNoStates         	0
XfrmOutStateProtoError  	0
XfrmOutStateModeError   	0
XfrmOutStateSeqError    	0
XfrmOutStateExpired     	0
XfrmOutPolBlock         	0
XfrmOutPolDead          	0
XfrmOutPolError         	0
XfrmFwdHdrError         	0
XfrmOutStateInvalid     	0
XfrmAcquireError        	0
```
###if_inet6
**explanation:**查看IPV6信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat if_inet6 
00000000000000000000000000000001 01 80 10 80       lo
fe80000000000000286725bb745ce16b 02 40 20 80   enp0s3
```
###ip_mr_cache
**explanation:** 与组播相关的信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat ip6_mr_cache 
Group                            Origin                           Iif      Pkts  Bytes     Wrong  Oifs
```
###ip_mr_vif
**explanation:** 与组播相关的信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat ip_mr_vif
Interface      BytesIn  PktsIn  BytesOut PktsOut Flags Local    Remote
```
###ip6_mr_cache
**explanation:**IPV6协议中与组播相关的信息
###ip6_mr_vif
**explanation:**IPv6协议中与组播相关的信息
###rt_cache
**explanation:**路由缓存信息  
**example:**
```bash
root@weikang-VirtualBox:/proc/net# cat rt_cache 
Iface	Destination	Gateway 	Flags		RefCnt	Use	Metric	Source		MTU	Window	IRTT	TOS	HHRef	HHUptod	SpecDst                          
```
