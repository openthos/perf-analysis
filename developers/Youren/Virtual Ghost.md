# Virtual Ghost notes.

## Motivation:
Protect application from malicious OS.

## Approach:
Leverage SVA system and SVA-OS instructions.
In SVA system, all the instruction can be checked before they execution.
### Attack deal with:  
1. Data access in Memory which include   
  a. direct access to memory     
  b. using MMU to map this memory to another address.    
  c. use the DMA and copy it.   
2. Data access through I/O    
  a. Data on the disk as file.   
  b. Data through syscall like network    
  c. mmap syscall to map   
3. Code Modification Accacks   
  a. Directly modify the code.   
  b. load a malicious program file when the apps launching.   
  c. The OS could transfer the control to an malicious signal handler.   
  d. The OS could link in a malicious version of dynamically loaded library.   
4. Interrupt Program State Attacks   
  a. The OS might read the Program State to get some sensitive information.   
  b. It can modifiy the State to redirect the apps.   
5. Attacks through System Services.   


So we can do following thing:   
1. spilt an ghost memory.monitor all access to this area.   
2. using SVA-OS protect MMU.
3. For DMA, the SVA check the instructions or IOMMU configurre operations.  
3. Using Compiler Tech to keep Control Flow Integrity.   
4. Using encryption to keep I/O and other communication secure.  
5. Keep interrupt state in SVA internal memory and provides operations to maniplulate it. 


## Problem of this approach:
1. Performance: Because only access to the ghost memory and I/O will cause large overhead, Virtual Ghost gain a lot improvement compared with previous system. However, it's still not enough for product system.     
2. All the application should match the Virtual Ghost request to leverage this system which means the application request rewrite.    
3. No Virtualization support. This is a critical problem.    
4. To enable encryption key chain, TPM is requested which is not as they claimed that no hardware support needed for Virtual Ghost.   

## Test Result
   Test Guide for SVA:
   1. Install Freebsd 9.3 on virtual machine.   
   2. clone the source code of SVA to Freebsd.   
   3. Follow the instructions on github to compile and install the kernel.   
   4. Reboot, type 3 to enter prompt mode at bootloader, then type boot svaKernel -s to enter the kernel.   
  
  Then, the kernel encounter segmentation fault on boot. Abort now for the test...   
## Misc
In this paper, there are two important related works:    
1. SVA system.   
2. Control Flow Integrity.   

The most valuable and intriguing thing of this paper is it analysis all the way to attack an application from the kernel and also show how to defeat them.     

## Survey paper list: 
Privious work about protect App from Malious OS:    
1. Use hardware page protection through a trusted hypervisor to achieve control over the operating system capabilities.     
2. SVA related paper.  
3. 
