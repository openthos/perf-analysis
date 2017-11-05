代码在https://github.com/XingGaoY/kix

到移植完只有82599的驱动函数，已经有20k sloc了。

## ixgbe driver
当ix完成一般的cpu，内存和内存池初始化后，开始初始化网络设备

ix通过用户给出的pci号，直接查看文件`/sys/bus/pci/device`来获得pci设备信息。同时，自己维护一个`dev`结构，来保存读出的pci信息。  
而Linux中，通过注册pci设备驱动，检查pci id，得到一个`pci_dev`结构体。

早一点的ix没有使用完整的dpdk，而是只有dpdk的ixgbe驱动和部分dpdk的数据结构（`rte_eth_dev`等等），有一个简单的linux ixgbe驱动模块，仅仅完成使能pci_dev
和申请内存区域的工作。之后的初始化ixgbe的任务全部交给dune上的ix完成。dma linux中直接提供了api，我恢复了linux的实现。

之后的ix驱动完成分配一个`netdev`结构体保存网卡驱动中的函数表，有两类`netdev_ops`（mac层）, `phy_ops`（hw）。初始化dma，dcb，eeprom，注册中断号，使能
网卡，完成网卡驱动注册。

`netdev_ops`是对上的，暂时没有移植，因为和rx/tx相关，需要ix提供内存分配，内存池和numa的功能。  
但是由于一般的netdev结构是直接提供给linux网络协议栈的，有部分（比如rx hash）不存在，不能直接使用linux的结构和注册方式，我直接移植了ix的结构，由于，
没有在linux中注册，用linux的vfs和函数查询不到这个netif，之后可能需要增加一层来统一linux和ix的netdev。

`phy_ops`和硬件相关的函数，enable/reset hw，一些功能的setup和multicast，rar，vmdq, vlan等等，这一部分我与linux驱动比较了一下，基本没有变化。  
我将IXGBE_REG相关的读写操作恢复成Linux中的实现，增加了访问的原子限制，和使用`writel`写入，而不是直接向对应的内存赋值，之前ix里的相当简单粗暴，
感觉直接放到内核里不好。  

其他的改动就是将ix的部分api用linux替换，类似delay，timer，prefetch，byteorder等等。

同时，ix完全没有用到workqueue，之后再看看哪里被改掉了。

不太懂dune的实现，但是我理解的是跑在dune里的程序会获得一部分的高特权级。但是光看实现代码，驱动部分还没有用到什么系统调用，不存在什么用户态内核态的区别。  
之前做的事情主要是比较ix提供给驱动的api和linux的区别，以及了解一个网卡驱动注册到底要做什么。
```
+------------------+
|                  |
|     dev_ops      |      dpdk,ix(ixgbe_: rxtx.c)
|                  | 
|------------------|
|                  |
|      hw_ops      |      linux(ixgbe_: _common.c, _phy.c, _82599.c)
|                  |
+------------------|
```
下半部分是一个网卡的基本功能，可以说是完全没有任何修改。而`dev_ops`中的函数基本都被修改掉了。

而由于这些需要内核提供服务（内存，numa等等），准备先移植好ix的核心部分，再来管这一块。
