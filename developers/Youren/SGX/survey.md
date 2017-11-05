#SGX-related summary

目前来看，SGX 相关的论文主要可以分为以下几种用途：
1. 分布式系统中使用SGX
2. SGX 本身的用处，提高security，支持某些服务
3. 针对SGX的一些限制，提出的解决方法
4. 对SGX 内部的code 的正确性提出保障。

其中，第一点我了解的比较少，第二点主要是Haven，SCONE， 和Ryoan。
第三点包括Ariadne和ROTE，针对SGX只能保证运行时的freshness，Ariadne提出了希望能够实现状态的连续，即除了roll back攻击，还能够保证系统在任何时候crash都可以恢复到最新保存的状态运行。Ariadne的实现基于非易失性存储的Monotonic counter，该Monotonic Counter 可能来源于TPM 或Intel ME。实际上，Intel SDK 中的Platform Enclave也可以提供给其他的Application Enclave Counter。
Panoply系统针对SGX enclave的兼容性，希望能够在Enlcave中运行兼容Posix的程序。
Eleos针对SGX的硬件限制，包括内存大小和系统调用需要退出enclave等，导致的性能问题，提出了RPC syscall和SUVM（用户态的page 机制。
第四点是针对SGX 内部的code 实际上也可能有bug，SGXBounds发现现有的memory safety 机制在SGX 中难以直接使用，所以依赖于SGX 中的内存地址只有32位，实现了性能可以容忍的memory safety方案。

以上可以看出，sgx 目前的工作中并不是一定要有很巧的user case才能作出contribution。

# brief summary and comments of SGX

事实上，Intel SGX的功能主要包括三个部分，即：
1. 内存隔离
2. 内存加密
3. attestation and launch control
前两者基于硬件，而最后的部分因为过于复杂，因此作为一种policy，这个部分是基于软件实现的，即SDK所提供的platform service。还有一部分CPU核心中为这些功能所提供的指令因为涉及到微指令，因此并没有公开的资料。

前两者的实现可以参考Intel的文章 《A Memory Encryption Engine Suitable for General Purpose Processors》或我的总结, 后者可以看目录下的SDK analysis一点点分析。
