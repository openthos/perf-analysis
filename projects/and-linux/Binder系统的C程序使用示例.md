# 1 概述

本文是《Android系统_binder_c程序示视频课程 韦东山》的学习笔记。

视频地址：http://edu.51cto.com/course/course_id-6595.html

源码地址：https://github.com/weidongshan/APP_0003_Binder_C_App

该教程讲解了用C语言编写 Android 系统层的 Server 和 Client ，它们基于Binder驱动完成RPC通信。


<!--more-->


# 2 IPC & RPC

## 2.1 IPC

**IPC：Inter-Process Communication，进程间通信**

IPC指进程间通信，有三大要素，发送方（源）、接收方（目的）、内容（数据）。

比如：在Binder的使用过程中，A进程请求B进程的led服务。B进程首先需要向servicemanager注册led服务，然后A进程向servicemanager查询led服务，可以获取一个代表B进程led服务的handle。

这里面的每一次通信过程都是IPC过程。

IPC三大要素：

1. **源：** A进程
2. **目的：**
    (1) B向servicemanager注册led服务
    (2) A向servicemanager查询led服务，得到一个handle
3. **数据：** char buf[512]

## 2.2 RPC

**RPC：Remote Procedure Call，远程过程（函数）调用**

RPC三大要素：

1. **调用哪个函数：** server的函数编号
2. **传给它什么参数：** 通过IPC的buf传输
3. **返回值：** 通过IPC的buf传输

A进程使用led服务的led_open/led_ctl函数是一个RPC过程，这里面包含很多次IPC通信。

```
① 封装数据                       ② 调用led_open/led_ctl
② 发送给B                        ① 取出数据
A -------------IPC-----------------> B
```

# 3 Binder系统分析

## 3.1 Binder系统框架

```
  client        servicemanager       server
    |                |                 |
    |                |                 |
+--------------------------------------------+
|             binder驱动                     |
+--------------------------------------------+
```

Binder通信过程中，至少有四个部分。

1. **servicemanager**负责管理所有的服务，包括服务注册、获取、注销。
2. **server**则表示一个服务。
3. **client**表示一个使用服务的客户端。
4. **binder**驱动用来传送数据给指定目标。

## 3.2 client执行流程

① open驱动

② 获取服务

        (1) 向servicemanager查询服务
        (2) 获得一个handle

③ 向handler发送数据

## 3.3 servicemanager执行流程

① open驱动

② 告诉驱动程序，它是“servicemanager”

③ 循环

```
while(1) {
     读取驱动数据
     调用   {
               a. 注册服务     { 在链表中记录 }
               b. 获取服务
                              {
                                 b.1 在链表中查询有无服务
                                 b.2 返回‘server进程 ’
                              }
            }
}
```

## 3.4 server执行流程

① open驱动

② 注册服务：向servicemanager发送服务名

③ 循环

```
while(1)
{
     读驱动
     解析数据
     调用对应函数
}
```

# 4 Binder系统的C语言使用示例

## 4.1 代码执行流程

程序源码在概述里说APP_0003_Binder_C_App项目，bctest是一个服务示例。

frameworks\native\cmds\servicemanager

**service_manager.c**

```
a. binder_open
b. binder_become_context_manager
c. binder_loop(bs, svcmgr_handler);
     c.1 res = ioctl(bs->fd, BINDER_WRITE_READ, &bwr);
     c.2 binder_parse
               //解析
               //处理：svcmgr_handler
                              SVC_MGR_GET_SERVICE/SVC_MGR_CHECK_SERVICE:获取服务
                              SVC_MGR_ADD_SERVICE：注册服务
               //回复
```

**bctest.c**

注册服务的过程：
```
a. binder_open
b. binder_call(bs, &msg, &reply, 0, SVC_MGR_ADD_SERVICE)
                    // 含有服务的名字
                            //含有servicemanager回复的数据
                                 // 0表示servicemanager
                                      // code：表示要调用servicemanager中的“addservice函数”
```

获取服务的过程
```
a. binder_open
b. binder_call(bs, &msg, &reply, target, SVC_MGR_CHECK_SERVICE)
                    // 含有服务的名字
                            //含有servicemanager回复的数据，表示提供服务的进程
                                    // 服务编号
                                            // code：表示要调用servicemanager中的“getservice函数”
```

binder.c （封装好的C函数，包含binder_call等）

## 4.2 binder_call 原理

binder_call 是一个远程调用过程。

```
int binder_call(struct binder_state *bs,
                         struct binder_io *msg,          //提供什么参数
                         struct binder_io *reply,          //返回值
                         uint32_t target,                    //向谁发数据
                         uint32_t code)                    //调用哪个函数
```

### 4.2.1 binder_call 内部流程

① 构造参数：放在buf[100000]，用binder_io来描述

    数据转换：binder_io => binder_write_read

② 调用ioctl发数据

```
res = ioctl(bs->fd, BINDER_WRITE_READ, &bwr);
```

bwr的类型是binder_write_read。

```
struct binder_write_read bwr;
```

binder_write_read结构体：

```
struct binder_write_read {
binder_size_t write_size;
binder_size_t write_consumed;
binder_uintptr_t write_buffer;
binder_size_t read_size;
binder_size_t read_consumed;
binder_uintptr_t read_buffer;
};
```

③ ioctl也会收数据，收到 binder_write_read

```
之后会转换为 binder_io 然后调用 binder_call
```

### 4.2.2 构造 ioctl 参数的例子

```
unsigned iodata[512/4];
struct binder_io msg, reply;

bio_init(&msg, iodata, sizeof(iodata), 4);
bio_put_uint32(&msg, 0); // strict mode header
bio_put_string16_x(&msg, SVC_MGR_NAME);
bio_put_string16_x(&msg, name);
```

根据binder_io，target，code三者，构造writebuf：

```
writebuf.cmd = BC_TRANSACTION;
writebuf.txn.target.handle = target;
writebuf.txn.code = code;
writebuf.txn.flags = 0;
writebuf.txn.data_size = msg->data - msg->data0;
writebuf.txn.offsets_size = ((char*) msg->offs) - ((char*) msg->offs0);
writebuf.txn.data.ptr.buffer = (uintptr_t)msg->data0;
writebuf.txn.data.ptr.offsets = (uintptr_t)msg->offs0;

bwr.write_size = sizeof(writebuf);
bwr.write_consumed = 0;
bwr.write_buffer = (uintptr_t) &writebuf;
```

writebuf结构体：

```
struct {
    uint32_t cmd;
    struct binder_transaction_data txn;
} __attribute__((packed)) writebuf;
```

# 5 怎么写APP

这里的 APP 的意思是一个Binder服务和一个Binder客户端。

① client

    a. binder_open
    b. 获得服务：handle
    c. 构造参数：binder_io
    d. 调用binder_call(handle, code, binder_io)
    e. 分析返回binder_io,取出返回值

② server

    a. binder_open
    b. 注册服务
    c. ioctl(读)
    d. 解析数据
          binder_write_read
                    .readbuf -> binder_transation_data {code、参数}
          e. 根据code决定调用哪个函数，参数也构造为binder_io
                    从binder_io取出参数
          f.把返回值转换为binder_io，发给client

详见 APP_0003_Binder_C_App 。
