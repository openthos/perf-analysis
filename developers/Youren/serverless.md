
What is serverless
serverless 是一种新的云处理架构，其基本思想是将server的逻辑分为 stateless的Functions，developer不再需要考虑platform。Serverless的主要平台有AWS lambda， google Cloud functions 和Azure Function。

Serverless definitions
AWS对 lambda 的定义是：AWS Lambda lets you run code without provisioning or managing servers. (1) ... With Lambda, you can run code for virtually any type of application or backend service (2) - all with zero administration. Just upload your code and Lambda takes care of everything required to run (3) and scale (4) your code with high availability. You can set up your code to automatically trigger from other AWS services (5) or call it directly from any web or mobile app (6).
1. FaaS 是让你的back end code不需要管理服务器或者自己的server application就可以运行。
2. 不需要你提供一个特殊的框架或者库，任何的可以最后编译成Unix的process的程序都可以运行
3. 因为没server application 来部署程序，所以developer只需将代码上传给Cloud provider即可。
4. scaling 是完全自动的，弹性的，由provider 来管理。
5. Function in Faas 是被provider 的其他的event触发。
6. 大多数provider 同时提供function 被http require 触发的机制。


Serverless 是Stateless的，应该假定之前的任何调用都不对之后的调用照成影响。

Serverless的执行时间通常有限制，AWS 现在限制在5分钟，超过就会终止执行
Startup Latency也是serverless的一个重要指标，目前可能是10ms到2分钟之间。通常javascript是10ms -100ms之间，JVA 需要10秒来启动。

通常serverless的服务中都有一个API gateway，转发http 请求，调用function。

目前大部分的serverless架构都没有开源，除了IBM 的openwhisk和一个open lambda。
目前来看，serverless 的架构都是基于docker container的，但是对于用户来说，serverless 和container 还是有区别的。FaaS 的scaling 是完全自动的。Container 还是需要考虑多少个。

Where and when this word serverless come

Serverless benefit
Serverless可以带来的好处包括：
1. 降低操作成本（Operational cost）
2. 降低部署成本
3. scaling cost
Occasional request
4. 优化的效果变得更好（因为只有你的运行时间考虑在内）
5. 降低打包和部署成本
Serverless drawback
1. Vendor control 厂商对功能的限制
2. Multitenancy problem 多个客户都在同一个物理机上，可能会有secure，robustness，performance问题
3. Vendor lock-in
4. Security concerns

5. Repetition of logic across client platforms
Server-side不会有跨Function的逻辑，这些都实现在Client端。
同时，Server端的一些优化也没有办法做了。

实现上的drawback
Configuration不存在了
AWS 对同时执行的Lambda有数量上的限制，这个限制也更小。
执行时间和启动延迟。
测试更加的困难。

Open lambda
理论上来说，cloud中的层次应该是原来越少的，但是为了安全考虑，其实是越做越多了。
Lambda 比Container要慢的多。
因此，为了能够降低一些开销，AWS 会将执行的container 在不同的实例中重用：
https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
即使有上面的优化，在小的request 时lambda还是比container慢。
当lambda的container 没有任务运行时，就可以将container paused，但是这个操作速度快，不减少内存占用。

Load Balancer 也是lambda 需要考虑的一个问题。

SGX feature

Serverless + SGX
首先，FaaS 作为一个云计算的模式，能够被SGX secure本身就是一个不错的工作。
同时，可以改变已有的thread model。既然Function

microservices with unikernel

Why unikernel?
Improved security properties — as unikernels contain no unnecessary code deployed, the application’s attack surface is dramatically reduced.
Smaller footprints — unikernel code bases are typically several orders of magnitude smaller than their traditional equivalents and they can be managed much more easily.
Fine-grained optimization — as unikernels are constructed through a coherent compiler tool-chain, whole-system optimization can be carried out across device drivers and application logic, potentially improving specialisation further.
Fast boot times — as unikernels can boot in less than a second, provisioning can become highly dynamic.

Docker with serverless



https://zhuanlan.zhihu.com/p/20297696

https://yq.aliyun.com/articles/60966?spm=5176.100244.teamhomeleft.1.Gf1Uwa

Serverless with IoT and edge computing


https://martinfowler.com/articles/serverless.html
User case:
使用lambda处理大数据

lambda近乎无限扩容的能力使得我们可以很轻松地进行大容量数据的map/reduce。你可以使用一个lambda函数分派数据给另一个lambda函数，使其执行成千上万个相同的实例。假设在你的S3里存放着过去一年间每小时一份的日志文件，为做security audit，你需要从中找出非正常访问的日志并聚合。如果使用lambda，你可以把访问高峰期（7am-11pm）每两小时的日志，或者访问低谷期每四小时的日志交给一个lambda函数处理，处理结果存入dynamodb。这样会同时运行近千个lambda函数（24 x 365 / 10），在不到一分钟的时间内完成整个工作。同样的事情交给EC2去做的话，单单为这些instance配置网络就让人头疼：instance的数量可能已经超出了子网中剩余IP地址的数量（比如，你的VPC使用了24位掩码）。

同时，这样一个量级的处理所需的花费几乎可以忽略不计。而EC2不足一小时按一小时计费，上千台t2.small运行一小时的花费约等于26美金，相当可观。

JAWS和server-less architecture

两三个月前，我介绍了JAWS，当时它是一个利用aws刚刚推出的API gateway和lambda配合，来提供REST API的工具，如果辅以架设在S3上的静态资源，可以打造一个完全不依赖EC2的网站。这个项目从另一个角度诠释了lambda的巨大威力，所以demo一出炉，就获得了一两千的github star。如今JAWS羽翼臻至丰满，推出了尚处在beta的jaws fraemwork v1版本：jaws-framework/JAWS · GitHub，并且在re:invent 2015上做了相当精彩的主题演讲（见github）。JAWS framework大量使用API gateway，cloudformation和lambda来提供serverless architecture，值得关注。
