# 1 前言

由于大论文实验方案更改，放弃从 ioctl() 直接获取binder数据的方案，改为从 JAVA 层函数直接拦截获取。 所以为了方便实验，利用 Xposed 框架，直接hook JAVA 函数，从而获取binder的上层业务数据。

# 2 Xposed 框架介绍

项目源码地址：[https://github.com/rovo89/XposedBridge][1]

Xposed 是目前 Android 平台最成熟最强大的开源的 JAVA 层代码hook框架，它能够hook包括系统进程在内的任何运行在ART虚拟机上的进程里的 JAVA 方法。对指定类的指定方法或变量进行修改或覆写。

Xposed 框架在 Android 手机玩家中已经极为普及，已存在大量基于 Xposed 框架的UI美化或者程序修改插件，比如微信自动抢红包、网易云音乐破解。

因此我通过编写 Xposed 插件，能够拦截到我想要的数据。当然我也可以不用 Xposed 框架，直接在 Android 源代码里写，但是使用 Xposed 框架，调试较为方便，所以在实验过程中我借助 Xposed 完成数据获取。

# 3 Xposed 插件（模块）编写

Xposed 插件（模块）编写分为四步。

## 3.1 在 Android 项目里添加 Xposed 依赖

目前 Android 应用层编程均使用A ndroid Studio 开发环境，在一个项目中有若干个模块，每个模块可以理解为一个APP。因此新建好项目之后，打开所要编写的模块，编辑该模块的`build.gradle`文件。

在`dependencies`里添加`provided 'de.robv.android.xposed:api:82'`，如需要观看源代码则再添加`provided 'de.robv.android.xposed:api:82:sources'`。

添加完 Xposed 依赖后，同步即可。

``` gradle
dependencies {
    compile fileTree(dir: 'libs', include: ['*.jar'])
    androidTestCompile('com.android.support.test.espresso:espresso-core:2.2.2', {
        exclude group: 'com.android.support', module: 'support-annotations'
    })
    compile 'com.android.support:appcompat-v7:25.2.0'
    testCompile 'junit:junit:4.12'
    provided 'de.robv.android.xposed:api:82'
    provided 'de.robv.android.xposed:api:82:sources'
}
```

## 3.2 在 AndroidManifest.xml 里添加 Xposed 声明

打开该模块的`AndroidManifest.xml`文件，在`<application>`里添加`xposedmodule`、`xposeddescription`、`xposedminversion`三个`meta-data`。

- `xposedmodule`表示这是一个 Xposed 模块（插件）。
- `xposeddescription`表示对该模块的描述。
- `xposedminversion`表示支持的 Xposed 框架的最小版本号。

``` xml
    <application android:allowBackup="true" android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name" android:supportsRtl="true" android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <meta-data
            android:name="xposedmodule"
            android:value="true" />
        <meta-data
            android:name="xposeddescription"
            android:value="Hook System Call" />
        <meta-data
            android:name="xposedminversion"
            android:value="82" />
    </application>
```

## 3.3 实现 IXposedHookLoadPackage 接口

插件的入口只能是指定的几个接口，主要有以下两个：

- `IXposedHookLoadPackage`该接口在App被加载时调用，用于hook ART虚拟机上的进程，即每个APP运行的进程。
- `IXposedHookZygoteInit`该接口在Zygote启动时调用，用于hook系统进程。

值得注意的是在 Android 5.x 版本以后，JAVA类编写的系统服务已经与普通APP一样，由ART虚拟机加载，使用`IXposedHookLoadPackage`接口。
> 关于此问题，作者在github的回复：[https://github.com/rovo89/XposedBridge/issues/72][3]
作者说在5.x版本之后，系统服务的类由另外的加载器加载，用handleLoadPackage方法，并且找包名叫 android 的包。

我的实验基于 Android 6.0 ，需要修改`ActivityManagerService`服务的`startActivity()`方法，所以我实现`IXposedHookLoadPackage`接口。

代码如下：

``` java
public class SystemHook implements IXposedHookLoadPackage {
    private static final String TAG = "SystemHook";
    private static final Object ACTIVITY_START_SUCCESS = 0;     //ActivityManager.START_SUCCESS

    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        XposedBridge.log("Loaded app: " + lpparam.packageName);
        if (!lpparam.packageName.equals("android")) {
            return;
        }

        final Class<?> IApplicationThreadClazz = XposedHelpers.findClass("android.app.IApplicationThread", lpparam.classLoader);
        final Class<?> IntentClazz = XposedHelpers.findClass("android.content.Intent", lpparam.classLoader);
        final Class<?> IBinderClazz = XposedHelpers.findClass("android.os.IBinder", lpparam.classLoader);
        final Class<?> ProfilerInfoClazz = XposedHelpers.findClass("android.app.ProfilerInfo", lpparam.classLoader);
        final Class<?> BundleClazz = XposedHelpers.findClass("android.os.Bundle", lpparam.classLoader);

        XposedHelpers.findAndHookMethod("com.android.server.am.ActivityManagerService",
                lpparam.classLoader,
                "startActivity",
                IApplicationThreadClazz,
                String.class,
                IntentClazz,
                String.class,
                IBinderClazz,
                String.class,
                int.class,
                int.class,
                ProfilerInfoClazz,
                BundleClazz,
                new XC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        String callingPackage = (String) param.args[1];
                        Intent intent = (Intent) param.args[2];
                        XposedBridge.log("SystemHook:startActivity:"
                                + callingPackage
                                + " "
                                +  intent.toString());
                        Log.d(TAG, "SystemHook:startActivity:" + intent.toString());
                        param.setResult(ACTIVITY_START_SUCCESS);
                    }
                });
    }
}
```

我新建了一个类`SystemHook`，实现了`IXposedHookLoadPackage`接口。
实现最关键的是实现`handleLoadPackage()`方法，插件的执行从这里开始。

这里面有两个类`XposedBridge`和`XposedHelpers`。

- `XposedBridge`有个`log()`方法，能打印Xposed日志。
- `XposedHelpers`有`findClass()`方法用于反射出指定的类，`findAndHookMethod()`用于hook方法。

我们首先通过`lpparam`参数，获取当前加载的应用包名称，从而判断是不是我所要修改的`ActivityManagerService`服务。`android`就是系统服务所在的包名。

然后通过`XposedHelpers.findClass`把需要hook的方法的所有形参的类反射处理。常规类型不需要通过`findClass`获取，比如int类型，直接写`int.class`。

最后通过`XposedHelpers.findAndHookMethod`方法反射修改指定函数的逻辑。
这个方法的参数介绍如下：

- 第一个参数指定该方法所在的类。
- 第二个参数指定类的加载器，`lpparam.classLoader`就是一般应用的类加载器。
- 第三个直至倒数第二个依次与需要hook的方法的形参一一对应。
- 最后一个参数继承`XC_MethodHook`类，函数的修改逻辑就写在里面。

`XC_MethodHook`类主要有两个方法需要覆写，`beforeHookedMethod`和`afterHookedMethod`分别用于hook方法调用前和方法调用后。

这里我用`afterHookedMethod`在`startActivity()`方法调用后，添加了自己的逻辑，并调用`param.setResult()`方法修改了返回值。

## 3.4 声明Xposed插件（模块）入口

在 Android Studio 模块的`assets`文件夹中添加xposed_init文件，写上类的限定名。

Android Studio 模块默认没有`assets`文件夹，可以手动在`模块根目录/src/main`中新建该文件夹。

我的入口声明如下：
```
com.example.xposedhook.SystemHook
```

编写好插件之后，安装到 Android 系统，并在 Xposed 框架中启用即可。

# 4 Xposed框架安装

在 Android 中安装 Xposed 框架非常简单，下载一个名为`Xposed Installer`的APP，打开APP即可安装。

`Xposed Installer`官方下载地址：[https://forum.xda-developers.com/showthread.php?t=3034811][4]

注意：在 Android 中使用 Xposed 需要root权限。

Xposed 框架安装完成和安装新插件都需要重启系统。

# 5 Xposed原理简介

在Android系统中，应用的进程都是由Zygote来孵化。

Xposed 通过将更改的系统程序刷入系统，替换系统原有的逻辑。实现在`Zygote`进程运行时加载 Xposed 的组件`XposedBridge`。

XposedBreidge中有一个专门用于hook的native方法，该方法通过java的反射机制，覆盖掉了原先也就是我们想要hook的java方法。

然后 Xposed 替换`app_process`来实现Android上的所有App使用替换后的`app_process`加载。

Zygote加载XposedBridge之后，将会把所有需要hook的方法都替换为名为hookMethodNative的jni函数，该函数处理相应的参数（被hook的函数名称，hook的方法）后，通过反射调用java方法handleHookedMethod，并由handleHookedMethod完成用户指定的hook逻辑。

因此 Xposed 针对每个版本的 Android 系统都各自修改了其系统文件，并针对ARM、X86等构架单独编译。

更多参考博文：[Xposed实现过程][5]

# 6 完成效果和总结

启用插件之后，每次APP调用`startActivity()`来启动新的Activity，我们都能检测到。
Log打印如下图：
![hook_startActivity_log](https://github.com/HsingPeng/research-analysis/raw/master/projects/and-linux/image/hook_startActivity_log.png)

借助 Xposed ，我已经成功的拦截并实现了 `startActivity()`的自定义处理，对于Android中的其他组件`Service`、`Broadcast`可用同样的方式处理。但是，对于`AIDL`和`Content Provider`的处理还有些问题。接下来我会想办法处理这几个组件，实现这几个组件向 Linux 程序的扩展。

这些都处理完成之后，整个 Binder 机制的扩展就走通了，再完善上层接口即可。

参考博文：
1. Android中Xposed框架篇---利用Xposed框架实现拦截系统方法
http://blog.csdn.net/jiangwei0910410003/article/details/52822081
2. 理解 Android Hook 技术以及简单实战
http://www.jianshu.com/p/4f6d20076922
3. [OFFICIAL] Xposed for Lollipop/Marshmallow/Nougat [v88.2, 2017/10/30]
https://forum.xda-developers.com/showthread.php?t=3034811
4. Xposed模块的开发
http://www.snowdream.tech/2016/09/02/android-develop-xposed-module/
5. Xposed实现过程
https://goodoak.github.io/2016/09/27/xposed-intro/
6. 使用Xposed添加自定义系统服务
https://haoutil.com/topic/xposed-add-custom-system-service
7.  Custom System Service using XposedBridge
http://nameless-technology.blogspot.com/2013/11/custom-system-service-using-xposedbridge.html
8. ClassNotFoundException #72
https://github.com/rovo89/XposedBridge/issues/72


  [1]: https://github.com/rovo89/XposedBridge
  [3]: https://github.com/rovo89/XposedBridge/issues/72
  [4]: https://forum.xda-developers.com/showthread.php?t=3034811
  [5]: https://goodoak.github.io/2016/09/27/xposed-intro/
