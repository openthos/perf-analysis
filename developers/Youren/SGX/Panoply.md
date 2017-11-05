# Reading notes of Panoply  
PANOPLY: Low-TCB Linux Applications with SGX Enclaves  

## Motivation  
Support POSIX application with minimal TCB on SGX enclaves.
POSIX like multi-process and multi-threads.
## Approach
Microns as
1. POSIX import an slim lib.
2. Reuse some function like schedule in kernel rather than in enclave.
3. SGX awareness by separating application to micros by simple annotations
