# Reading notes for Eleos
Eleos: ExitLess OS Services for SGX Enclaves

## Movitation
As we discussed in SCONE before, the SGX has a heavy hardware limitation, that is:
1. Memory limitation
2. Can only run in Uer mode, to call syscall, Enclave exit operation is required
To analysis why this two limitation will cause performance overhead, the author give an more detailed performance test than SCONE.
In this paper, the author use two approaches to reduce the performance overheads:
### what performance overheads
#### Cost of system call.
##### Direct costs
EEXIT and EENTER

##### Indirect cost
1. The cost of LLC pollution.
2. The cost of TLB flushes.

#### Cost of EPC page faults
Since the memory in EPC are limited to 128 MB, to support oversize application, the kernel driver implement swap mechanism for SGX applications. In this situation, the EPC page faults will introduce new overheads.

## Design
Now we know the overhead in SGX mainly comes from system call and page fault, the Eleos trying to improve the performance from them:
1. RPC for system call
2. Secure user-managed virtual memory
The system call is easy to understand. note that it also use the poll.
### Secure user-managed virtual memory
Retrofit the ActivePointers approach in GPUs.
1. program alloc memory by calling suvm_malloc function.
