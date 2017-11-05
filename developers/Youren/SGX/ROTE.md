# Reading notes for ROTE
ROTE: Rollback Protection for Trusted Execution
## Key ideas
Intel SGX can only secure runtime memory, sealing prevents an untrusted OS from reading or arbitrarily modifying stored data. However, rollback attacks for stored data remains possible.
ROTE use multiple processors to assist each other. The ROTE can achieve all or nothing integrity, i.e, reset all the platforms to their initial state is the only way.

## Movitation
Treat the system as a distributed system among multiple enclaves. When an enclave updates its state, it stores a counter to a set of enclaves running on assisting processors and saves its state data on persistent storage.

### Previous approaches
1. Store the persistent state of enclave in a non-volatile memory
2. maintain integrity information for protected applications in a separate trusted server.

#### Drawback of SGX SDK Monotonic Counter
Although less documented, the author found:
1. Tooks so long 250 ms to one increment
2. after remove SGX SDK or remove BIOS will remove all counter.
3. SGX Counter service needs internet

## Design
ROTE use other platform to assist the system keep secure
