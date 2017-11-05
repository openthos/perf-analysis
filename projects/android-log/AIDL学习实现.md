## AIDL介绍
 - aidl是 Android Interface definition language的缩写，一看就明白，它是一种android内部进程通信接口的描述语言，通过它我们可以定义进程间的通信接口
## AIDL实现例子
 - 创建一个AIDL接口，myAIDL.aidl,并写入自己要在进程间通信用的抽象方法

```
package com.example.root.aidltest;

// Declare any non-default types here with import statements

interface myAIDL {

    void testMethod();
}
```
 - 创建一个远程Service，在Service中创建一个类继承AIDL接口中的Stub类并实现Stub中的抽象方法，最后在onBind中返回这个类的对象
 
```
package com.example.root.aidltest;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;

public class AIDLRemoteService extends Service {


    private static final String TAG = "AIDLRemoteService";

    private final myAIDL.Stub mBinder=new myAIDL.Stub(){
        @Override
        public void testMethod() throws RemoteException {
            Log.d(TAG, "testMethod: "+android.os.Process.myPid()+"this is myAIDLTest");
        }
    };

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        return  mBinder;
    }
}

```
 - 在要调用的地方：MainActivity绑定该Service，将Service返回的Binder对象转换成AIDL接口所属的类型，接着直接调用AIDL的方法
 
 ```
 package com.example.root.aidltest;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.os.RemoteException;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private Button btnBindService;
    private Button btnStartMethod;

    private myAIDL mMyAIDL;
    private ServiceConnection mServiceConnection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            Log.e(TAG, "onServiceConnected");
            mMyAIDL = myAIDL.Stub.asInterface(service);
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
            Log.e(TAG, "onServiceDisconnected");
            mMyAIDL = null;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d("bbbbbbbbbbbb", "testMethod: "+android.os.Process.myPid()+"this is myAIDLTest");
        initView();
    }

    private void initView() {
        btnBindService = (Button) findViewById(R.id.button1);
        btnStartMethod = (Button) findViewById(R.id.button2);
        btnBindService.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, AIDLRemoteService.class);
                bindService(intent, mServiceConnection, Context.BIND_AUTO_CREATE);
            }
        });

        btnStartMethod.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("aaaaaaaaaaaaa", "testMethod: "+android.os.Process.myPid()+"this is myAIDLTest");

                try {
                    mMyAIDL.testMethod();
                } catch (RemoteException e) {
                    Toast.makeText(MainActivity.this, "服务被异常杀死，请重新开启。", Toast.LENGTH_SHORT).show();
                }

            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unbindService(mServiceConnection);
    }
}
 ```
 
  - 在AndroidManifest中添加服务，其中关键的是android:process=":remote"，其中进程名以“:”开头的进程属于当前应用的私有进程，其他应用的组件不可以和它跑在同一个进程中，从而实现跨进程进行通讯
 
 ```
  <service android:name=".AIDLRemoteService"  
            android:process=":remote"/> 
 ```
 ## 实验结果
  - log信息如下
 
 ```
04-13 07:19:11.150 8891-8891/com.example.root.aidltest D/bbbbbbbbbbbb: testMethod: 8891this is myAIDLTest
04-13 07:19:20.567 8891-8891/com.example.root.aidltest D/aaaaaaaaaaaaa: testMethod: 8891this is myAIDLTest
04-13 07:19:20.569 9055-9069/com.example.root.aidltest:remote D/AIDLRemoteService: testMethod: 9055this is myAIDLTest

 ```
