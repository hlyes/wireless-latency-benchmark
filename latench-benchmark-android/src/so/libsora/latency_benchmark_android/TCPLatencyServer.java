package so.libsora.latency_benchmark_android;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;

import android.util.Log;

public class TCPLatencyServer implements IServerRunnable {
    public static final String TAG = "TCPServer";
    
    ServerSocket serverSocket;
    boolean running = true;
    
    @Override
    public void run() {
        running = true;
        try {
            serverSocket = new ServerSocket(ServerConfig.PORT);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        while(running) {
            Socket socket = null;
            try {
                socket = serverSocket.accept();
                
                OutputStream out = socket.getOutputStream();
                InputStream in = socket.getInputStream();
                DataOutputStream dos = new DataOutputStream(out);
                DataInputStream dis = new DataInputStream(in);
                
                boolean running = true;
                while(running) {
                    String line = dis.readLine();
                    if(line != null) {
                        dos.writeBytes(line);
                        dos.flush();
                    } else {
                        break;
                    }
                }
                
                dos.close();
                dis.close();
                socket.close();
            } catch (SocketException e) {
                Log.v(TAG, e.getClass().getName() + ':' + e.getMessage());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    
    @Override
    public void close() {
        try {
            serverSocket.close();
            running = false;
        } catch(IOException e) {
            e.printStackTrace();
        }
    }
}
