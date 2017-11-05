## AsyncTask概述
 - Android异步消息的一种处理机制，是Thread + Handler的一种方式。一般使用AsyncTask需要重写一下四个方法：onPreExecute()、doInBackground(Params...)、onProgressUpdate(Progress...)、onPostExecute(Result)
 
## AsyncTask基本用法
 - AsyncTask是一个抽象类，所以如果我们想使用它，就必须要创建一个子类去继承它。在继承时我们可以为AsyncTask类指定三个泛型参数，这三个参数的用途如下：
  - Params：在执行AsyncTask时需要传入的参数，可用于在后台任务中使用
  - Progress：后台任何执行时，如果需要在界面上显示当前的进度，则使用这里指定的泛型作为进度单位
  - Result：当任务执行完毕后，如果需要对结果进行返回，则使用这里指定的泛型作为返回值类型
 - 重写AsyncTask中的几个方法才能完成对任务的定制。经常需要去重写的方法有以下四个：
  - onPreExecute()：这个方法会在后台任务开始执行之间调用，用于进行一些界面上的初始化操作，比如显示一个进度条对话框等
  - doInBackground(Params...)：这个方法中的所有代码都会在子线程中运行，我们应该在这里去处理所有的耗时任务。任务一旦完成就可以通过return语句来将任务的执行结果进行返回，如果AsyncTask的第三个泛型参数指定的是Void，就可以不返回任务执行结果。注意，在这个方法中是不可以进行UI操作的，如果需要更新UI元素，比如说反馈当前任务的执行进度，可以调用publishProgress(Progress...)方法来完成
  - onProgressUpdate(Progress...)：当在后台任务中调用了publishProgress(Progress...)方法后，这个方法就很快会被调用，方法中携带的参数就是在后台任务中传递过来的。在这个方法中可以对UI进行操作，利用参数中的数值就可以对界面元素进行相应的更新
  - onPostExecute(Result)：当后台任务执行完毕并通过return语句进行返回时，这个方法就很快会被调用。返回的数据会作为参数传递到此方法中，可以利用返回的数据来进行一些UI操作，比如说提醒任务执行的结果，以及关闭掉进度条对话框等
 - 小例子源码如下：
```
class DownloadTask extends AsyncTask<Void, Integer, Boolean> {  
  
    @Override  
    protected void onPreExecute() {  
        progressDialog.show();  
    }  
  
    @Override  
    protected Boolean doInBackground(Void... params) {  
        try {  
            while (true) {  
                int downloadPercent = doDownload();  
                publishProgress(downloadPercent);  
                if (downloadPercent >= 100) {  
                    break;  
                }  
            }  
        } catch (Exception e) {  
            return false;  
        }  
        return true;  
    }  
  
    @Override  
    protected void onProgressUpdate(Integer... values) {  
        progressDialog.setMessage("当前下载进度：" + values[0] + "%");  
    }  
  
    @Override  
    protected void onPostExecute(Boolean result) {  
        progressDialog.dismiss();  
        if (result) {  
            Toast.makeText(context, "下载成功", Toast.LENGTH_SHORT).show();  
        } else {  
            Toast.makeText(context, "下载失败", Toast.LENGTH_SHORT).show();  
        }  
    }  
}  
```
  
## AsyncTask源码解析
 - 在上述的例子中，可以看到继承AsyncTask，我们先看AsyncTask的源码,实际上并没有任何具体的逻辑会得到执行，只是初始化了两个变量，mWorker和mFuture，并在初始化mFuture的时候将mWorker作为参数传入。
 mWorker是一个Callable对象，mFuture是一个FutureTask对象，这两个变量会暂时保存在内存中，稍后才会用到它们
 
 ```
 public AsyncTask() {  
    mWorker = new WorkerRunnable<Params, Result>() {  
        public Result call() throws Exception {  
            mTaskInvoked.set(true);  
            Process.setThreadPriority(Process.THREAD_PRIORITY_BACKGROUND);  
            return postResult(doInBackground(mParams));  
        }  
    };  
    mFuture = new FutureTask<Result>(mWorker) {  
        @Override  
        protected void done() {  
            try {  
                final Result result = get();  
                postResultIfNotInvoked(result);  
            } catch (InterruptedException e) {  
                android.util.Log.w(LOG_TAG, e);  
            } catch (ExecutionException e) {  
                throw new RuntimeException("An error occured while executing doInBackground()",  
                        e.getCause());  
            } catch (CancellationException e) {  
                postResultIfNotInvoked(null);  
            } catch (Throwable t) {  
                throw new RuntimeException("An error occured while executing "  
                        + "doInBackground()", t);  
            }  
        }  
    };  
}  
 ```
 - 启动某一个任务，就需要调用该任务的execute()方法，因此现在我们来看一看execute()方法的源码,在其中仅仅调用了executeOnExecutor()方法
 
 ```
 public final AsyncTask<Params, Progress, Result> execute(Params... params) {  
    return executeOnExecutor(sDefaultExecutor, params);  
}  
 ```
 - 我们接着看executeOnExecutor()方法，在里面调用了onPreExecute()方法，因此证明了onPreExecute()方法会第一个得到执行。并将我们传入的参数赋值给了mWorker.mParams，
 然后执行exec.execute(mFuture)

```
 public final AsyncTask<Params, Progress, Result> executeOnExecutor(Executor exec,  
        Params... params) {  
    if (mStatus != Status.PENDING) {  
        switch (mStatus) {  
            case RUNNING:  
                throw new IllegalStateException("Cannot execute task:"  
                        + " the task is already running.");  
            case FINISHED:  
                throw new IllegalStateException("Cannot execute task:"  
                        + " the task has already been executed "  
                        + "(a task can be executed only once)");  
        }  
    }  
    mStatus = Status.RUNNING;  
    onPreExecute();  
    mWorker.mParams = params;  
    exec.execute(mFuture);  
    return this;  
}  
 ``` 
 - mWorker的初始化
  
  ```
  private static abstract class WorkerRunnable<Params, Result> implements Callable<Result> {  
        Params[] mParams;  
}  
  ```
 - 看到是Callable的子类，且包含一个mParams用于保存我们传入的参数,这一步就到了AsyncTask初始化的时候，mWorker的调用过程,在此调用doInBackground(mParams)，并将返回值传给postResult
  
  ```
  public AsyncTask() {  
        mWorker = new WorkerRunnable<Params, Result>() {  
            public Result call() throws Exception {  
                mTaskInvoked.set(true);  
  
                Process.setThreadPriority(Process.THREAD_PRIORITY_BACKGROUND);  
                //noinspection unchecked  
                return postResult(doInBackground(mParams));  
            }  
        };  
//….  
          
}  
  ```
 - postResult中出现了我们熟悉的异步消息机制，传递了一个消息message, message.what为MESSAGE_POST_RESULT；message.object= new AsyncTaskResult(this,result)
  
  ```
  private Result postResult(Result result) {  
        @SuppressWarnings("unchecked")  
        Message message = sHandler.obtainMessage(MESSAGE_POST_RESULT,  
                new AsyncTaskResult<Result>(this, result));  
        message.sendToTarget();  
        return result;  
}  
  ```
 - AsyncTaskResult就是一个简单的携带参数的对象,因此在某处肯定存在一个sHandler，且复写了其handleMessage方法等待消息的传入，以及消息的处理;
  可以看到，在接收到MESSAGE_POST_RESULT消息时，执行了result.mTask.finish(result.mData[0]);其实就是我们的AsyncTask.this.finish(result)

```
 private static final InternalHandler sHandler = new InternalHandler();  
    private static class InternalHandler extends Handler {  
        @SuppressWarnings({"unchecked", "RawUseOfParameterizedType"})  
        @Override  
        public void handleMessage(Message msg) {  
            AsyncTaskResult result = (AsyncTaskResult) msg.obj;  
            switch (msg.what) {  
                case MESSAGE_POST_RESULT:  
                    // There is only one result  
                    result.mTask.finish(result.mData[0]);  
                    break;  
                case MESSAGE_POST_PROGRESS:  
                    result.mTask.onProgressUpdate(result.mData);  
                    break;  
            }  
        }  
}  
 ```
 - finish方法中如果我们调用了cancel()则执行onCancelled回调；正常执行的情况下调用我们的onPostExecute(result);主要这里的调用是在handler的handleMessage中，所以是在UI线程中,最后将状态置为FINISHED
 
 ```
 private void finish(Result result) {  
        if (isCancelled()) {  
            onCancelled(result);  
        } else {  
            onPostExecute(result);  
        }  
        mStatus = Status.FINISHED;  
    }  
 ```
 
