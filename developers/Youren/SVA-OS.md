Reading notes for SVA-OS.
=========================

#### Memory Safety for Low level Software/Hardware Interactions.

---

Motivation: 1. All the previous memory safety system did not consider the low-level interactions between an OS kernel and hardware.

Problems:
---------

### Definiation and Goal:

type-safe program: all operations respect the types of their operands. Memory-safety: every memory access uses a previously initialized pointer variable; accesses the same object to which the pointer pointed initially; and the object has not been deallocated.

### The cause of Voilation and its solutions.

How to breaking Memory Safety with low-level Kernel Operations. 1. Corrupting Processor State: The kernel must protect the processor register; sometimes the Kernel save the Processor States in Memory and will modifity it in some case.

1.	Corrupting Stack State:  
	a. Stack should only be used for stack frames and can not be modified.  
	b. The memory for the stack must not be deallocated and reused for other memory objects.  
	c. A context switch must switch to a stack.  
	d. after deallocated, all pointer to the stack/local variables should be dereferenced.

2.	Corrupting Memory-Mapped I/O

3.	Corrupting Code  
	a. Self-modifying Code.  
	b. Incorrect program loading

4.	General Memory Corruption with privilege operations.  
	a. MMU configuration. An error memory mapping.  
	b. Page swapping. If it's not at the same place between out and in.  
	c. DMA. May overwrite data or fresh data is corrupted.

To deal with those Voilations, it's easy to give a general design principles.  
1. Processor State:  
 a. The systems should not provides such low-level api to change the register in CPU.  
 b. The verifier should save the processor state in a special memory and only allowed special API access.  
 c. To modifiy the processor state for some reason like signal handler dispatch  
2. Memory-mapped I/O:  
 a. All I/O object allocations be identifiable in the kernel code.  
 b. All access to I/O can only use special I/O instructions.  
 c. The memory from I/O should be marked as type-unsafe.

1.	Kernel Code:  
	a. a section of code can only be enabled and disabled by the Verifier. b. Instruction cache
2.	General Memory Corruption:  
	a. MMU configuration  
	b. Page swapping c. DMA.
3.	Entry Points:  
	a. For CFI, all handler of interrupt, trap and syscall are the initial address of a valid function.  

Related Backgound
-----------------

###Self-modifying code
