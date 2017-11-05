# [Panappticon](（http://ziyang.eecs.umich.edu/projects/panappticon/）)重现工作

##### 1.Clone this repository and checkout the branch for your desired version of Android

```
git clone https://github.com/EmbeddedAtUM/panappticon.git
git checkout panappticon-tuna-4.1.2_r1
git submodule update --remote
```

##### 2.Replace the framework/base and libcore directories of your Android source tree with the corresponding directories in this repository.

###### 2.1 在用户目录下，创建*bin*文件夹，用于存放repo，并把该路径设置到环境变量中去

```
$ mkdir ~/bin  
$ PATH=~/bin:$PATH  
```

###### 2.2 下载repo工具

```
$ curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo  
$ chmod a+x ~/bin/repo  
```

###### 2.3 创建本地保存Android源码目录

```
$ mkdir ANDROID_SOURCE4.1.2  
$ cd ANDROID_SOURCE4.1.2
```

###### 2.4 通过以下命令进行初始化，其中最后一个参数是从上一个网址中自己根据相应版本获取的Branches名称

```
$ repo init -u git://mirrors.ustc.edu.cn/aosp/platform/manifest -b android-4.1.2_r1 
```

###### 2.5 同步源码树

```
$ repo sync
```

###### 2.6 用panappticon仓库中的framewor/base和libcore替换Android4.1.2源码中的同名文件夹

##### 3.Compile the kernel and replace the provided kernel image in your Android source tree（[参考](http://blog.sina.com.cn/s/blog_abc7e49a01011xlk.html)）

###### 3.1下载crosscompiler  180 server: ~/sdk/arm-eabi-4.6.tar.gz

```
scp lh@192.168.0.180:~/sdk/arm-eabi-4.6.tar.gz /home/ll
tar -xzvf arm-eabi-4.6.tar.gz
export PATH=$PATH:arm-eabi-4.6/bin
```

###### 3.2进入到内核源码目录

```
cd mygit/panappticon/kernel/panappticon-kernel/
```

###### 3.3创建一个linux_out目录存放编译生成的文件(**最好在上一级目录**)

```
mkdir linux_out
```

###### 3.4清除所有上次编译产生的文件和.config文件

```
make mrproper  O=./linux_out   
```

###### 3.5使用arch/arm/configs/versatile_defconfig文件的配置，versatile_defconfig的内容将被copy到.config中。.config文件是将用户选好的编译选项保存下来，make时读取.config中的选项来编译kernel。注意：必须指定ARCH=arm，否则make会到arch/i386/configs下去找versatile_defconfig。正如前面2.ARCH中所述不指定ARCH的话，将使用本机（i386）的ARCH作为缺省ARCH。

```
make ARCH=arm  O=./linux_out  versatile_defconfig
```

###### 3.6启动图形界面来作手工配置刚此生成的.config文件。此处也必须指定ARCH＝arm，否则不会load刚才生成的ARCH=arm的.config.修改配置后保存退出，此处不做修改

```
make ARCH=arm  O=./linux_out  menuconfig
```

###### 3.7编译生成kernel image，arm的kernel image存放在arch/arm/boot/zImage.

```
make ARCH=arm CROSS_COMPILE=arm-eabi-   O=./linux_out all
```

###### *报错*：

```
/home/ll/mygit/panappticon/kernel/panappticon-kernel/include/eventlogging/events.h:546:39: error: macro "event_log_waitqueue_wait" requires 2 arguments, but only 1 given
make[2]: *** [kernel/sched.o] 错误 1
make[1]: *** [kernel] 错误 2
make: *** [sub-make] 错误 2
```
###### *原因*：内核需要按照具体的andoroid手机进行配置
###### *解决方法*：
1、查找源码，找到需要配置的变量
```
xhl@xhl-SMBIOS:~/mygit/panappticon/kernel/panappticon-kernel$ sudo apt install silversearcher-ag
xhl@xhl-SMBIOS:~/mygit/panappticon/kernel/panappticon-kernel$ ag event_log_waitqueue_wait
kernel/wait.c
75:		event_log_waitqueue_wait(q);
91:		event_log_waitqueue_wait(q);

kernel/eventlogging/events.c
3:void event_log_waitqueue_wait(void* wq) {

include/linux/wait.h
29:extern void event_log_waitqueue_wait(void* wq);
31:#define event_log_waitqueue_wait(t) do{;}while(0);
37:#define event_log_waitqueue_wait(t) do{;}while(0);
43:#define event_log_waitqueue_wait(t, p) do{;}while(0);
416:		event_log_waitqueue_wait(&wq);				\

include/eventlogging/events.h
546:void event_log_waitqueue_wait(void* wq);
xhl@xhl-SMBIOS:~/mygit/panappticon/kernel/panappticon-kernel$ vi include/linux/wait.h 
```
2、在make ARCH=arm  O=./linux_out  menuconfig后显示的配置界面里

Kernel hacking  --->Event Logging Zhang/Bild---->Log wait queue event waits  点击y选中   /：查询

3、Android内核不需要Linux内核的所有功能，如上这么配置，需要配置的东西很多，可以获取Android官方的默认内核配置文件.config


（http://blog.csdn.net/a578559967/article/details/8654563）

在android studio里建立一个和Panappticon一样的Android虚拟机，Galaxy Nexus 、Jelly Bean、armeabi-v7a、android4.1

然后启动虚拟机，利用ddms从模拟器中提出内核配置文件/proc/config.gz:

替换cp config ~/mygit/panappticon/kernel/panappticon-kernel/arch/arm/configs/.config

make ARCH=arm CROSS_COMPILE=arm-eabi- O=./linux_out all

报错，有待实验

4、查看Panappticon使用的是什么config文件

cd configs/

git log -p查看提交历史，找到关于config的是tuna_eventlogging_defconfig

ls tuna_eventlogging_defconfig 在configs/查看是否有这个config，有的话用这个config进行编译

make ARCH=arm CROSS_COMPILE=arm-eabi- O=./linux_out tuna_eventlogging_defconfig



###### 3.8根据提示找到arm的kernel image

```
ls ~/mygit/panappticon/kernel/panappticon-kernel/linux_out/arch/arm/boot/zImage
```

##### 4.Build the Android system images in the standard fashion.

###### 4.1在180上编译android 4.1.2镜像，为了避免配置编译环境的问题，不然可以按照官方文档进行配置,android4.1.2必须在jdk1.6环境下编译，并配置环境变量，切换jdk

```
scp lh@192.168.0.180:~/sdk/jdk1.6.0_45.tar.gz /home/ll
```
###### 4.2把修改过的Android4.1.2源码拷贝到180上，利用docker进行编译，lunch选择full-eng
```
scp -r ./ANDROID_SOURCE4.1.2/ lh@192.168.0.180:/home/lh/ll/
```
scp断点续传
```
rsync -rP --rsh=ssh /home/ll/mygit/ANDROID_SOURCE4.1.2/ lh@192.168.0.180:/home/lh/ll/
```
```
source build/env
lunch 1
make -j16
```
报错：编译时所有引号都报错，修改bashrc 添加lan = C.UTF-8   **配置方法再看一下**


###### 4.3找到编译好的镜像导出
```
ll/ANDROID_SOURCE4/out/target/product/generic
system.img
userdate.img
ramdisk.img
```
```
scp lh@192.168.0.180:/home/lh/ll/ANDROID_SOURCE4/out/target/product/generic/*.img .   当前目录为ANDROID_SOURCE_4.1.2_IMG
```
###### 4.4用命令行启动模拟器，把系统和内核作为参数传入

```
emulator -avd Galaxy_Nexus_API_16 -system ~/ANDROID_SOURCE_4.1.2_IMG/system.img -kernel ~/mygit/panappticon/kernel/panappticon-kernel/linux_out/arch/arm/boot/zImage
```

##### 5.Build and install on your server the EventLoggingServer application in the tools/ directory.  Panappticon traces will be uploaded by the phone.
```
root@dd34e340243a:~/ll/panappticon-tools/EventLoggingServer# ./compile.sh

root@dd34e340243a:~/ll/panappticon-tools/EventLoggingServer# mkdir bin
root@dd34e340243a:~/ll/panappticon-tools/EventLoggingServer# ./compile.sh 
added manifest
adding: servers/Collector.class(in = 531) (out= 367)(deflated 30%)
adding: servers/CollectorWorker.class(in = 3911) (out= 2263)(deflated 42%)
adding: common/BaseServer.class(in = 3068) (out= 1819)(deflated 40%)
adding: common/BaseWorker.class(in = 1969) (out= 1121)(deflated 43%)
adding: common/Definition.class(in = 1288) (out= 626)(deflated 51%)
adding: common/PrefixParser.class(in = 919) (out= 531)(deflated 42%)
root@dd34e340243a:~/ll/panappticon-tools/EventLoggingServer# ls
bin  compile.sh  config.txt  manifest  src
root@dd34e340243a:~/ll/panappticon-tools/EventLoggingServer# ls bin/
Collector.jar  common  servers

root@dd34e340243a:~/ll/panappticon-tools/EventLoggingServer/bin# java -jar Collector.jar 

root@dd34e340243a:~/ll/panappticon-tools/EventLoggingServer/bin# netstat -tpln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp6       0      0 :::5204                 :::*                    LISTEN      2734/java       
root@dd34e340243a:~/ll/panappticon-tools/EventLoggingServer/bin# fg
java -jar Collector.jar
```
##### 6.Update the EventLogging application in the tools/ directory to point to your server's URL.


##### 7.Build the EventLogging application and install the resulting *.apk.
因为EventLogging有Android.mk文件，需要在放在源码环境里编译，进入docker，把EventLogging放到到ANDROID_SOURCE4/packages/apps的文件夹下
```
xhl@xhl-SMBIOS:~$ ssh lh@192.168.0.180
lh@server2:~/ll$ docker start -ai ll-5.1
root@dd34e340243a:~/ll/ANDROID_SOURCE4/packages/apps
root@dd34e340243a:~/ll# git clone https://github.com/EmbeddedAtUM/panappticon-tools.git
root@dd34e340243a:~/ll/panappticon-tools# git branch -a
root@dd34e340243a:~/ll/panappticon-tools# cd EventLogging
root@dd34e340243a:~/ll/panappticon-tools# cp -rf EventLogging ~/ll/ANDROID_SOURCE4/packages/apps/
-r 递归处理，指定目录下的文件和子目录一并处理
-f 强行复制，无论目标是否存在
root@dd34e340243a:~/ll/panappticon-tools# cd -
cd -是返回到上一次的工作目录
/root/ll/panappticon-tools/EventLogging
root@dd34e340243a:~/ll/ANDROID_SOURCE4/packages/apps/EventLogging# vi Android.mk
看LOCAL_PACKAGE_NAME := EventLogging

root@dd34e340243a:~/ll/ANDROID_SOURCE4/build# vi target/product/core.mk    EventLogging加入编译系统build/target/product/core.mk:PRODUCT_PACKAGES

root@dd34e340243a:~/ll/ANDROID_SOURCE4# source build/envsetup.sh
root@dd34e340243a:~/ll/ANDROID_SOURCE4# lunch 1
root@dd34e340243a:~/ll/ANDROID_SOURCE4/packages/apps/EventLogging# mm  只编译这个应用
```
##### 8.The scripts in the tools/ directory may be helpful for parsing and interpretting the logs.


其他：
emulator -avd Galaxy_Nexus_API_16 -kernel ~/mygit/panappticon/kernel/panappticon-kernel/linux_out/arch/arm/boot/zImage -system ~/ANDROID_SOURCE_4.1.2_IMG/system.img -show-kernel
打印kernel信息

xhl@xhl-SMBIOS:~/Android/Sdk/tools$ emulator -avd Galaxy_Nexus_API_16 -kernel ~/mygit/panappticon/kernel/panappticon-kernel/linux_out/arch/arm/boot/zImage -system ~/ANDROID_SOURCE_4.1.2_IMG/system.img -help|grep -i kernel

模拟器gpu加速
xhl@xhl-SMBIOS:~/Android/Sdk/tools$ glxinfo
The program 'glxinfo' is currently not installed. You can install it by typing:
sudo apt-get install mesa-utils
xhl@xhl-SMBIOS:~/Android/Sdk/tools$ sudo apt-get install mesa-utils




