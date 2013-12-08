package so.libsora.latency_benchmark_android;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

import android.util.Log;

public class UDPLatencyServer implements IServerRunnable {
    public static final String TAG = "UDPServer";    
    DatagramSocket socket;
    
    @Override
    public void run() {
        byte[] recvData = new byte[256];
        
        try {
            InetAddress serverAddr = InetAddress.getByName("0.0.0.0");
            socket = new DatagramSocket(ServerConfig.PORT, serverAddr);
            
            while(true) {
                DatagramPacket recvPacket = new DatagramPacket(recvData, recvData.length);
                socket.receive(recvPacket);
                
                InetAddress clientAddr = recvPacket.getAddress();
                int clientPort = recvPacket.getPort();
                DatagramPacket sendPacket = createLatencyPacket(clientAddr, clientPort, recvPacket);
                socket.send(sendPacket);
            }            
        } catch (Exception e) {
            Log.v(TAG, e.getClass().getName() + ':' + e.getMessage());
        } finally {
            close();
        }
    }
    
    public DatagramPacket createLatencyPacket(InetAddress addr, int port, DatagramPacket recvPacket) {
        byte[] data = recvPacket.getData();
        int length = recvPacket.getLength();
        DatagramPacket packet = new DatagramPacket(data, length, addr, port);
        return packet;
    }
    
    @Override
    public void close() {
        if(socket != null) {
            socket.close();
        }
        socket = null;
    }
}
