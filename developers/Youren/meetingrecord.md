

2017-04-24
田洪亮提到的三个点：
1. file system 的安全目前还没有人做，sgx 是runtime 的，而filesystem最后是要存储的，没法保证交给OS 的存储确实完成了 这个工作已经有人做了，security'16 Ariadne
2. JVM 等在SGX 中的支持
3. SGX 对Unikernel的移植。

我觉得
serverless是一个SGX 未来可以做的use case，为了支持这个use case，也许需要替换掉container + VM 的软件栈
共同讨论的一些东西：
只是证明sgx 内部的tcb没有bug（形式化验证），在SGX的新环境下，是否会有新的需求，简化已有的工作。

陈老师的意见：

1. 看看serverless相关的论文
2. serverless 的问题究竟是什么，安全还是performance
3. 为了找出问题，多做一些测试

SGX 现有的限制未必是合理的，如何改善？
另一方面，抓住SGX 的本质，突破他本来的用法。
