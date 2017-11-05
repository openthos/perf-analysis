#Reading notes for SGXBounds
SGXB OUNDS : Memory Safety for Shielded Execution  
## key ideas
Implement Memory safety system in SGX enclave.  
Previous approach to ensure memory safety like AddressSanitizer and Intel Memory Protection Extensions cause high performance and memory overheads.  
SGXBounds try to use the SGX architectural features to implement memory safety system with lower overheads.  
The key idea is: In the SGX enclave, only lower 32 bits will be used to present program address space and leave 32 higher bits unused.  The SGX bounds use the higher bits to pointer some metadata.

##Background
### Definiation

Memory Safety  
Memory safety can be achieved by enforcing a single invariant: Memory accesses must always stay within stay within the bounds of originally intended objects.
### Movition
In SGX the previous approach do not works good.
Intel MPX will crash due to insufficient memory.
Address Sanitizer perform up to 3.1X slower than the native SGX execution.

Three consideration:
1. Memory limitation
2. application spend a considerable amount of time iterating through the elements of an array. So smartly chosen layout of metadata.
3. The enclave is linked statically, so all the code can be instrumented.

## Design
### Tagged Pointer
a 64-bit pointer contains the pointer itself in its lower 32 bits and the referent object’s upper bound in the upper 32 bits

### Pointer operations
#### Create Pointer
Global and stack-allocated variables are changed to structs.
struct xwrap {int x; void* LB}
specify_bounds(&xwrap, &xwrap.LB)
```
void* specify_bounds(void *p, void *UB):
  LBaddr = UB
  *LBaddr = p
  tagged = (UB << 32) | p
  return tagged
```
For dynamically allocated variables, the alloc function was wraped.

For pointer assign, in SGXBounds, it do not need to instrumentation since newly signed pointer will also inherit the upper bound.
#### Run-time bounds checks

SGXBounds inserts run-time bounds check before each memory access.

#### Pointer arithmetic
Only lower 32 bits will cal in Pointer arithmetic(Extract and cal then construct)

#### Typer cast
#### Function calls
Do not need to instrument this two suction


## Implementation
SGXBounds mainly include compiler support and run-time support.

Then moving AddressSanitizer and MPX into SGX enclave
## Evaluation
