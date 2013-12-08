package so.libsora.latency_benchmark_android;

import android.util.Log;

public class ThreadSocketServer implements IServer {
    public static final String TAG = "Thread Socket Server";
    
    // handle only one to one connection
    Thread thread;
    IServerRunnable runnable;
    
    public ThreadSocketServer(IServerRunnable runnable) {
        this.runnable = runnable;
    }
    
    @Override
    public boolean start() {
        if(thread == null) {
            thread = new Thread(runnable);
            thread.start();
            Log.v(TAG, "Server Start");
            return true;
        }
        return false;
    }
    @Override
    public boolean stop() {
        if(thread != null) {
            thread.interrupt();
            thread = null;
            runnable.close();
            Log.v(TAG, "Server Stop");
            return true;
        }   
        return false;
    }
}
