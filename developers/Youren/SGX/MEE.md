#Reading notes for Memory Encryption Engine
A Memory Encryption Engine Suitable for General Purpose Processors
## Goal
The Goal for the Memory Encryption Engine is to keep confidentiality, data integrity and data replay prevention.

For the confidentiality it's easy to understand.
1. The MEE keys are generated uniformly at random at boot time and never leave the die.   
2. The encryption keys and the authentication keys are separate.   

What I want to mentation is the data replay prevention.   

The MEE has an integrity tree to keep the data freshness：  
Simply speaking:   
The root of the tree located in a SRAM and can only be modify by the cpu.
The memory region is separate into blocks. The first block is consist only nonces of other blocks and a TAG. The TAG is computer by the nonces and the special nonce stored in SRAM. Except first block, each block of memory have three parts: data and MAC tag. The Tag is computer by the data and nonce in first block. If you want to modify one of the block, you should update the Data, Tag and nonce in first block and SRAM.  
