# Reading notes for Haven

Haven is the first system using SGX, so it's the entry for me to understand the mechanism about sgx.

## Motivation

Protect Application from cloud by using hardware on x86.

## Goal:

Confidentiality: The execution of the shielded program appears as a black box to the rest of the system. Only its input and output are observable.
Integrity: The system cannot affect the behavior o the program, except by choosing not to execute it at all or withholding resources.

## Background/SGX

SGX is the intel Secure Guard eXtension.

### Memory protection

The secure zone is called enclave. Then enclave data is protected by CPU access control(The TLB). SGX mediates page mappings at enclave setup and maintains shadow state for each page. The OS allocate the page for enclave from Enclave page cache(EPC). On each page access, the processor will check page table, enclave mode, the page blongs to EPC and is *correctly typed*. Due to the limition of EPC, the processor will flush the content to an encrypted buffer in main memory like swap for normal memory.

### Attestation

#### What's attestation

Attestation is a mechanism for software to prove its identity to remote computer.

#### SGX's attestation

SGX support CPU-based attestation. For the purpose of attestation, It will be explained in the deployment of Haven application.

### Enclave entry and exit

SGX mediate transitions into and out of the enclaves and protects the enclave's register file from OS exception handlers by thread control structure(TCS).

### Dynamic memory allocation

Using EADD to add a page and before EACCEPT execute, the page still remain unaccessible.

## Design of Haven

The Haven system is built on drawbridge with a new shield module. Compared with drawbridge, the shield module implement some typical kernel function like threads, virtual memory management, and file system. In the drawbridge, those part is in the host kernel.

### Architecture

The Haven can be consist with five parts:
1. Unmodified Applications
2. Library OS
3. Shield module
4. Untrusted runtime
The shield module can give the library OS essential support so it do not need to exit the enclave. To keep the shield module secure, it will not trusted the runtime of downcall and upcall, reference to Iago attacks. About the denial of service, it will terminate its process but do not allow the host to access the enclave.  
The interface should be easy to verify the correctness of it for the shield module. As a result, only 22 operations is designed rather then 40s.

#### Shield services

1. Virtual memory  
2. Storage/Filesystem  
3. Threads and synchronisation  
4. Miscellaneous.

Fork is not supported.

## Implementation

### How to deployment an application of the Haven.

User <---> Cloud
1. The User constructs a disk image with applications and LibOS, encrypts it and keep the key. Then send this VHD(LibOS, app and data) and shield to the cloud. The shield is not encrypted. After the shield is loaded, the SGX hardware provide attestation mechanism to measure the code and initial state.
After this, the shield generate public/private key to communicate with user, using the attestation mechanism to proving it's secure with the public key. If the user checked as OK, the user will send the key of VHD encrypts with the public key to shield. The shield receive and use the key of VHD to extract the VHD.


## Problems:
Thread module -- No fork supported in LibOS.

### Reference
https://software.intel.com/en-us/articles/innovative-technology-for-cpu-based-attestation-and-sealing
https://software.intel.com/en-us/articles/intel-software-guard-extensions-tutorial-part-1-foundation
