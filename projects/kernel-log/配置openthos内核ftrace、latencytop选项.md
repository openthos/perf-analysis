## 配置openthos内核ftrace、latencytop选项

`root@df33622109f6:~/ll/multiwindow/kernel# ls`

`root@df33622109f6:~/ll/multiwindow/kernel# cp arch/x86/configs/android-x86_64_defconfig .config`

`root@df33622109f6:~/ll/multiwindow/kernel# make menuconfig ARCH=x86_64`//配置ftrace、latencytop选项

`root@df33622109f6:~/ll/multiwindow/kernel# git status .`

`root@df33622109f6:~/ll/multiwindow/kernel# cp .config arch/x86/configs/android-x86_64_defconfig`

`root@df33622109f6:~/ll/multiwindow/kernel# git status .`

`root@df33622109f6:~/ll/multiwindow/kernel# git diff .`

`root@df33622109f6:~/ll/multiwindow/kernel# rm .config .config.old scripts/basic/.fixdep.cmd scripts/kconfig/.mconf.cmd`
