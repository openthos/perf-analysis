# Symbolic Execution
- [KLEE: Unassisted and automatic generation of high-coverage tests for complex systems programs](http://vglab.cse.iitd.ernet.in/~sbansal/csl865/readings/klee-osdi-08.pdf)  
``这篇文章谈到具体的se内容不多，对于入门理解se的意义似乎不大``
- [EXE: Automatically generating inputs of death](http://web2.cs.columbia.edu/~junfeng/10fa-e6998/papers/exe.pdf)
- [SAGE: Whitebox Fussing for security testing](http://delivery.acm.org/10.1145/2100000/2094081/p20-godefroid.pdf?ip=101.5.242.74&id=2094081&acc=OPEN&key=BF85BBA5741FDC6E%2E587F3204F5B62A59%2E4D4702B0C3E38B35%2E6D218144511F3437&CFID=926132909&CFTOKEN=12819413&__acm__=1492677015_1b1345eccd61661643936fe2079082ff)

# Concolic testers
- [DART:Directed automated random testing](https://wkr.io/public/ref/godefroid2005dart.pdf)
``这篇文章是xiw的mini-mc的原理，对于concolic的实现给出了比较具体的定义和实现过程。不过其中的testgen和commuter的很不一样，读一下里面的定义和伪代码对于理解concolic还是很有用的。``
- [CUTE: A concolic unit testing engine for C](http://delivery.acm.org/10.1145/1090000/1081750/p263-sen.pdf?ip=101.5.242.74&id=1081750&acc=ACTIVE%20SERVICE&key=BF85BBA5741FDC6E%2E587F3204F5B62A59%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&CFID=926132909&CFTOKEN=12819413&__acm__=1492677212_ca86dca9561b2f0556bf397a6258e28c)
