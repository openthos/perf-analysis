#The reading notes for Ryoan
Ryoan: A Distributed Sandbox for Untrusted Computation on Secret Data
##Key ideas
This paper is driven by special needs in real world(?) When we use the cloud to provide data-processing with our secret data like tax, we want that no one cat steal out data.

##Thread model
There is four parts in this model:
1. Service Provider
2. Platform Provider
3. User

The user can't trust any software in the computational platform

Ryoan do not prevent each party from leaking it's own secrets and do not prevent DOS attack
