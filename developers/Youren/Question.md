1. SGX 能否访问普通内存，SGX 如何使用seal key 将内容保存到磁盘上 为什么要用seal key
SGX 可以直接访问普通内存。 Seal key 分两种，一种是enclave 的key，一种是enclave author的key。encalve author 的key可以保证同一个platform 中的同一个人写的不同enclave 之间key共享。不同的CPU 之间的key 不能共享，于此同时，可以将seal key 通过remote attestation后建立的secure session 将key 发送给可信的远端 server。
2. SGX 能否修改自己的内容。
Code 不能，stack 和heap 可以。
3. SGX 中Glibc 等library是如何保存，如何调用的。
SGX 中每个enclave 都只能有静态链接的库。
4. TCS最多能有多少个，如何负责调度
TCS 的调度
5. Trampoline 在Interrupt 或 Exception之间的过渡是什么。

6. SGX 中page fault 如何避免信息泄漏？
SGX 中AEX发现退出原因是PF，会自动将CR2后12位清除。

7. SGXKernel 如何实现抢占式调度？
传统的OS thread感知不到interrupt的发生，但是Enclave可以通过AEX 和SSA 知道自己因为中断跳出了enclave过。
同时，AEX跳出Enclave后执行的代码是AEP指向的代码，即由Enclave指定的，可以将AEP指向的区域中加入Scheduler代码。
