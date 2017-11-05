## 目标
- 复现论文的工作
 + 一个apk的Demo
 + 手动添加Log
 + 手动生成Decour库
 
## 工作进展
- 一个Demo，实现简单的异步调用UI更新
- 手动在回调的地方添加Log

### Handler.sendMessage机制的实现
- apk源码如下：
```
public class MainActivity extends Activity implements OnClickListener{

    public static final int UPDATE_TEXT=1;
    private TextView text;
    private Button changeText;
    private Handler handler=new Handler(){
        public void handleMessage(Message msg){
            Log.d("LOG", "upcall start (21)"+Thread.currentThread().getId());
            switch(msg.what){
                case UPDATE_TEXT:
                    text.setText("Nice to meet you");
                    break;
                default:
                    break;
            }
            Log.d("LOG", "upcall end (21)"+Thread.currentThread().getId());
        }
    };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        text=(TextView)findViewById(R.id.text);
        changeText=(Button)findViewById(R.id.change_text);
        changeText.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        // TODO Auto-generated method stub
        new Thread(new Runnable(){
            @Override
            public void run() {
                // TODO Auto-generated method stub
                Message message=new Message();
                message.what=UPDATE_TEXT;
                Log.d("LOG", "call start(13)"+Thread.currentThread().getId());
                Detour dt=DetourFactory.getDetour(handler,13);
                dt.message=message;
                dt.cb();
                Log.d("LOG","call end(13)"+Thread.currentThread().getId());
            }

        }).start();
    }
}
```
- 手动生成Decour库，可以对回调函数进行绕行，源码如下：
```
public class Detour {

    private Handler handler;
    private int matchId;
    Message message=new Message();
    public Detour(Handler handler,int matchId){
        this.handler=handler;
        this.matchId=matchId;
    }
     public  void cb(){
         Log.d("LOG", "callback start ("+matchId+")"+Thread.currentThread().getId());
        handler.sendMessage(message);
    }
}


public class DetourFactory {
    public static Detour getDetour(Handler handler,int callId){
        int matchId=new Random().nextInt(10)+1;
        Log.d("LOG", "async start ("+callId+","+matchId+")"+Thread.currentThread().getId());
        return new Detour(handler,matchId);
    }

}
```
- 打印结果的Log如下：
```
02-24 10:59:29.221 23537-29364/com.example.root.sendmessagetest D/LOG: call start(13)179
02-24 10:59:29.307 23537-23546/com.example.root.sendmessagetest W/art: Suspending all threads took: 23.244ms
02-24 10:59:29.319 23537-29364/com.example.root.sendmessagetest D/LOG: async start (13,6)179
02-24 10:59:29.326 23537-29364/com.example.root.sendmessagetest D/LOG: callback start (6)179
02-24 10:59:29.326 23537-29364/com.example.root.sendmessagetest D/LOG: call end(13)179
02-24 10:59:29.660 23537-23537/com.example.root.sendmessagetest D/LOG: upcall start (21)1
02-24 10:59:29.663 23537-23537/com.example.root.sendmessagetest D/LOG: upcall end (21)1
```
### Thread和Handle.post机制的实现
- apk源码如下：
```
public  class MainActivity extends Activity implements OnClickListener{

    private TextView textView;
    private Button button;
    private Handler myHandler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        textView=(TextView)findViewById(R.id.text_view);
        button=(Button)findViewById(R.id.button);
        button.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        Log.d("LOG", "call start (7)"+Thread.currentThread().getId());
        // thraed机制额绕行实现 
        ThreadDetour dt=ThreadDetourFactory.getThreadDetour(new MyThread(),7);
        dt.Thdt();
        Log.d("LOG", "call end (7)"+Thread.currentThread().getId());
    }

    public class MyThread extends Thread{
        public void run(){
            Log.d("LOG", "upcall start (19)"+Thread.currentThread().getId());
            try {

                sleep(10*1000);

            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            Runnable runnable=new Runnable(){

                @Override
                public void run() {
                    Log.d("LOG", "callup start(21);"+Thread.currentThread().getId());
                    // TODO Auto-generated method stub
                    textView.setText("after update");
                    Log.d("LOG", "callup end(21);"+Thread.currentThread().getId());
                }

            };
            Log.d("LOG", "call start(13);"+Thread.currentThread().getId());
            //Runnable机制的实现
            RunnableDetour dt=RunnableDetourFactory.getDetour(runnable,13);
            Log.d("LOG", "call end(13);"+Thread.currentThread().getId());
            Log.d("LOG", "upcall end (19)"+Thread.currentThread().getId());
        }
    }
}
```
- 手动生成Decour库，可以对回调函数进行绕行，源码如下：
```
public class ThreadDetour {
    private Thread thread1;
    private Thread thread;
    private int matchId;
    public ThreadDetour(Thread t, int matchId) {
        // TODO Auto-generated constructor stub
        this.thread=t;
        this.matchId=matchId;
    }
    void Thdt(){
        Log.d("LOG", "callback start ("+matchId+")"+Thread.currentThread().getId());
        thread.start();
    }
}

public class ThreadDetourFactory {
    public static ThreadDetour getThreadDetour(Thread t,int callId) {
        // TODO Auto-generated method stub
        int matchId=new Random().nextInt(10)+1;
        Log.d("LOG", "async start ("+callId+","+matchId+")"+Thread.currentThread().getId());
        return new ThreadDetour(t,matchId);
    }
}


public class RunnableDetour {
    int matchId;
    Runnable r;
    Runnable r1 = new Runnable(){
        @Override
        public void run() {
            // TODO Auto-generated method stub
            Log.d("LOG", "callback start,"+"("+matchId+");"+Thread.currentThread().getId());
            r.run();
        }
    };

    public RunnableDetour(Runnable r,int matchId){
        this.r=r;
        this.matchId=matchId;
    }
}


public class RunnableDetourFactory {
    public static RunnableDetour getDetour(Runnable r,int callId){
        //生成１到１０随机数
        int matchId=new Random().nextInt(10)+1;
        Log.d("LOG", "AsyncStart,"+"("+callId+","+matchId+");"+Thread.currentThread().getId());
        return new RunnableDetour(r,matchId);
    }
}

```

- 打印结果的Log如下：
```
02-24 11:04:43.332 31300-31300/com.example.root.threadtest D/LOG: call start (7)1
02-24 11:04:43.751 31300-31300/com.example.root.threadtest D/LOG: async start (7,7)1
02-24 11:04:43.755 31300-31300/com.example.root.threadtest D/LOG: callback start (7)1
02-24 11:04:43.756 31300-31300/com.example.root.threadtest D/LOG: call end (7)1
02-24 11:04:43.776 31300-2752/com.example.root.threadtest D/LOG: upcall start (19)185
02-24 11:04:53.825 31300-2752/com.example.root.threadtest D/LOG: call start(13);185
02-24 11:04:53.889 31300-2752/com.example.root.threadtest D/LOG: AsyncStart,(13,8);185
02-24 11:04:53.908 31300-2752/com.example.root.threadtest D/LOG: call end(13);185
02-24 11:04:53.909 31300-2752/com.example.root.threadtest D/LOG: upcall end (19)185
02-24 11:04:53.951 31300-31300/com.example.root.threadtest D/LOG: callback start,(8);1
02-24 11:04:53.951 31300-31300/com.example.root.threadtest D/LOG: callup start(21);1
02-24 11:04:53.963 31300-31300/com.example.root.threadtest D/LOG: callup end(21);1
```
## 存在的问题
- Android异步编程还有一个AsyncTask，Android对它的封装几乎完美，暂时未找到进行绕行的方法
- Runnable机制进行绕行的时候需要新建立一个对象，会比较浪费资源并且影响性能
