本周工作进展和下周计划

2017.02.27~2017.03.03

- 本周工作计划点1: Read the paper related to SVA.

- 完成情况：Extreamly interesting about Virtual Ghost.

- 本周工作计划点2: Read the three paper on OSDI about SGX

- 完成情况： Not good as I planed.

Virtual Ghost can described briefly as following:
Motivation: Protect application from malicious OS.
Approach: Leverage SVA and SVA-OS system.
1. spilt an ghost memory.monitor all access to this area.
2. using SVA-OS protect MMU and something like interrupt state.
3. Using Compiler Tech to keep Control Flow Integrity.
4. Using encryption to keep I/O and other communication secure.

Problem of this approach:
1. Performance: Because only access to the ghost memory and I/O will cause large overhead, Virtual Ghost gain a lot improvement compared with previous system. However, it's still not enough for product system.
2. All the application should match the Virtual Ghost request to leverage this system which means the application request rewrite.
3. No Virtualization support. This is a critical problem.  
4. To enable encryption key chain, TPM is requested which is not as they claimed that no hardware support needed for Virtual Ghost.

SGX analysis:
Background:
With SGX, the CPU can split some memory as enclaves. All the access to enclaves will be checked by hardware. Before able to access the enclave, the process should entry the enclave by Instruction EENTER and vise versa with EEXIT.
1. Haven:
Approach:
Reuse the Drawbridge. Secure the whole LibOS with enclave.. Like describe in Drawbridge, the LibOS include the applications, Virtual memory and file system. To support Haven, the threads and scheduling is also included in LibOS to.
2. SCONE:
To secure Cloud, do not need to keep the kernel safe. The kernel might be comprised by some vulnerability but the other application do not be infected.


Problem of SGX:
1. Overhead: Basically, the overhead of SGX is just like virtual ghost in some extends.
2. Size: Only 64MB or 128MB enclaves supported for whole system. If the enclaves fulls, swaps the enclaves needs encryption which cost CPU cycles.
3. No privilege instruction allowed in enclave, which cause a lot of overhead if the system needs to do so. But the C library has to be included in the enclave to keep application secure.

- 下周计划：
	1. Rethink all the approach about SGX, where I can improve and what's missing.


- 其他事宜：
	2. Should complete the questions from the suggestion below.


```
chy: 第一周
SVA的相关论文有哪些？这个领域是啥？是否有相关综述？
希望看到一个文档，列出了相关的论文名称，列表，可以放到
https://github.com/openthos/research-analysis/tree/master/developers/%E6%B2%88%E6%B8%B8%E4%BA%BA
```

```
chy: 第二周
上周我提出的问题好像没看到解答。 你写的论文阅读报告可进一步清晰和深入，我觉得如可能，需要实验一下，并对照论文再阅读，比如你说性能是问题，具体测试情况如何。
对于你的想法，建议对一个潜在研究方向，建立一个单独的文件进行撰写。重点论文，需要自己尽量理解清楚，了解相关领域研究现状，并能够给大家清晰的讲解（这一点，在我听到的两次你面向大家的汇报中，觉得还有很大提升空间）。

建议看看 MIT的Sanctum : minimal architectural extensions for isolated execution ，并与SGX对比一下。

对于对于论文阅读报告，请写到单独的文档中，一篇论文一个报告。建议写出：

– Summary of major innovations
– What the problems the paper mentioned?
– How about the important related works/papers?
– What are some intriguing aspects of the paper?
– How to test/compare/analyze the results?
– How can the research be improved?
– If you write this paper, then how would you do?
– Did you test the results by yourself? If so, What’s your test Results?
– Give the survey paper list in the same area of the paper your reading.

建议本周能够给大家汇报一次  Virtual Ghost 或 SGX，最好结合实际的实验。

```