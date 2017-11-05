## 模拟App卡顿的Demo
 - 影响App性能的因素很多，这次的Demo主要针对在主线程有过多操作的因素进行还原，并进行测试
 - 利用Android自带的数据库SQlite，在UI线程中进行大规模的数据库读写操作，进而测试App的响应性能，关键代码如下：
 
 ```
 //新建数据库
 dbHelper = new MyDatabaseHelper(this,"BookStore.db",null,1);
        createDatabase.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                dbHelper.getWritableDatabase();
            }
        });

        addData.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                SQLiteDatabase db = dbHelper.getWritableDatabase();
                ContentValues values = new ContentValues();
                //循环写入数据到数据库
                for(int i =0; i<20;i++) {
                    values.put("author", "Dan Brown");
                    values.put("price", "16.96");
                    values.put("pages", "454");
                    values.put("name", "The Da Vinci Code");
                    db.insert("Book", null, values);
                }
            }
        });
 ```
## GT测试结果分析
 - 在OPENTHOS上运行Demo，并启用GT的流畅度分析工具，不断点击addData往数据库写入数据可以得到SM的值
 - 在Android Studio中也可以看到Choreographer统计的掉帧Log信息如下：
 
 ```
 4-01 00:58:46.255 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 4 frames!  The application may be doing too much work on its main thread.
04-01 00:58:46.297 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 1 frames!  The application may be doing too much work on its main thread.
04-01 00:58:48.198 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 32 frames!  The application may be doing too much work on its main thread.
04-01 00:58:50.118 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 32 frames!  The application may be doing too much work on its main thread.
04-01 00:58:51.746 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 32 frames!  The application may be doing too much work on its main thread.
04-01 00:58:53.134 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 32 frames!  The application may be doing too much work on its main thread.
04-01 00:58:54.455 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 31 frames!  The application may be doing too much work on its main thread.
04-01 00:58:57.743 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 32 frames!  The application may be doing too much work on its main thread.
04-01 00:58:58.747 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 31 frames!  The application may be doing too much work on its main thread.
04-01 00:58:59.862 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 66 frames!  The application may be doing too much work on its main thread.
04-01 00:59:02.589 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 162 frames!  The application may be doing too much work on its main thread.
04-01 00:59:08.575 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 359 frames!  The application may be doing too much work on its main thread.
04-01 00:59:18.393 3438-3438/com.example.root.gtdatabasetest I/Choreographer: Skipped 588 frames!  The application may be doing too much work on its main thread.

 ```
## 因素分析
 - OPENTHOS自带的有iostat可以检测磁盘的IO性能，iostat -d 1
   - tps：该设备每秒的传输次数
   - kB_read/s：每秒从设备（drive expressed）读取的数据量；
   - kB_wrtn/s：每秒向设备（drive expressed）写入的数据量；
   - kB_read：读取的总数据量；
   - kB_wrtn：写入的总数量数据量；这些单位都为Kilobytes
  
  ```
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda       0.00   0.00           0.00         0          0
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda       89.00   0.00          688.00         0        688
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda      512.00   0.00           3856.00       0       3856
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda       515.00   0.00           3832.00         0     3832
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda       514.00   0.00           3872.00         0      3872
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda       524.00   0.00           3912.00         0      3912
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda       530.00   0.00           3992.00         0       3992
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda       308.00   0.00           2336.00         0        2336
  Device    tps    Blk_read/s     Blk_wrtn/s  Blk_read   Blk_wrtn
  sda       0.00   0.00           0.00         0          0
  ```
  - 以上数据显示在反复点击addData的时候，IO的tps最大值为530，已达到瓶颈
  - 因为iostat只能反应IO的整体性能，并不能确定是哪一个进程导致的IO性能下降，因为利用iotop进一步分析
    - OPENTHOS上安装[iotop](https://forum.xda-developers.com/android/software-hacking/script-iotop-android-t2910428)
        1.下载[iotop.sh](https://github.com/laufersteppenwolf/iotop)
        2.adb push iotop.sh  /system/bin     
        3.运行脚本iotop.sh
    - 得到以下数据,除了被测Demo的Write_speed为3860，其余进程都为0，因此确定IO的瓶颈是由被测Demo造成的
    
    ```
    PID     READ       WRITTEN     READ_SPEED     WRITE_SPEED   PROCESS
    3438    344        74080          0            3860         com.example.root.gtdatabasetest
    ```
    
  ## 存在的问题
   - 因为OPENTHOS自身带的iostat存在问题，可以看到io很多数据的iostat -x参数无法用
   - iotop是自己写的脚本，测试的数据是测试脚本运行的点数据，不能非常的准确体现IO性能
   - 可以利用之前的Ubuntu和OPENTHOS搭一个chroot的环境，利用linux的工具测试OPENTHOS的数据
