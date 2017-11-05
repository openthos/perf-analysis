# proc
## lkp
### interrupts
- APIC：中断控制器
- timer：系统时钟
- i8042：控制键盘和鼠标的键盘控制器
- rtc（real time clock）：CPU是不会被中断的。因为RTC存在于电子设备中，是用于追踪时间的。
- ioc0：输入/输出控制寄存器
- ens37：网卡 mac地址
- PCI-MSI：PCI总线中，MSI中断机制是一个可选机制
- vmci：VMware产品中的一个可选功能,允许虚拟机之间相互通讯
- nmi：不可屏蔽中断
- loc：本地定时器中断
- pmi：性能监控中断
- res：重安排中断
- cal：函数调用中断
- TLB：虚拟内存地址到物理内存地址的映射表，有软件TLB和硬件TLB， x86架构使用硬件TLB
- MCP：机器检查调查
```
(example)
  "interrupts.CPU0.0:IO-APIC.2-edge.timer": 0,
  "interrupts.0:IO-APIC.2-edge.timer": 0, 
  
  "interrupts.CPU0.1:IO-APIC.1-edge.i8042": 0,
  "interrupts.CPU1.1:IO-APIC.1-edge.i8042": 0,
  "interrupts.1:IO-APIC.1-edge.i8042": 0,
  "interrupts.CPU0.12:IO-APIC.12-edge.i8042": 0,
  "interrupts.CPU1.12:IO-APIC.12-edge.i8042": 0,
  "interrupts.12:IO-APIC.12-edge.i8042": 0,

  "interrupts.CPU0.8:IO-APIC.8-edge.rtc0": 0,
  "interrupts.8:IO-APIC.8-edge.rtc0": 0,

  "interrupts.CPU0.16:IO-APIC.16-fasteoi.ehci_hcd:usb1,vmwgfx": 0,
  "interrupts.CPU1.16:IO-APIC.16-fasteoi.ehci_hcd:usb1,vmwgfx": 0,
  "interrupts.16:IO-APIC.16-fasteoi.ehci_hcd:usb1,vmwgfx": 0,   //猜测为驱动

  "interrupts.CPU0.17:IO-APIC.17-fasteoi.ioc0": 0,
  "interrupts.CPU3.17:IO-APIC.17-fasteoi.ioc0": 38,
  "interrupts.17:IO-APIC.17-fasteoi.ioc0": 38,

  "interrupts.CPU0.18:IO-APIC.18-fasteoi.uhci_hcd:usb2": 0,
  "interrupts.18:IO-APIC.18-fasteoi.uhci_hcd:usb2": 0,

  "interrupts.CPU0.19:IO-APIC.19-fasteoi.snd_ens1371,ens37": 0,
  "interrupts.CPU1.19:IO-APIC.19-fasteoi.snd_ens1371,ens37": 107,
  "interrupts.19:IO-APIC.19-fasteoi.snd_ens1371,ens37": 107,

  "interrupts.CPU0.56:PCI-MSI.1114112-edge.0000:02:04.0": 0,
  "interrupts.CPU2.56:PCI-MSI.1114112-edge.0000:02:04.0": 20,
  "interrupts.56:PCI-MSI.1114112-edge.0000:02:04.0": 20,
  "interrupts.CPU0.57:PCI-MSI.129024-edge.vmw_vmci": 0,
  "interrupts.CPU1.57:PCI-MSI.129024-edge.vmw_vmci": 0,
  "interrupts.57:PCI-MSI.129024-edge.vmw_vmci": 0,
  
  ```
### proc-vmstat ：虚拟内存
```
"proc-vmstat.pgpgin": 64,//从启动到现在读入的内存页数
  "proc-vmstat.pgpgout": 820,//从启动到现在换出的内存页数
  "proc-vmstat.pgalloc_dma": 0,//从启动到现在DMA存储区分配的页数
  "proc-vmstat.pgalloc_dma32": 79733,
  "proc-vmstat.pgfree": 76095,//从启动到现在释放的页数
  "proc-vmstat.pgactivate": 18,//从启动到现在去激活的页数
  "proc-vmstat.pgfault": 86037,//从启动到现在二级页面错误数
  "proc-vmstat.pgmajfault": 1,//从启动到现在一级页面错误数
  "proc-vmstat.pageoutrun": 0,//从启动到现在通过kswapd调用来回收的页面数
  "proc-vmstat.pgrotated": 0,//从启动到现在轮换的页面数
  "proc-vmstat.thp_fault_alloc": 2,
  "proc-vmstat.thp_collapse_alloc": 0,
  "proc-vmstat.thp_split": 2,
  "proc-vmstat.nr_free_pages": 127338,
  "proc-vmstat.nr_alloc_batch": 165,
  "proc-vmstat.nr_inactive_anon": 8056,
  "proc-vmstat.nr_active_anon": 47329,
  "proc-vmstat.nr_inactive_file": 65239,
  "proc-vmstat.nr_active_file": 190240,
  "proc-vmstat.nr_anon_pages": 46789,
  "proc-vmstat.nr_mapped": 32404,
  "proc-vmstat.nr_file_pages": 264094,
  "proc-vmstat.nr_dirty": 74,//脏页数
  "proc-vmstat.nr_slab_reclaimable": 41499,
  "proc-vmstat.nr_slab_unreclaimable": 9293,
  "proc-vmstat.nr_page_table_pages": 4048,
  "proc-vmstat.nr_kernel_stack": 486,
  "proc-vmstat.nr_shmem": 8616,
  "proc-vmstat.nr_dirtied": 111,
  "proc-vmstat.nr_written": 103,
  "proc-vmstat.numa_hit": 76559,
  "proc-vmstat.numa_interleave": 0,
  "proc-vmstat.numa_local": 76559,
  "proc-vmstat.nr_anon_transparent_hugepages": 29,
  "proc-vmstat.nr_dirty_threshold": 75751,
  "proc-vmstat.nr_dirty_background_threshold": 37875,
```

### uptime 
```
 "uptime.boot": 631339.68, //统启动到现在的时间
  "uptime.idle": 2438300.75 //系统空闲的时间
```
