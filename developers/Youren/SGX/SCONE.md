# Reading notes of SCONE
SCONE: Secure Linux containers with Intel SGX

## Main contribution
This paper has two main contribution
1. Detailed analysis the overhead of SGX and the security properties.
2. Designed a new architecture to run the containers on SGX.

## Performance overhead of SGX
1. threads must exit the enclave to execute system call. This produce a series of chekcs and updates include TLB flush.
2. Enclave code pays a penalty for memory writes and cache misses beacuse the on-chip memory encryption engine must encrypt and decrypt cache lines.
3. Application with memory requirements exceeding the size of the EPC must swap the EPC page to DRAM, which cost overhead in encryption.

## Design
### Design consideration
1. The security properties(The TCB and the exposed interface)
2. The performance impact due to SGX. Which include system call overhead and memory access overhead.


### Three Shield to secure External interface
There are two goal to achieve:
1. Preventing low-level attacks
2. Ensuring the confidentiality and integrity of the application data passed through the OS.

To gain this goal, there are three shields in the enclave at SCONE, which is:
1. File system shield   
which support transparent encryption of files
2. Network shield   
which support transparent encryption of network via TLS. The private key of the network is store at files so it's actually rely on the file system shield.
3. Console shield   
which support transparent encryption of console streams by splitting console streams into variable-sized blocks and encrypts the blcoks.

### Threading model
SCONE support M:N threading model in one process. Which means the M application thread response to N thread in kernel.  
The N (number of OS thread in kernel) is bound to the number of CPU to utilize the compute resources.  
This thread model will benefit the asynchronous system call mechanism we describe later.  

### Asynchronous system call
when an thread in enclave invoke an syscall, which is not the instruction, but using the slim C library, the syscall parameter is copied to the syscall slot aside of the enclave.  Then In the kernel meantime, there two lock-free queues response to receive and response queue, and a kernel thread in SCONE kernel module, will detect the system call and read the parameter from the receive queue. After handle the system call, the response will write to the response queue and the application thread will read from it.   
During the handling syscall in kernel thread, the system call response application will sleep until the syscall handler finished.

### Drawback of SCONE
rebuild image is required.
