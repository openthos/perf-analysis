# Reading notes for Haystack
Finding a needle in Haystack: Facebook’s photo storage

## Motivation
Normal previous filesystem is suit for facebook Photo storages due to lots of disk operations for filesystem metadata. New approach needed to meet facebook rapidly increasing photo uploads.
### Goal
The haystack targat to the use case with: written once, read often, never modified and rarely deleted.
1. High throughput and low latency
2. Fault-tolerant (for whold datacenter)
3. Cost-effective
4. Simple

## Background

### Typical Design
The Typical Design is that the browser visit the web server and the web server return the photo url. With this url, the browser visit the CDN, if the CDN miss this hit, it will request it with photo Storage.
In this Use case, the long tail effects, which is the photo storage always need to handle the request to less popular content.

Before the haystack ,the facebook use the NFS-based operations, which means a lot of metadata and disk operations to retrieve a single image.(Usually thousands of files in one directory.) Besides, it also makes impossible to cache all file metadata into memory.

## Design
### Overview
The Haystack consists of 3 core components: the haystack store, Haystack Directory and Haystack Cache.

Store store file, the Cache cache some file. With this cache, the facebook can reduce the dependency of CDN. And the Directory maintain the logical to physical mapping along with other application metadata.

Now, the sequence with haystack becames like:
1. the browser visit web server, and the web server use the Haystack directory to construct a url for each photo. The url contains several information:
 http://<CDN>/<Cache>/<Machine id>/<Logical volume, Photo>
According to this url the web browser can access the file.
### Directory
Functions:
1. provides a mapping from logical volumes to physical volumes.
2. Directory load balances writes across logical volumes and read across physical volumes
3. determines whether a photo request should be handled by the CDN or by the Cached
4. identifies those logical volumes that are read-only either because of operational reasons or because those volumes have reached their storage capacity
The directory store its information in a replicated database via PHP interface with memcached.
### Cache
The cache caches photo with two conditions:
1. the request comes directly from user but not CDN(CDN miss will usually miss the internal cache)
2. The photo is fetched from a write-enabled store machine(write-enable machine(still not fill) is popular)

### Store
Logical Volume: consists of physical volumes with replicate
Physical volume: a very large file(100 GB)

A store machine can access a photo quickly using only the id of the corresponding logical volume and the file offset at which the photo resides.

The store machine keep the physical voulme file descriptor in memory and mapping of photo ids to filesystem metadata
The store machine access the physical volume as a large file consist with superblock and needles.
needles consist photo metadata and content
#### Operations
1. Photo reads
When the phote uploads, the cookie's value is randomly assigned to photo. This can effectively eliminates attacks aimed at guessing valid urls for photo.
2. Phote write
sync appends needle images to it's physical volume files and update in-memory mappings as needed.
3. Phote delete
mark the flag in needles

#### Index file
Index file: while reboot, reconstruct all the mapping request to read whole physical volume which is not practical.
Index file is recording all the updates to volume file asynchronously. Two problem comes with asynchronously update:
1. write new photo
It's fast to update index file since check the new file from the end of volume is easy and quick. The needle will only appends to volume files.
2. delete new photo
check the delete flag while reading photo.

### Recovery from failure
a background task call pitchfork will check all the machines state.
