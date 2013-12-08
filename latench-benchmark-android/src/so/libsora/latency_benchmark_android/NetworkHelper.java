package so.libsora.latency_benchmark_android;

import android.app.Activity;
import android.content.Context;
import android.net.wifi.WifiManager;
import android.text.format.Formatter;

public class NetworkHelper {
    private Activity activity;
    public NetworkHelper(Activity activity) {
        this.activity = activity;
    }
    
    public String getIP() {
        //http://stackoverflow.com/questions/13406180/how-to-get-local-ip-and-display-it-in-textview
        String IP;
        WifiManager wim = (WifiManager) activity.getSystemService(Context.WIFI_SERVICE);
        //List<WifiConfiguration> l =  wim.getConfiguredNetworks(); 
        //WifiConfiguration wc = l.get(0);
        IP = Formatter.formatIpAddress(wim.getConnectionInfo().getIpAddress());
        return IP;
    }
}
