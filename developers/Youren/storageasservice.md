# MOTE
Storage as Service 是指云服务商提供给用户存储空间，通过Restful API，用户可以不管任何平台，直接存取自己的文件。同时，Storage as Service还具有一定的共享文件的功能。
主流的Storage as Service 服务提供商有Amazon S3， Aliyun OSS 和七牛云存储
## Storage as Service开发流程
通常，Storage as Service 的开发中可以有三个角色：
1. Cloud Platform provider
2. Service develop
3. User
Cloud Platform provider会提供一对secret id 和key 给自己的租户，而自己的租户通过这个pair访问云端的文件。为了能够实现访问该机器，同时实现一定的权限隔离，通常需要有一个service 运行，进行用户的权限验证。如果用户登陆成功，Service 会返回给用户这个pair 去访问Cloud，或者生成一个临时的key pair。
对于User来说，往往service 是可以信任的，因为这个service 是自己开发或委托他人开发，可以运行在自己所信任的机器上。但是cloud 是不可信的。同时，service 可以实现attestation，避免每个用户都要attestation。
因此，将SGX 放在Storage as service上是有必要的且可行的，接下来的问题就是，在apply的过程中可能会遇到什么问题，能够有什么contribution.
## Challenge
1. 多租户问题

2. 分布式存储问题
做Storage as service必须要能够支持分布式存储，也就是需要能够防止数据的丢失

3. Rollback attack
既然是在分布式存储的环境下，那么，enclave 之间可以互相的进行协助。
能否有一个counter，借助分布式一致性协议或者比特币的特性，能够多机共享。除非攻击者将所有机器上的数据清空，否则无法进行rollback 攻击
