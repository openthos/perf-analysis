## SM测试进程显示的问题

 - 以下是进程显示的关键代码以及Log信息
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
				reader = new BufferedReader(
						new InputStreamReader(is));

				String line = "";
				line = reader.readLine();
				line = reader.readLine();
				line = reader.readLine();
				while ((line = reader.readLine()) != null) {
					String[] array = line.trim().split("\\s+");
					if (array.length >= 9) {
            Log.v("11111","4");
						int uid = Integer.parseInt(array[0].substring(4)) + 10000;

						//int uid = Integer.valueOf(array[0].substring(4)).intValue() + 10000;
						Log.v("BBBB", " "+uid);
						Log.v("11111","5");
						int pid = Integer.parseInt(array[1]);

						Log.v("BBBB", String.valueOf(pid));
						int ppid = Integer.parseInt(array[2]);
						// 过滤掉系统子进程，只留下父进程是zygote的进程
						if (ppid == zygotePid || ppid == zygotePid64)
						{
							ProcessInfo pi = new ProcessInfo(pid, array[8], ppid, uid);
							appProcessList.add(pi);
							procInfoCache.put(array[8], pi);
						}
						
					}
```

```
03-15 10:41:28.919 4718-4718/com.tencent.wstt.gt V/AAAA: 1879
03-15 10:41:28.919 4718-4718/com.tencent.wstt.gt V/AAAA: 1880
03-15 10:41:28.919 4718-4718/com.tencent.wstt.gt V/11111: 1
03-15 10:41:28.919 4718-4718/com.tencent.wstt.gt V/11111: 2
03-15 10:41:28.922 4718-4718/com.tencent.wstt.gt V/11111: 3
03-15 10:41:28.923 4718-4718/com.tencent.wstt.gt V/11111: 4
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err: java.lang.NumberFormatException: Invalid int: "ING:"
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at java.lang.Integer.invalidInt(Integer.java:138)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at java.lang.Integer.parse(Integer.java:410)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at java.lang.Integer.parseInt(Integer.java:367)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at java.lang.Integer.parseInt(Integer.java:334)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at com.tencent.wstt.gt.api.utils.ProcessUtils$Process5x.getAllRunningAppProcessInfo(ProcessUtils.java:334)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at com.tencent.wstt.gt.api.utils.ProcessUtils.getAllRunningAppProcessInfo(ProcessUtils.java:140)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at com.tencent.wstt.gt.manager.AUTManager.findProcess5x(AUTManager.java:93)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at com.tencent.wstt.gt.manager.AUTManager.findProcess(AUTManager.java:87)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at com.tencent.wstt.gt.activity.GTAUTFragment.doResume(GTAUTFragment.java:340)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at com.tencent.wstt.gt.activity.GTAUTFragment.onResume(GTAUTFragment.java:288)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.support.v4.app.Fragment.performResume(Fragment.java:2020)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.support.v4.app.FragmentManagerImpl.moveToState(FragmentManager.java:1107)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.support.v4.app.FragmentManagerImpl.moveToState(FragmentManager.java:1252)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.support.v4.app.FragmentManagerImpl.moveToState(FragmentManager.java:1234)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.support.v4.app.FragmentManagerImpl.dispatchResume(FragmentManager.java:2056)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.support.v4.app.FragmentController.dispatchResume(FragmentController.java:196)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.support.v4.app.FragmentActivity.onResumeFragments(FragmentActivity.java:505)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.support.v4.app.FragmentActivity.onPostResume(FragmentActivity.java:494)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.app.Activity.performResume(Activity.java:6241)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.app.ActivityThread.performResumeActivity(ActivityThread.java:2975)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.app.ActivityThread.handleResumeActivity(ActivityThread.java:3017)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:2392)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.app.ActivityThread.access$800(ActivityThread.java:151)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1303)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.os.Handler.dispatchMessage(Handler.java:102)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.os.Looper.loop(Looper.java:135)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at android.app.ActivityThread.main(ActivityThread.java:5254)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at java.lang.reflect.Method.invoke(Native Method)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at java.lang.reflect.Method.invoke(Method.java:372)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:903)
03-15 10:41:28.924 4718-4718/com.tencent.wstt.gt W/System.err:     at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:698)
```

 - 分析
  由以上Log发现出现了System.err，原因是java.lang.NumberFormatException: Invalid int: "ING:",即存在非数字类型的“ING：”。然后打印出来array[0]发现是  WARNING：，然后想到这是OPENTHOSL、的Log信息里，
  因此在OPENTHOS上手动 ps| grep u0_a  得到的结果如下
 
  ```
  WARNING: linker: WARNING: linker: [vdso][vdso]: unused DT entry: type : unused DT entry: type 0x6fffef50x6fffef5
  
  uo_a18 2255  1879 1601244 130804 0000000  d892b35a S com.android.systemui
  uo_a12 2281  1879 1451243 47256  0000000  d892b35a S com.github.openthos.printer.localprint
  .
  .
  .
  ```
  即OPENTHOS的Log取出来第一行是Warning，第二行是空白的，而在GT上没有进行筛选与判断，所以导致进程不显示，在GT中加上判断就可以了，如下所示
  
  ```
  while ((line = reader.readLine()) != null) {
					String[] array = line.trim().split("\\s+");
					//在此添加判断筛选的代码
          if (array.length >= 9 && array[0].indexOf("u0_a")!=-1) {
						int uid = Integer.parseInt(array[0].substring(4)) + 10000;
						Log.v("BBBB", " "+uid);
						Log.v("11111","5");
						int pid = Integer.parseInt(array[1]);

						Log.v("BBBB", String.valueOf(pid));
						int ppid = Integer.parseInt(array[2]);
						// 过滤掉系统子进程，只留下父进程是zygote的进程
						if (ppid == zygotePid || ppid == zygotePid64)
						{
							ProcessInfo pi = new ProcessInfo(pid, array[8], ppid, uid);
							appProcessList.add(pi);
							procInfoCache.put(array[8], pi);
						}
						
					}
  ```
  
