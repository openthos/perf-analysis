## isgx_init
### sgx_init_platform:
1. 判断是否支持sgx
2. 如果CPU 有XSAVE 功能，则配置SAVE-Feature Request Mask (XFRM)的bits。并根据xfrm的配置确定ssaframesize的大小。
```c
if (boot_cpu_has(X86_FEATURE_OSXSAVE)) {
		cpuid_count(SGX_CPUID, 0x1, &eax, &ebx, &ecx, &edx);
		isgx_xfrm_mask = (((u64) edx) << 32) + (u64) ecx;
		for (i = 2; i < 64; i++) {
			cpuid_count(0x0D, i, &eax, &ebx, &ecx, &edx);
			if ((1 << i) & isgx_xfrm_mask)
				isgx_ssaframesize_tbl[i] =
					(168 + eax + ebx + PAGE_SIZE - 1) /
					PAGE_SIZE;
		}
	}
```
先通过cpuid 读取sgx secs 的ATTRIBUTES。Attributes的高64位存在ecx，edx中，为XFRM 的值。
而后，通过CPUid读取eax ：extended state feature 的bytes 长度； ebx：这个component save area offset 是多少

An enclave thread’s execution context consists of the general-purpose registers (GPRs) and the result of the XSAVE instruction (§ 2.6). Therefore, the size of the execution context depends on the requested-feature bitmap (RFBM) used by to XSAVE. All the code in an enclave uses the same RFBM, which is declared in the XFRM enclave attribute (§ 5.2.2). The number of EPC pages reserved for each SSA, specified in SSAFRAMESIZE, must 7 be large enough to fit the XSAVE output for the feature bitmap specified by XFRM.
		-- intel sgx explained

If the processor does support XSAVE, the length of the XSAVE area depends on SECS.ATTRIBUTES.XFRM. The length would be equal to what CPUID.(EAX=0DH, ECX= 0):EBX would return if XCR0 were set to XFRM. The following pseudo code illustrates how software can calculate this length using XFRM as the input parameter without modifying XCR0:
```
offset = 576;
size_last_x = 0;
For x=2 to 63
IF (XFRM[x] != 0) Then
tmp_offset = CPUID.(EAX=0DH, ECX= x):EBX[31:0];
IF (tmp_offset >= offset + size_last_x) Then
offset = tmp_offset;
size_last_x = CPUID.(EAX=0DH, ECX= x):EAX[31:0];
FI;
FI;
EndFor
return (offset + size_last_x); (* compute_xsave_size(XFRM), see “ECREATE—Create an SECS page in the Enclave
Page Cache”*)
```
table 在validate_secs中的使用：
```c
for (i = 2; i < 64; i++) {
	tmp = isgx_ssaframesize_tbl[i];
	if (((1 << i) & secs->xfrm) && (tmp > needed_ssaframesize))
		needed_ssaframesize = tmp;
}

if (!secs->ssaframesize || !needed_ssaframesize ||
		needed_ssaframesize > secs->ssaframesize)
	return -EINVAL;

```
因此这段代码写的无法解释，感觉是没写好。

之后：
通过CPUID 判断一下最大支持的enclave size。
CPUID 判断Intel SGX 能使用的物理资源。
CPUID 12x sub-leaf 从2开始可以探测EPC 的可用资源。EAX 中返回0则这个sub-leaf 无效。
EAX高12-31位是EPC 的物理地址对应的位，EBX 低20位为51:32位。最低的12位是in page offset。
类似的，ECX 的31：12 是size的31：12位，EDX 的低20位为51：32位。
```c
cpuid_count(SGX_CPUID, 0x2, &eax, &ebx, &ecx, &edx);

	/* The should be at least one EPC area or something is wrong. */
	BUG_ON((eax & 0xf) != 0x1);
	isgx_epc_base = (((u64) (ebx & 0xfffff)) << 32) +
		(u64) (eax & 0xfffff000);
	isgx_epc_size = (((u64) (edx & 0xfffff)) << 32) +
		(u64) (ecx & 0xfffff000);
```

调用ioremap_cache，EPC memory是可以cache的普通内存（和device register相比），remap到isgx_epc_mem上。

isgx_page_cache_init：
对这块物理内存以页为单位，链表的形式组织起来。
同时启动kernle sgx swap线程 kisgxswapd，其中，high 和low用来做swap的临界值，即当free page小于 low时，swap到大于high

```c
for (i = 0; i < size; i += PAGE_SIZE) {
		new_epc_page = kzalloc(sizeof(struct isgx_epc_page), GFP_KERNEL);
		if (!new_epc_page)
			goto err_freelist;
		new_epc_page->pa = start + i;

		spin_lock(&isgx_free_list_lock);
		list_add_tail(&new_epc_page->free_list, &isgx_free_list);
		isgx_nr_total_epc_pages++;
		isgx_nr_free_epc_pages++;
		spin_unlock(&isgx_free_list_lock);
	}
	isgx_nr_high_epc_pages = 2 * isgx_nr_low_epc_pages;
	kisgxswapd_tsk = kthread_run(kisgxswapd, NULL, "kisgxswapd");

```
分配workqueue 和注册dev以及power management notifier。
```c
isgx_add_page_wq = alloc_workqueue("isgx-add-page-wq", wq_flags, 1);
ret = misc_register(&isgx_dev);
ret = register_pm_notifier(&isgx_pm_notifier);
```

workqueue主要是之后在EPC add page的时候使用，pm可以在电量管理变化时操作之前创建的线程。
这就是isgx_init 的主要工作。

### pm_notifier
isgx_suspend:
杀死kisagxswapd线程。同时将Enclave都invalidate。
```
/**
 * isgx_invalidate - invalidate the enclave
 *
 * @encl:	an enclave
 *
 * Unmap TCS pages and empty the VMA list.
 */
void isgx_invalidate(struct isgx_enclave *encl)
{
	struct isgx_vma *vma;

	list_for_each_entry(vma, &encl->vma_list, vma_list)
		isgx_zap_tcs_ptes(encl, vma->vma);

	while (!list_empty(&encl->vma_list)) {
		vma = list_first_entry(&encl->vma_list, struct isgx_vma,
					vma_list);
		list_del(&vma->vma_list);
		kfree(vma);
	}
}
```
isgx_resume:
enable_sgx in CR4 同时启动内核线程。

## Dev ioctl.
```C
switch (cmd) {
	case SGX_IOC_ENCLAVE_CREATE:
		handler = isgx_ioctl_enclave_create;
		break;
	case SGX_IOC_ENCLAVE_ADD_PAGE:
		handler = isgx_ioctl_enclave_add_page;
		break;
	case SGX_IOC_ENCLAVE_INIT:
		handler = isgx_ioctl_enclave_init;
		break;
	default:
		return -EINVAL;
	}

```
### enclave create:
1. 从kernel 内存中分配SECS。
2. 从用户态将secs页内容拷贝到kenrel中。
3. 验证SECS 是否有效。
4. 从Kernel 内存中分配enclave管理结构体
5. 初始化结构体的内容以及工作队列 //page table 还是在kernel手里
```
	kref_init(&enclave->refcount);
	INIT_LIST_HEAD(&enclave->add_page_reqs);
	INIT_LIST_HEAD(&enclave->va_pages);
	INIT_LIST_HEAD(&enclave->vma_list);
	INIT_LIST_HEAD(&enclave->load_list);
	INIT_LIST_HEAD(&enclave->enclave_list);
	mutex_init(&enclave->lock);
	INIT_WORK(&enclave->add_page_work, isgx_add_page_worker);

	enclave->owner = current->group_leader;
	enclave->mm = current->mm;
	enclave->base = secs->base;
	enclave->size = secs->size;
	enclave->backing = backing;

```
6. 调用add_tgid_ctx，如果该进程（tgid）已经有了ctx，（通过全局变量isgx_tgid_ctx_list)连接所有的ctx）
则将该enclave的ctx指向这个已有的ctx，如果没有，则新建ctx，并将enclave->ctx 指向该ctx，ctx 加入全局列表中，ctx->tgid = current_tgid.
6. 分配一个EPC 中的page作为secs page。
7. 用construct_enclave_page 函数创建 version array page，并为secs page 分配version array
```
ret = construct_enclave_page(enclave, &enclave->secs_page,
				     enclave->base + enclave->size);
```
8. 创建pageinfo 结构体，调用ecrate创建enclave。
```c
ret = __ecreate((void *) &pginfo, secs_vaddr);
```
9. 在内核中找到secs->base 的vma，创建一个isgx_vma结构体将其管理起来。并将刚刚的vma 的private_data 指向enclave
10. 将enclave添加到当前线程的enclave list中。

#### construct_enclave_page
VA pages do not belong to any enclave and tracking with ETRACK isn’t necessary. 	--sdm
这是一个Version array page。
传入的参数有 enclave， 要初始化的页面的管理结构体，以及这个页面想要加载的地址。
先编历enclave 的va_pages列表，看有没有有空余va slot的va_page
```c
	list_for_each_entry(va_page, &enclave->va_pages, list) {
		va_offset = isgx_alloc_va_slot(va_page);
		if (va_offset < PAGE_SIZE)
			break;
	}
```
如果没有，则分配一个新的epc page作为va_page ,调用epa指令使其成为Version array page。同时分配一个va_page 管理结构体
```c
	if (va_offset == PAGE_SIZE) {
		va_page = kzalloc(sizeof(\*va_page), GFP_KERNEL);
		epc_page = isgx_alloc_epc_page(NULL, 0);
		vaddr = isgx_get_epc_page(epc_page);

		ret = __epa(vaddr);

		va_page->epc_page = epc_page;
		va_offset = isgx_alloc_va_slot(va_page);
		list_add(&va_page->list, &enclave->va_pages);
	}
```
最后，将这个va_slot 给entry
```c
	entry->va_page = va_page;
	entry->va_offset = va_offset;
	entry->addr = addr;
```


### isgx_ioctl_enclave_add_page
1. get_enclave 根据page的addr 找到对应的vma，并读取vma中的enclave值。升高enclave refcount的值。
2. 分配一个isgx_enclave_page结构体
3. 调用__enclave_add_page
```
ret = __enclave_add_page(enclave, page, addp, &secinfo);
```
\__enclave_add_page:
 1. 创建一个tmp_page 并将添加的页面的内容从用户空间拷贝到tmp_page
 2. 验证这个页面的secinfo是否有效，主要是页面类型不是TCS 或者REG, 页面可写不可读。同时所有reserved bit 必须是reserved bit。

 3. 如果页面类型是TCS，则还需要验证TCS（page content）的有效性。
 4. 调用construct_enclave_page将这个页的管理结构建立，并且。
 5. 判断该地址是否已经有页，如有则出错
 6. 将tmp_page 的内容拷贝到backing page。
 7. 如果是TCS，将enclave_page flag设置位TCS
 8. 将add page 请求的信息填入quque ，并将任务加入work queue.
 9. workqueue最终调用process_add_page_req 添加这个页。
 10. 将backing_page set dirty 并puting

#### process_add_page_req
1. 分配一个EPC page
2. 锁定enclave的mm_struct
3. 获取backing page
4. 调用isgx_insert_pte将pte设置好（VMA中va到epc page addr 的映射）
5. 调用do_eadd backing page作为src page，secs地址从enclave中得到，epc地址是epc page 虚拟地址
```c
ret = __eadd(&pginfo, epc_page_vaddr);
```
7. enclave->secs_child_cnt++;
8. 调用sgx_measure_page，其中调用eextend对EPC 页面的内容进行measure
9. enclave_page->epc_page = epc_page
10. 将enclave_page ->load_list 添加到enclave->load_list

### isgx_ioctl_enclave_init
1. 将sigstruct和einittoken 的内容从用户空间拷贝下来
SIGSTRUCT
EINITTOKEN 是用来判断一个enclave是否允许启动的，他是由Launch enclave来生成的。
2. 判断该enclave 是未初始化的
2. flush_work将页面全部添加
3. \__isgx_enclave_init调用einit初始化enclave。可能会因为interrupt storm导致失败，因此一共会尝试50*20次。

## kisgxswapd：
根据名字推断，kisgxswapd是sgx 中负责epc swap out的线程，线程中的逻辑简单，因此只记录主要操作的逻辑和页面管理的逻辑。
其中比较主要的操作有：
isolate_cluster和evict_cluster
### isolate_cluster

1. 首先调用isolate_enclave->isolate_ctx
进程和ctx对应的，因此一个ctx可能有多个enclave， 先通过isolate_ctx 找到一个ctx(victim)：
schedule()//？？
isolate_ctx判断全局ctx_list是否为空，为空则continue
找到第一个ctx且refcount为0，移至列表最后。返回该ctx
而后，类似得在isolate_enclave中找到一个enclave refcount 为0
释放ctx 的refcount并返回enclave
在isolate_cluster 中：
通过enclave->load_list找到可以使用的entry（page），并加入到dst列表中。返回当前enclave。
### evict_cluster

根据isolate_cluster 得到的enclave和page list dst，进行页面的换出，对dst中所有的页面，调用
1. EBLOCK
找到evma然后将entry addr对应的vma umap。分配相应内存页个数的backing page，最后对页面进行eblock
```c
pages[cnt] = isgx_get_backing_page(enclave, entry, true);
zap_vma_ptes(evma->vma, entry->addr, PAGE_SIZE);
do_eblock(entry->epc_page);
```

2. ETRACK
调用ETRACK 对secs的epc page 进行操作
```c
do_etrack(enclave->secs_page.epc_page);
```
3. EWB
对每一个列表中的page，进行EWB，将其写入到backing pages中去。因为之前在挑选enrty（isolate_cluster）时有判断，因此VA page 不会被加入，简化了EWB 流程。
4. 如果这个enclave的page 全部被swap out，则将SECS 也swap。

Swap in:
isgx_vma_fault： 当对这块内存区域读取时，发生fault
先reload SECS, 然后reload page
