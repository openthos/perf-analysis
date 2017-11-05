# Patch-4.4.70-rt83 分析

#### 0001-ARM-smp-Move-clear_tasks_mm_cpumask-call-to-__cpu_di.patch

```shell
diff --git a/arch/arm/kernel/smp.c b/arch/arm/kernel/smp.c
index b26361355dae..e5754e3b03c4 100644
--- a/arch/arm/kernel/smp.c
+++ b/arch/arm/kernel/smp.c
@@ -230,8 +230,6 @@ int __cpu_disable(void)
        flush_cache_louis();
        local_flush_tlb_all();

-       clear_tasks_mm_cpumask(cpu);
-
        return 0;
 }

@@ -247,6 +245,9 @@ void __cpu_die(unsigned int cpu)
                pr_err("CPU%u: cpu didn't die\n", cpu);
                return;
        }
+
+       clear_tasks_mm_cpumask(cpu);
+
        pr_notice("CPU%u: shutdown\n", cpu);

        /*
-- 
```

​	修改了smp中关于cpu的操作，将clear_tasks_mm_cpumask()的位置从\_\_cpu\_disable()函数中移到了\_\_cpu\_die()函数中。在多核arm架构、RT-kernel的机器中，将机器挂起到内存时，disable cpu时会卡住，原因是clear_tasks_mm_cpumask()函数在遍历锁的时候，使用的是一种比较松弛的调度，task_lock()函数使用spin_lock，在保持锁的过程中执行了sleep，导致死锁。在clear_tasks_mm_cpumask()函数的注释中也明确写了，只适用于已经处于offline状态的cpu。



#### 0002-rtmutex-Handle-non-enqueued-waiters-gracefully.patch

```shell
diff --git a/kernel/locking/rtmutex.c b/kernel/locking/rtmutex.c
index b066724d7a5b..e10cd0ec66fe 100644
--- a/kernel/locking/rtmutex.c
+++ b/kernel/locking/rtmutex.c
@@ -1681,7 +1681,7 @@ int rt_mutex_start_proxy_lock(struct rt_mutex *lock,
                ret = 0;
        }

-       if (unlikely(ret))
+       if (ret && rt_mutex_has_waiters(lock))
                remove_waiter(lock, waiter);

        raw_spin_unlock(&lock->wait_lock);
-- 
```

​	首先理清一下rtmutex是啥。mutex是linux同步中的互斥量，出自POSIX线程标准，用来保证一个对象的在任意时刻，最多只有一个线程能访问它。RT-mutex采用优先级继承(PI, Priority Inheritance) 的机制来解决优先级反转问题，详见Documentation/locking/rt-mutex-design.txt

​	在这个Patch中，unlikely是一个宏，这个宏在此处的用法是：

```C
#define unlikely(cond) (cond)
```

​	语义上来说这个宏相当于没用，修改之后，除了通过ret判断这个锁当前是否有线程占用，还要判断等待队列里是否有线程。



#### 0003-sparc64-use-generic-rwsem-spinlocks-rt.patch

```shell
diff --git a/arch/sparc/Kconfig b/arch/sparc/Kconfig
index 56442d2d7bbc..8c9598f534c9 100644
--- a/arch/sparc/Kconfig
+++ b/arch/sparc/Kconfig
@@ -199,12 +199,10 @@ config NR_CPUS
 source kernel/Kconfig.hz

 config RWSEM_GENERIC_SPINLOCK
-       bool
-       default y if SPARC32
+       def_bool PREEMPT_RT_FULL

 config RWSEM_XCHGADD_ALGORITHM
-       bool
-       default y if SPARC64
+       def_bool !RWSEM_GENERIC_SPINLOCK && !PREEMPT_RT_FULL

 config GENERIC_HWEIGHT
        bool
-- 
```

​	这个patch修改的是sparc架构里的Kconfig文件。分两部分看：

（1）sparc

​	全称为“可扩充处理器架构”（Scalable Processor ARChitecture），是RISC微处理器架构之一。

（2）Kconfig文件

​	当执行如make menuconfig时会出现内核的配置界面，所有配置工具都是通过读取"arch/$(ARCH)Kconfig"文件来生成配置界面。Kconfig的作用：Kconfig用来配置内核，它就是各种配置界面的源文件，内核的配置工具读取各个Kconfig文件，生成配置界面供开发人员配置内核，最后生成配置文件.config。Kconfig的语法可以参考“Documentation/kbuild/kconfig-language.txt”

​	这个patch修改的是读写信号量(R/W semaphores)相关的代码，semaphore是linux进程间通信的信号量，读写信号量将访问临界区的代码分为读者和写者，一个读写信号量可以被多个读者同时访问，或者被一个写者访问，写者访问时其它读者和写者都不能访问。放一个写了信号量API的博客：http://blog.csdn.net/zjc0888/article/details/6971915

​	Kconfig文件的语法可以直接百度，bool default y if SPARC32表示该选项是个bool值，在SPARC32环境下默认值是yes。修改后，def_bool 等同于bool default，是一个类型定义加上一个默认值的速记符号， PREEMPT_RT_FULL 表示 Fully Preemptible Kernel (RT)，在另外某一个patch中定义，留坑待补。



#### 0004-kernel-SRCU-provide-a-static-initializer.patch

​	这个patch比较大，修改了两个文件，修改了8个位置，将这个patch分成8个部分来看

（1）/include/linux/notifier.h

+ ​

```shell
@@ -6,7 +6,7 @@
  *
  *				Alan Cox <Alan.Cox@linux.org>
  */
- 
+
 #ifndef _LINUX_NOTIFIER_H
 #define _LINUX_NOTIFIER_H
 #include <linux/errno.h>
```

​	减掉的一行里有一个空格，增加的空行里没有空格，可能是某些编码或者编译对这个空格的处理有些问题？

+ ​

```shell
@@ -42,9 +42,7 @@
  * in srcu_notifier_call_chain(): no cache bounces and no memory barriers.
  * As compensation, srcu_notifier_chain_unregister() is rather expensive.
  * SRCU notifier chains should be used when the chain will be called very
- * often but notifier_blocks will seldom be removed.  Also, SRCU notifier
- * chains are slightly more difficult to use because they require special
- * runtime initialization.
+ * often but notifier_blocks will seldom be removed.
  */
 
 typedef	int (*notifier_fn_t)(struct notifier_block *nb,
```

​	此处修改了注释，去掉了一句“SRCU 事件通知链有点难用，因为它们需要在运行时进行特殊的初始化。“

​	事件通知链是内核各个子系统之间互相通知的机制，本质是一个事件处理函数的列表，每个通知链都与某个或某些事件有关，当特定的事件发生时，就调用相应的回调函数。通知链有四种类型：

​	a) 原子通知链(Atomic notifier chains)：只能在中断上下文进行，不允许阻塞；

​	b) 可阻塞通知链(Blocking notifier chains)：通过链元素的回调函数在进程上下文中运行，允许阻塞；

​	c) 原始通知链(Raw notifier chains)：对通知链元素的回调函数没有任何限制，所有锁和保护机制都由调用者维护；

​	d) SRCU通知链(SRCU notifier chains)：可阻塞通知链的一种变体。

+ ​

```shell
@@ -88,7 +86,7 @@ struct srcu_notifier_head {
 		(name)->head = NULL;		\
 	} while (0)
 
-/* srcu_notifier_heads must be initialized and cleaned up dynamically */
+/* srcu_notifier_heads must be cleaned up dynamically */
 extern void srcu_init_notifier_head(struct srcu_notifier_head *nh);
 #define srcu_cleanup_notifier_head(name)	\
 		cleanup_srcu_struct(&(name)->srcu);
```

​	这里也是修改了一处注释，修改前，SRCU事件通知链必须动态的初始化并且清零；修改后，不再需要动态初始化，只需要动态清零即可。

+ ​

```shell
@@ -101,7 +99,13 @@ extern void srcu_init_notifier_head(struct srcu_notifier_head *nh);
 		.head = NULL }
 #define RAW_NOTIFIER_INIT(name)	{				\
 		.head = NULL }
-/* srcu_notifier_heads cannot be initialized statically */
+
+#define SRCU_NOTIFIER_INIT(name, pcpu)				\
+	{							\
+		.mutex = __MUTEX_INITIALIZER(name.mutex),	\
+		.head = NULL,					\
+		.srcu = __SRCU_STRUCT_INIT(name.srcu, pcpu),	\
+	}
 
 #define ATOMIC_NOTIFIER_HEAD(name)				\
 	struct atomic_notifier_head name =			\
```

​	这处修改删除了SRCU事件通知链不能静态初始化的注释，增加了静态初始化的宏。

+ ​

```shell
@@ -113,6 +117,18 @@ extern void srcu_init_notifier_head(struct srcu_notifier_head *nh);
 	struct raw_notifier_head name =				\
 		RAW_NOTIFIER_INIT(name)
 
+#define _SRCU_NOTIFIER_HEAD(name, mod)				\
+	static DEFINE_PER_CPU(struct srcu_struct_array,		\
+			name##_head_srcu_array);		\
+	mod struct srcu_notifier_head name =			\
+			SRCU_NOTIFIER_INIT(name, name##_head_srcu_array)
+
+#define SRCU_NOTIFIER_HEAD(name)				\
+	_SRCU_NOTIFIER_HEAD(name, )
+
+#define SRCU_NOTIFIER_HEAD_STATIC(name)				\
+	_SRCU_NOTIFIER_HEAD(name, static)
+
 #ifdef __KERNEL__
 
 extern int atomic_notifier_chain_register(struct atomic_notifier_head *nh,
```

​	这里增加了SRCU事件通知链静态初始化的代码。

+ ​

```shell
@@ -182,12 +198,12 @@ static inline int notifier_to_errno(int ret)
 
 /*
  *	Declared notifiers so far. I can imagine quite a few more chains
- *	over time (eg laptop power reset chains, reboot chain (to clean 
+ *	over time (eg laptop power reset chains, reboot chain (to clean
  *	device units up), device [un]mount chain, module load/unload chain,
- *	low memory chain, screenblank chain (for plug in modular screenblankers) 
+ *	low memory chain, screenblank chain (for plug in modular screenblankers)
  *	VC switch chains (for loadable kernel svgalib VC switch helpers) etc...
  */
- 
+
 /* CPU notfiers are defined in include/linux/cpu.h. */
 
 /* netdevice notifiers are defined in include/linux/netdevice.h */
```

​	这里代码的内容没有改变。删除的行末都有一个空格，新增的行末都没有空格，和这个patch文件的第一处修改一样，可能是某些编码或者编译对这个空格的处理有些问题？



（2）/include/linux/srcu.h

+ ​

```shell
@@ -84,10 +84,10 @@ int init_srcu_struct(struct srcu_struct *sp);

 void process_srcu(struct work_struct *work);

-#define __SRCU_STRUCT_INIT(name)                                       \
+#define __SRCU_STRUCT_INIT(name, pcpu_name)                            \
        {                                                               \
                .completed = -300,                                      \
-               .per_cpu_ref = &name##_srcu_array,                      \
+               .per_cpu_ref = &pcpu_name,                              \
                .queue_lock = __SPIN_LOCK_UNLOCKED(name.queue_lock),    \
                .running = false,                                       \
                .batch_queue = RCU_BATCH_INIT(name.batch_queue),        \

-- 
```

​	这里修改的就是初始化的代码了，增加了pcpu_name这个参数。

+ ​

```shell
@@ -104,7 +104,7 @@ void process_srcu(struct work_struct *work);
  */
 #define __DEFINE_SRCU(name, is_static)                                 \
        static DEFINE_PER_CPU(struct srcu_struct_array, name##_srcu_array);\
-       is_static struct srcu_struct name = __SRCU_STRUCT_INIT(name)
+       is_static struct srcu_struct name = __SRCU_STRUCT_INIT(name, name##_srcu_array)
 #define DEFINE_SRCU(name)              __DEFINE_SRCU(name, /* not static */)
 #define DEFINE_STATIC_SRCU(name)       __DEFINE_SRCU(name, static)
```



#### 0005-ARM-OMAP2-Drop-the-concept-of-certain-power-domains-.patch





#### 0006-block-Shorten-interrupt-disabled-regions.patch

```shell
diff --git a/block/blk-core.c b/block/blk-core.c
index ef083e7a37c5..0260ed7c2f64 100644
--- a/block/blk-core.c
+++ b/block/blk-core.c
@@ -3222,7 +3222,7 @@ static void queue_unplugged(struct request_queue *q, unsigned int depth,
                blk_run_queue_async(q);
        else
                __blk_run_queue(q);
-       spin_unlock(q->queue_lock);
+       spin_unlock_irq(q->queue_lock);
 }

 static void flush_plug_callbacks(struct blk_plug *plug, bool from_schedule)
@@ -3270,7 +3270,6 @@ EXPORT_SYMBOL(blk_check_plugged);
 void blk_flush_plug_list(struct blk_plug *plug, bool from_schedule)
 {
        struct request_queue *q;
-       unsigned long flags;
        struct request *rq;
        LIST_HEAD(list);
        unsigned int depth;
@@ -3290,11 +3289,6 @@ void blk_flush_plug_list(struct blk_plug *plug, bool from_schedule)
        q = NULL;
        depth = 0;

-       /*
-        * Save and disable interrupts here, to avoid doing it for every
-        * queue lock we have to take.
-        */
-       local_irq_save(flags);
        while (!list_empty(&list)) {
                rq = list_entry_rq(list.next);
                list_del_init(&rq->queuelist);
@@ -3307,7 +3301,7 @@ void blk_flush_plug_list(struct blk_plug *plug, bool from_schedule)
                                queue_unplugged(q, depth, from_schedule);
                        q = rq->q;
                        depth = 0;
-                       spin_lock(q->queue_lock);
+                       spin_lock_irq(q->queue_lock);
                }

                /*
@@ -3334,8 +3328,6 @@ void blk_flush_plug_list(struct blk_plug *plug, bool from_schedule)
         */
        if (q)
                queue_unplugged(q, depth, from_schedule);
-
-       local_irq_restore(flags);
 }

 void blk_finish_plug(struct blk_plug *plug)
```

​	blk-core.c定义了通用块层的接口函数。

​	首先第一处修改，将spin_unlock改为spin_unlock_irq，这两个宏套了好几层，最后分别调用了\_\_raw_spin_unlock(raw_spinlock_t *lock)和\_\_raw_spin_unlock_irq(raw_spinlock_t *lock)，这两个函数的区别在于，后者增加了一句local_irq_enable()，这句代码用来打开本地处理器的中断。

​	在单核不可抢占系统中，local_irq_enable()和local_irq_disable()可以保证不会出现异步并发源，方式是通过关闭中断来进行互斥保护。

​	第二、三处修改可以合起来说，在原来的代码中使用的是local_irq_save()，local_irq_save会在关闭中断前，将处理器当前的标志位保持在一个unsigned long flags中，在调用local_irq_restore时，在将保存的flags恢复到处理器的FLAGS寄存器中。







































