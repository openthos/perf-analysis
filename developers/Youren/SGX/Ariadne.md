# Reading notes for Ariadne
Ariadne: A Minimal Approach to State Continuity
## Key idea
The SGX only can secure the system during running, which explore the storage system under the risk of rollback attack.
In this paper, the author trying to secure the system with the help of TPM or ME when SGX is down.
Besides, the system can
1. protect the secure module(Intel SGX) from rollback attack
2. Once the input is accept, the system will finished it.
3. the lost of power will never cause the system unrecoverable. (Liveness property)
I.e. state Continuity.
## Definiation
Protected-module:
The author define(abstract) the Intel sgx as two function:
1. Key derivation
2. Isolation mechanism

## Key idea to prevent attack:
Increment the number when save a package and increment the counter twice when load back a package.
Increment only once is not enough because there maybe a lot package with counter + 1 on the system(The attack may crash the system when the package generated but the counter didn't increment).

To prevent the system crash from when update the Monotonic counter, an atomic  counter number generate mechanism is needed. The author use the gray code to achieve single bit flipping mechanism.
