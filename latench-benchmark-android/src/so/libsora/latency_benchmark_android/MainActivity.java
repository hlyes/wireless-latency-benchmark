
package so.libsora.latency_benchmark_android;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.view.View.OnClickListener;

public class MainActivity extends Activity {
    
    LogView logView;
    
    ThreadSocketServer tcpServer;
    ThreadSocketServer udpServer;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        NetworkHelper networkHelper = new NetworkHelper(this);
        TextView ipTextView = (TextView)findViewById(R.id.ipTextView);
        ipTextView.setText(networkHelper.getIP());
        
        ListView listView = (ListView)findViewById(R.id.logListView);
        logView = new LogView(this, listView);
        
        Button tcpStartButton = (Button)findViewById(R.id.tcpStartButton);
        Button tcpStopButton = (Button)findViewById(R.id.tcpStopButton);
        Button udpStartButton = (Button)findViewById(R.id.udpStartButton);
        Button udpStopButton = (Button)findViewById(R.id.udpStopButton);
        Button btStartButton = (Button)findViewById(R.id.btStartButton);
        Button btStopButton = (Button)findViewById(R.id.btStopButton);
        
        tcpStartButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                udpServer.stop();
                
                boolean success = tcpServer.start();
                if(success) {
                    logView.add(new LogRow("TCP Start"));
                }
            }
        });
        tcpStopButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                udpServer.stop();
                
                boolean success = tcpServer.stop();
                if(success) {
                    logView.add(new LogRow("TCP Stop"));
                }
            }
        });
        
        udpStartButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                tcpServer.stop();
                
                boolean success = udpServer.start();
                if(success) {
                    logView.add(new LogRow("UDP Start"));
                }
            }
        });
        udpStopButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                tcpServer.stop();
                
                boolean success = udpServer.stop();
                if(success) {
                    logView.add(new LogRow("UDP Stop"));
                }
            }
        });
        
        btStartButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                logView.add(new LogRow("Bluetooth Start"));
            }
        });
        btStopButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                logView.add(new LogRow("Bluetooth Stop"));
            }
        });
        
        tcpServer = new ThreadSocketServer(new TCPLatencyServer());
        udpServer = new ThreadSocketServer(new UDPLatencyServer());        
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
    
    @Override
    protected void onPause() {
        super.onPause();
        stopAllServer();
    }
    
    public void stopAllServer() {
        tcpServer.stop();
        udpServer.stop();
    }
}
