# GT在Openthos无法正确运行问题的分析和解决

## 问题一：Openthos上SM测试模块进程信息不能显示问题

### 1.问题描述

SM测试模块针对单个进程进行流畅度测试，所以在测试前需要选择要进行监控的进程，正常情况下，打开SM测试插件即可看到系统正在运行的所有进程名，通过实验，在模拟器
上运行GT的SM测试模块可以看到进程信息，但是在Openthos上看不到，导致无法在Openthos上正确运行GT的SM测试模块并通过SM进行流畅度测试。

### 2.问题分析

#### 2.1 找到SM测试模块种获取进程信息的代码片段

正常情况下，进程信息被存放在一个ListView中进行显示，首先需要找到这个ListView，并查看它的显示数据是如何获取的。

在GT/android/src/com/tencent/wstt/gt/plugin/smtools/SMActivity.java 文件中SMActivity类的onCreate方法里找到了这个ListView

```
listview = (ListView) findViewById(R.id.listViewOtherSM);
listview.setChoiceMode(ListView.CHOICE_MODE_SINGLE);
ArrayList<String> datas = getData();
ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_single_choice,datas);
listview.setAdapter(adapter);
```

其中listview的datas是由getData()函数获取的，该函数如下所示：

```
private ArrayList<String> getData() {
		List<ProcessInfo> rp = ProcessUtils.getAllRunningAppProcessInfo();
		for (ProcessInfo i : rp) {
			data.add(i.name);
		}
		return data;
}
```

由此得到，进程信息是由ProcessUtils类的getAllRunningAppProcessInfo()函数得到的，ProcessUtils类在 GT/android/src/com/tencent/wstt/gt
/api/utils/ProcessUtils.java文件中，getAllRunningAppProcessInfo()函数如下所示：

```
public static List<ProcessInfo> getAllRunningAppProcessInfo() {
		return processUtil.getAllRunningAppProcessInfo();
}
```

需要看以下processUtil是什么

```
private static IProcess processUtil;
```

所以接下来看IProcess，如下所示：

```
static interface IProcess {
		List<ProcessInfo> getAllRunningAppProcessInfo();
		String getPackageByUid(int uid);
		int getProcessPID(String pName);
		int getProcessUID(String pName);
		boolean hasProcessRunPkg(String pkgName);
		boolean isProcessAlive(String sPid);
		void killprocess(String proc, int cmd);
		boolean initUidPkgCache();
}
```

IProcess是一个借口，通过查看源码，有两个类实现了这个接口，分别是Process5x和Process4x，分别查看他们的getAllRunningAppProcessInfo()方法是如何实现的，
代码如下所示：

```
static class Process5x implements IProcess
{
  ... ...
  
  @Override
  public List<ProcessInfo> getAllRunningAppProcessInfo() {
	List<ProcessInfo> appProcessList = new ArrayList<ProcessInfo>();
			
	// 先取Android进程的父进程zygote的进程号，64位app对应的是zygote64
	int zygotePid = -1;
	int zygotePid64 = -1;

	BufferedReader readerZ = null;
	try {
		ProcessBuilder execBuilderZ = null;
		execBuilderZ = new ProcessBuilder("sh", "-c", "ps |grep zygote");
		execBuilderZ.redirectErrorStream(true);
		Process execZ = execBuilderZ.start();
		InputStream isZ = execZ.getInputStream();
		readerZ = new BufferedReader(new InputStreamReader(isZ));

		String lineZ = "";
		while ((lineZ = readerZ.readLine()) != null) {
			String[] arrayZ = lineZ.trim().split("\\s+");
			if (arrayZ.length >= 9) {
				if (arrayZ[8].equals("zygote"))
				{
					zygotePid = Integer.parseInt(arrayZ[1]);
				}
				else if (arrayZ[8].equals("zygote64"))
				{
					zygotePid64 = Integer.parseInt(arrayZ[1]);
				}
			}
		}
	}catch (Exception e) {
		e.printStackTrace();
	} finally {
		FileUtil.closeReader(readerZ);
	}
	if (zygotePid < 0){
		return appProcessList;
	}

	// 正式取可用的Android进程
	BufferedReader reader = null;
	try {
			ProcessBuilder execBuilder = null;
			execBuilder = new ProcessBuilder("sh", "-c", "ps |grep u0_a");
			execBuilder.redirectErrorStream(true);
			Process exec = null;
			exec = execBuilder.start();
			InputStream is = exec.getInputStream();
			reader = new BufferedReader(new InputStreamReader(is));

			String line = "";
			while ((line = reader.readLine()) != null) {
				String[] array = line.trim().split("\\s+");
				if (array.length >= 9) {
					int uid = Integer.parseInt(array[0].substring(4)) + 10000;
					int pid = Integer.parseInt(array[1]);
					int ppid = Integer.parseInt(array[2]);
					// 过滤掉系统子进程，只留下父进程是zygote的进程
					if (ppid == zygotePid || ppid == zygotePid64)
					{
						ProcessInfo pi = new ProcessInfo(pid, array[8], ppid, uid);
						appProcessList.add(pi);
						procInfoCache.put(array[8], pi);
					}	
				}
			}
	} catch (Exception e) {
		e.printStackTrace();
	}finally
	{
		FileUtil.closeReader(reader);
	}
	return appProcessList;
  }
  
  ... ...
  
}
```

Process5x的getAllRunningAppProcessInfo()正是获取进程信息的全部代码，主要包括三步：

（1）先取Android进程的父进程zygote的进程号

（2）正式取可用的Android进程

（3）过滤掉系统子进程，只留下父进程是zygote的进程

大致确定Openthos上SM测试模块进程信息不能显示问题的原因在这部分代码当中

```
static class Process4x  implements IProcess
{
    ... ...
    
  @Override
  public List<ProcessInfo> getAllRunningAppProcessInfo() {
	ActivityManager am = (ActivityManager) GTApp.getContext().getSystemService(Context.ACTIVITY_SERVICE);
	List<ActivityManager.RunningAppProcessInfo> appProcessList = am.getRunningAppProcesses();
	List<ProcessInfo> ret = new ArrayList<ProcessInfo>();
	for (ActivityManager.RunningAppProcessInfo info : appProcessList)
	{
		// pid目前不需要，默认赋值为-1
		ProcessInfo processInfo = new ProcessInfo(info.pid, info.processName, -1, info.uid);
		ret.add(processInfo);
	}
	return ret;
 }
    ... ...
}
```

Process5x和Process4x的分别代表什么以及他们的区别还没有研究。。。

#### 2.2 打log定位问题代码的准确位置

将关注点集中在Process5xgetAllRunningAppProcessInfo()，在其中随机添加log发现问题主要集中在第二步正式取可用的Android进程的代码中，代码如下：

```
// 正式取可用的Android进程
BufferedReader reader = null;
try {
	Log.v("11111","1");
	ProcessBuilder execBuilder = null;
	execBuilder = new ProcessBuilder("sh", "-c", "ps |grep u0_a");
	Log.v("11111","2");

	execBuilder.redirectErrorStream(true);
	Process exec = null;
	exec = execBuilder.start();
	Log.v("11111","3");
	InputStream is = exec.getInputStream();
	reader = new BufferedReader(new InputStreamReader(is));

	String line = "";
	line = reader.readLine();
	line = reader.readLine();
	line = reader.readLine();
	while ((line = reader.readLine()) != null) {
		String[] array = line.trim().split("\\s+");
		if (array.length >= 9) {
			Log.v("11111","4");
			int uid = Integer.parseInt(array[0].substring(4)) + 10000;
			Log.v("11111","5");
			int pid = Integer.parseInt(array[1]);
			int ppid = Integer.parseInt(array[2]);
			// 过滤掉系统子进程，只留下父进程是zygote的进程
			if (ppid == zygotePid || ppid == zygotePid64)
			{
				ProcessInfo pi = new ProcessInfo(pid, array[8], ppid, uid);
				appProcessList.add(pi);
				procInfoCache.put(array[8], pi);
			}					
		}
	}

} catch (Exception e) {
	e.printStackTrace();
}finally
{
	FileUtil.closeReader(reader);
}
return appProcessList;
}
```

log输出如下：

```
03-15 10:41:28.919 4718-4718/com.tencent.wstt.gt V/AAAA: 1879
03-15 10:41:28.919 4718-4718/com.tencent.wstt.gt V/AAAA: 1880
03-15 10:41:28.919 4718-4718/com.tencent.wstt.gt V/11111: 1
03-15 10:41:28.919 4718-4718/com.tencent.wstt.gt V/11111: 2
03-15 10:41:28.922 4718-4718/com.tencent.wstt.gt V/11111: 3
03-15 10:41:28.923 4718-4718/com.tencent.wstt.gt V/11111: 4
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err: java.lang.NumberFormatException: Invalid int: "ING:"
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at java.lang.Integer.invalidInt(Integer.java:138)
... ... 
```

第5个log没有输入，并且报int uid = Integer.parseInt(array[0].substring(4)) + 10000;处数据类型异常，存在非法整形 "ING:"。所以之后的代码无法执行，
导致进程信息无法显示。

#### 2.3 结合Openthos分析错误原因

报错原因是array[0]类型错误，所以分析array来源，由代码可知是ps |grep u0_a的命令的执行结果，在Openthos上实验，直接输入该命令，查看结果输出

```
WARNING: linker: WARNING: linker: [vdso][vdso]: unused DT entry: type : unused DT entry: type 0x6fffef50x6fffef5

uo_a18 2255  1879 1601244 130804 0000000  d892b35a S com.android.systemui
uo_a12 2281  1879 1451243 47256  0000000  d892b35a S com.github.openthos.printer.localprint
```

通过检查结果输出，发现Openthos会输出三行无用信息，所以确定报错原因是这些无用信息导致array[0]获取的值类型错误，最终导致程序不能正常执行，进程信息无法显示。

### 3.解决方法

结合Openthos的log输出特点，对输出信息进行筛选，从正确结果输出部分开始分析，修改代码如下：
```
// 正式取可用的Android进程
BufferedReader reader = null;
try {
	ProcessBuilder execBuilder = null;
	execBuilder = new ProcessBuilder("sh", "-c", "ps |grep u0_a");

	execBuilder.redirectErrorStream(true);
	Process exec = null;
	exec = execBuilder.start();
	InputStream is = exec.getInputStream();
	reader = new BufferedReader(new InputStreamReader(is));

	String line = "";
	line = reader.readLine();
	line = reader.readLine();
	line = reader.readLine();
	while ((line = reader.readLine()) != null) {
		String[] array = line.trim().split("\\s+");
    //在此添加判断筛选的代码
		if (array.length >= 9 && array[0].indexOf("u0_a")!=-1) {
			int uid = Integer.parseInt(array[0].substring(4)) + 10000;
			int pid = Integer.parseInt(array[1]);
			int ppid = Integer.parseInt(array[2]);
			// 过滤掉系统子进程，只留下父进程是zygote的进程
			if (ppid == zygotePid || ppid == zygotePid64)
			{
				ProcessInfo pi = new ProcessInfo(pid, array[8], ppid, uid);
				appProcessList.add(pi);
				procInfoCache.put(array[8], pi);
			}					
		}
	}

} catch (Exception e) {
	e.printStackTrace();
}finally
{
	FileUtil.closeReader(reader);
}
return appProcessList;
}
```

通过修改代码，Openthos上SM测试模块进程信息不能显示问题得到解决！

## 问题二：Openthos上SM测试模块的测试结果不正确

### 1.问题描述

SM测试模块以SM作为指标，通过统计跳帧的数量来衡量流畅度，其满分为60，对于所有的Android应用，跳帧现象是普遍的并且变化的，所以SM的测试结果应该在0到60间浮动。
但是通过在Openthos上实验，所有的测试结果都为60，即不存在跳帧现象，这个测试结果是不正确的。
### 2.问题分析
 
#### 2.1 从SM的测量统计原理进行分析

GT的SM测试模块对SM的测量计算方法已经调研清楚（[文档第5部分](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/SM%E8%B0%83%E7%A0%94%E6%8A%A5%E5%91%8A.md)），SM值通过计算统计Choreographer输出log的跳帧数据获得，但是通过实验发现没有Choreographer关于跳帧的log输出，而Choreographer的工作机制也已经调研清楚（[文档第3部分](https://github.com/openthos/research-analysis/blob/master/projects/android-log/GT/SM%E8%B0%83%E7%A0%94%E6%8A%A5%E5%91%8A.md)），可能的原因是log输出的条件不够，即debug.choreographer.skipwarning的值不为1。

#### 2.2 针对debug.choreographer.skipwarning的值进行实验

1.运行SM测试测试后，直接输入getprop debug.choreographer.skipwarning命令，显示结果为1，也就是说明GT完成debug.choreographer.skipwarning了的设置，log不是因为不满度条件没有输出

2.重启计算机（不进行SM测试），输入getprop debug.choreographer.skipwarning命令，显示结果为空，也就是系统本身没有对debug.choreographer.skipwarning进行赋值，也就是frameworks\base\core\java\android\view\Choreographer.java文件根本没有执行到，所以log没有正确输出，而这个文件没有执行到，有可能和我之前在startmenu代码中打log却没有输出的情况一样，是由于源码环境破坏导致的，重新同步以下代码应该就可以解决

**薛海龙的意见：** Openthos没有root彻底，导致debug.choreographer.skipwarning没有被GT设置，他通过直接更改frameworks\base\core\java\android\view\Choreographer.java中debug.choreographer.skipwarning的初始化值为1，实现了log的打印

**我的分析：** 第一个实验种输入getprop debug.choreographer.skipwarning命令，显示结果为1，可以说明GT完成debug.choreographer.skipwarning了的设置，因为系统种不可能有两个debug.choreographer.skipwarning变量，GT也不可能自己创建一个debug.choreographer.skipwarning变量，而且这个实验用了新的代码环境，不能确定是因为新的代码环境的影响还是没有root彻底的影响，下周可以把薛海龙实验的Openthos代码种的frameworks\base\core\java\android\view\Choreographer.java中debug.choreographer.skipwarning恢复成正常情况30，如果能正常打印log，则说明是代码环境的问题，并不是因为root不彻底，在根据具体情况确定解决方法
