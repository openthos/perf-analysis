# Goal
Allows threads of the same process to perform `mmap`, `munmap` and `pagefault` operations for **non-overlapping memory regions in parallel**.
# Problem
The root of VM scalability problems.
- Serialize operations such as mmap and munmap, which forces application developers to split their multithreaded applications into **multiprocess applications**;
	- ensuring address space operations on **non-overlapping memory regions scale perfectly.
- Detail problems:
	- Complex invariants between different parts of the virtual mamroy system. *Not a good explanation*. **And the kernel must enforce ordering on operations.**
		- The contention of data structure(the tree that preserve region of memory regions)
		- concurrent insert and delete
	- Single contended cache line become a scaling bottleneck;
	- TLB shoot down.
		- when a thread removes a region from its address space, the os must send sootdown interrupts to other processors to ensure that those processors flush translations for that region from there TLBs.
		- limit the number of cores that must be contacted to perform the shootdown.
		- tracks wich cores may have each page mappig cached int their TLBs precisely.
	- Scalable reference counters
		- do the count job in the cores and need some work every time slice to determine the true total value.
# Method:
- organizes metadata in a radix tree to avoid unnecessary **cache line movement**;
- uses a novel **memory-efficient distributed reference counting scheme** to track physical pages free and radix tree nodes no longer used.
- a new scheme to target remote TLB shootdowns and avoid them
