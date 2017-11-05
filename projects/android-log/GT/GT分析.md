## GT流畅度（SM）的分析
### FPS和SM的概念
 - FPS：1s内界面刷新的次数。正常情况下是1s刷新60次，即16.6ms刷新一次是为流畅的
 - SM：腾讯提出的流畅度概念。腾讯认为FPS不能准确的量化流畅度。
 例如：在1s内，前332ms刷新了20次，完成任务，剩余668ms闲着一次都不刷新（所谓闲着是指屏幕无动画，静止不动），算出来帧率是20。所以腾讯提出来
 流畅度的概念（SM）：60-跳帧的次数。即统计1s内出现的跳帧的次数，然后用标准的60减去得到SM的值可以更好的量化流畅度
### SM测试前进程信息筛选与显示代码分析

 - ProcessUtils：进程筛选
  - zygote或者zygote64的判断
 
 ```
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
				readerZ = new BufferedReader(
						new InputStreamReader(isZ));

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
			}
 ```
  - 正式取可用的Android进程
  
  ```
  // 正式取可用的Android进程，放入列表中
			BufferedReader reader = null;
			try {
				ProcessBuilder execBuilder = null;
				//筛选用户进程				
				execBuilder = new ProcessBuilder("sh", "-c", "ps |grep u0_a");
				execBuilder.redirectErrorStream(true);
				Process exec = null;
				exec = execBuilder.start();
				InputStream is = exec.getInputStream();
				reader = new BufferedReader(
						new InputStreamReader(is));

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
							//将过滤的信息放入列表中
							appProcessList.add(pi);
							procInfoCache.put(array[8], pi);
						}
						
					}


  ```
  
   - 从列表中读取pid
    
    ```
    
		//从列表中读出pid
		public int getProcessPID(String pName) {
			int pId = -1;
			List<ProcessInfo> appProcessInfos = getAllRunningAppProcessInfo();
			for (ProcessInfo info : appProcessInfos) {
				if (info.name.equals(pName)) {
					pId = info.pid;
					break;
				}
			}
			return pId;
		}
    ```
   - 抽取出的方法，在SMActivity或者别的类种调用
    
    ```
     //在SMActivity中会调用此方法
public static int getProcessPID(String pName) {
		return processUtil.getProcessPID(pName);
	}

    ```
    
   - SMActivity调用进程的信息显示，并在SMActivity中对此进行下一步操作
    
    ```
    // SMActivity调用进程信息
AdapterView.OnItemClickListener listview_listener = new AdapterView.OnItemClickListener() {

		@Override
		public void onItemClick(AdapterView<?> adapter, View v, int position, long id) {
			selectedItem = (String) adapter.getItemAtPosition(position);
			pid = ProcessUtils.getProcessPID(selectedItem);
		}
	};
    ```
    
### GT中SM实现的代码分析
 
 - SMActivity：流畅度测试初始的Activity
 
  - 初始化SM
  
 ```
   //检测按钮的触发事件
   View.OnClickListener button_check_status = new View.OnClickListener() {

        @Override
        public void onClick(View v) {
	    // Choreographer 接收到 VSYNC 信号时，Choreographer 会调用 doFrame 函数依次对上述借口进行回调，从而进行渲染
	    //skippedFrames 则记录了 jitterNanos 这段时间 doFrame 错过了多少个 VSYNC 信号，即跳过了多少帧
       //debug.choreographer.skipwarning 来设定SKIPPED_FRAME_WARNING_LIMIT 的数值为1；默认值为30（即当跳帧达到30时才会打印Log，不能满足要求）
          
	  String cmd = "getprop debug.choreographer.skipwarning";
            ProcessBuilder execBuilder = new ProcessBuilder("sh", "-c", cmd);
            execBuilder.redirectErrorStream(true);
            try {
                TextView textview = (TextView) findViewById(R.id.textviewInformation);
                Process p = execBuilder.start();
                InputStream is = p.getInputStream();
                InputStreamReader isr = new InputStreamReader(is);
                BufferedReader br = new BufferedReader(isr);
                Boolean flag = false;
                String line;
                while ((line = br.readLine()) != null) {
		    //判断是否==1
                    if (line.compareTo("1") == 0) {
                        flag = true;
                        break;
                    }
                }

                if (flag) {
                    textview.setText("OK");
                } else {
                    textview.setText("NOT OK");
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    };
    
 ```
 - 开始测试
 
 ```
	//开始测试按钮的事件
	View.OnClickListener onStartClick = new View.OnClickListener() {

		@Override
		public void onClick(View v) {
			if (SMServiceHelper.getInstance().isStarted()) {
				SMServiceHelper.getInstance().stopBackgroundServiceIfRunning(SMActivity.this);
			} else {
				if (null == selectedItem) {
					ToastUtil.ShowLongToast(SMActivity.this, "select a app first!");
				}
				else
				{
          //把当前测试的进程号和进程名作为参数传出去					
          SMServiceHelper.getInstance().startBackgroundService(SMActivity.this, pid, selectedItem);
				}
			}
		}
	};
 ```
  
  - SMServiceHelper：跳转到SMLogService和SMDataService的中间服务
  
  ```
  synchronized void startBackgroundService(Context context, Integer pid, String pkgName) {
		if (! isStarted())
		{
			setStarted(true);
			//通过Intent把传递的参数取出并跳转到SMLogService
      Intent intent = new Intent(context, SMLogService.class);
			intent.putExtra("pid", pid.toString());
			intent.putExtra("pkgName", pkgName);
			context.startService(intent);
			//通过Intent把传递的参数取出并跳转到SMDataService
			Intent intent2 = new Intent(context, SMDataService.class);
			intent2.putExtra("pid", pid.toString());
			intent2.putExtra("pkgName", pkgName);
			context.startService(intent2);
			
			for (SMPluginListener listener : listeners)
			{
				listener.onSMStart();
			}
		}
  ```
   
   - SMLogService：核心代码！通过Choreographer输出的log信息获取到跳帧的次数
   
   ```
   protected void onHandleIntent(Intent intent) {
        try {
            //获取被测app的pid，用于过滤logcat输出的日志，找到被测app的日志
            String str = intent.getStringExtra("pid");
            int pid = Integer.parseInt(str);
            //过滤Choreographer输出的log
            List<String> args = new ArrayList<String>(Arrays.asList("logcat", "-v", "time", "Choreographer:I", "*:S"));
            dumpLogcatProcess = RuntimeHelper.exec(args);
            reader = new BufferedReader(new InputStreamReader(dumpLogcatProcess.getInputStream()), 8192);
            String line;
            while ((line = reader.readLine()) != null && !killed) {//循环读取跳帧日志
                // filter "The application may be doing too much work on its main thread."
                if (!line.contains("uch work on its main t")) {//过滤出跳帧日志
                    continue;
                }
                int pID = LogLine.newLogLine(line, false).getProcessId();
                if (pID != pid){
                    continue;
                }
		//从Log中截取跳帧的数据
                line = line.substring(50, line.length() - 71);
                Integer value = Integer.parseInt(line.trim());
		//把解析出的数值添加到一个阻塞列表里
                SMServiceHelper.getInstance().dataQueue.offer(value);
            }
        } catch (IOException e) {
            Log.e(TAG, e.toString() + "unexpected exception");
        } finally {
            killProcess();
        }
    }
   ```
   
    - SMDataService：核心代码！根据上边得到的跳帧的值计算SM
      - dataCountThread：对上述的跳帧进行求和
    ```
    private Thread dataCountThread = new Thread("SMDataCountThread") {
		@Override
		public void run() {
			while (!pause)
			{
				try {
			//take():取走BlockingQueue里排在首位的对象,若BlockingQueue为空,阻断进入等待状态直到Blocking有新的对象被加入为止
					int value = SMServiceHelper.getInstance().dataQueue.take();
					//使用AtomicInteger这个类进行跳帧求和
					count.addAndGet(value);
				} catch (InterruptedException e) {
					return;
				}
			}
		}
	};
    ```
      - onHandleIntent：循环计算流畅度
      
    ```
         while (true) {
            if (pause) {
                break;
            }
            int x = count.getAndSet(0);
            // 卡顿大于60时，要将之前几次SM计数做修正
            if (x > 60) {
                int n = x / 60;
                int v = x % 60;
                TagTimeEntry tte = OpPerfBridge.getProfilerData(key);
                int len = tte.getRecordSize();
                // 补偿参数
                int p = n;//Math.min(len, n);
                /*
                 * n > len是刚启动测试的情况，日志中的亡灵作祟，这种情况不做补偿;
                 * 并且本次也记为60。本逻辑在两次测试间会清理数据的情况生效。
                 */
                if (n > len) 
                {
                    globalClient.setOutPara(key, 60);
                }
                else
                {
                    for (int i = 0; i < p; i++) {
                        TimeEntry te = tte.getRecord(len - 1 - i);
                        te.reduce = 0;
                    }
                    globalClient.setOutPara(key, v);
                }
            } else {
                int sm = 60 - x;//正常情况下的流畅度值
                globalClient.setOutPara(key, sm);
            }

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    ```
	
### 参考资料
- GT源码下载：https://github.com/TencentOpen/GT
- GT流畅度测试：https://testerhome.com/topics/4770
- 那些年我们用过的显示性能指标：https://segmentfault.com/a/1190000005089412
- BlockingQueue介绍及使用：http://www.cnblogs.com/liangstudyhome/p/4531852.html
- Java 原子操作类详解：http://blog.csdn.net/sunxianghuang/article/details/52277370
  
 
