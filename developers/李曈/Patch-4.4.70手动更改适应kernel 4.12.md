# Patch-4.4.70 手动更改适应kernel 4.12

#### 0001-ARM-smp-Move-clear_tasks_mm_cpumask-call-to-__cpu_di.patch

​	这个patch之修改了arch/arm/kernel/smp.c这一个文件，相对于kernel 4.4.70，kernel 4.12除了代码位置有6行偏移外，pr_notice()改成了pr_debug()。

```c
pr_debug("CPU%u: shutdown\n", cpu);
```

​	pr_notice()是linux/printk.h中定义的一个宏，指向printk()函数，pr_debug()是linux/printk.h中定义的另一个宏，这个宏会根据config的选择，DEBUG的开关，通过if defined的方法来动态选择指向哪个函数。



#### 0002-rtmutex-Handle-non-enqueued-waiters-gracefully.patch

​	这个patch修改了rt_mutex_start_proxy_lock()函数里的内容，相对于kernel 4.4.70，kernel 4.12消除了raw_spin_unlock()函数的重复调用，方法是增加了__rt_mutex_start_proxy_lock()函数，具体的代码内容都没变，将patch里的函数名改一下就行。



#### 0003-sparc64-use-generic-rwsem-spinlocks-rt.patch

​	这个patch在linux kernel v4.12版本中，相比于v4.4.70，只是代码位置变了10行，内容没有动。



#### 0004-kernel-SRCU-provide-a-static-initializer.patch

（1）/include/linux/notifier.h

​	这个文件里修改了6个位置的代码，但都只是代码行数有微小的变动，代码内容没变。

（2）/include/linux/srcu.h

​	这个文件在linux-4.12中进行了比较大的变动，4.12种通过ifdef判断config选项，将原本的代码分布到另外的三个文件中，三个文件里的代码比较类似，对应不同的config选项。这三个config选项分别是：

+ CONFIG_TINY_SRCU
+ CONFIG_TREE_SRCU
+ CONFIG_CLASSIC_SRCU

​	其中CONFIG_CLASSIC_SRCU和linux-4.4.70中的srcu.h一样，另外两个则是新增加的，相应的宏代码也不一样。目前三个config选项对应的文件之修改了第三个，前两个还不知道该怎么改，需要了解代码的语义才能修改。**留坑待补**





































