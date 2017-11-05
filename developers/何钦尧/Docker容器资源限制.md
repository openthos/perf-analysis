# Docker容器资源限制

Docker可以在启动一个容器时限制通过命令行选项来限制该容器拥有的系统资源。如有以下命令选项

```bash
--cpus=<value>			# 容器中能够使用的CPU核心数
--memory=*				# 容器中能够使用的内存总量，如128m，4g等
--memory-swap=*			# 容器中能够使用的虚拟内存(swap分区)的总量
--device-read-bps		# 容器中的某个设备的读取速率限制(byte per second)，如 /dev/sda:100mb
--device-write-bps		# 容器中的某个设备的写入速率限制(byte per second)
--device-read-iops		# 容器中某个设备的读取次数限制(IO per second)，如 /dev/sda:1000
--device-write-iops		# 容器中某个设备的写入次数限制(IO per second)
```

目前最新的Dockerb版本中尚不支持对于network的访问速率的控制。