# 1 文献

|题目|作者|类型|链接
| ------------- |------------- |------------- |------------- |
| Android进程间通信Binder扩展模型的设计与实现 | 陈莉君; 张超	| 期刊 | http://suo.im/1P7Lhy 知网
| 面向桌面Linux的Android运行环境构建 | 张超 （国防科学技术大学）  |   硕士 | http://suo.im/knMAM 知网
| 基于LXC的Android系统虚拟化关键技术设计与实现 | 吴佳杰 | 硕士 | http://suo.im/3XyI6Q 知网

《基于LXC的Android系统虚拟化关键技术设计与实现》中的 Binder驱动复用 对我的参考价值较大。可以参考它对Binder的修改。

参考：https://github.com/openthos/research-analysis/blob/master/developers/%E4%BD%95%E5%85%B4%E9%B9%8F/%E5%85%B6%E4%BB%96.md

# 2 书籍

|书名|作者|ISBN|
| ------------- |------------- |------------- |
|深入理解Android：卷1|邓平凡| 9787111389187 |
|Android系统源代码情景分析|罗升阳| 9787121181085 |

# 3 网络资料

```
标题：Binder系列—开篇
作者：Gityuan
类型；系列博客
http://gityuan.com/2015/10/31/binder-prepare/

标题：Android Binder 分析——通信模型
作者：Mingming
类型：系列博客
http://light3moon.com/2015/01/28/Android%20Binder%20%E5%88%86%E6%9E%90%E2%80%94%E2%80%94%E9%80%9A%E4%BF%A1%E6%A8%A1%E5%9E%8B/

标题：Android驱动_Binder_情景分析视频课程
作者：韦东山
类型：系列视频
地址：http://edu.51cto.com/course/course_id-6829.html

标题：Android系统_binder_c程序示视频课程
作者：韦东山
类型：系列视频
地址：http://edu.51cto.com/course/course_id-6595.html
```

# 4 相关项目

## 在Android系统中运行桌面Linux程序

自动化部署软件：Linux Deploy、Linux Installer

运行原理：Chroot\PRoot

显示原理：SSH\VNC

## 在桌面Linux系统中运行Android应用程序

| 项目名 | 源码 | 原理 | 效果|链接
| ------------- |------------- |------------- |------------- |------------- |
| BlueStacks | 闭源 | VirtualBox虚拟机 | 同虚拟机运行Android X86效果 | www.bluestacks.com
| Genymotion | 闭源 | VirtualBox虚拟机 | 同虚拟机运行Android X86效果 | https://www.genymotion.com
| Shashlik | 开源 | SDK中的QEMU虚拟机 | 同SDK模拟器效果 | www.shashlik.io
| Anbox | 开源 | 构造Android系统兼容层 + QEMU | 不完善，仅能运行少数APP | https://github.com/anbox/anbox 
| Android Runtime for Chrome | 闭源 | 构造Android系统兼容层 | 较稳定 | https://developer.chrome.com/apps/getstarted_arc
