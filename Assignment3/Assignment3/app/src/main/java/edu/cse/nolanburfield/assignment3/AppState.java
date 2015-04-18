package edu.cse.nolanburfield.assignment3;

import android.app.AlertDialog;
import android.app.Application;
import android.content.Intent;
import android.os.AsyncTask;
import android.util.Log;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.io.IOException;
import java.net.SocketTimeoutException;

/**
 * Created by nolanburfield on 4/13/15.
 */
public class AppState extends Application {

    private static final String TAG = "thread";
    private boolean loggedin = false;
    private String user_id = "";
    private String ip = "192.168.1.193";
    private Integer server_port = 5000;
    private Integer peer_port = 5005;
    private static Packet result = new Packet("", "", "");
    private static Packet needs_run = new Packet("", "", "");
    Thread serverThread = null;
    private boolean killthread = false;
    private DatabaseHandler db = new DatabaseHandler(this);
    private String alert_message = "";
    private Packet message;

    private DatagramSocket serverSocket = null;

    public boolean isLoggedIn() {
        return loggedin;
    }

    public void setLoggedOut() {
        loggedin = false;
        user_id = "";
    }

    public void setLoggedIn(String id) {
        loggedin = true;
        user_id = id;
    }
    public String getUser() {
        if (loggedin) {
            return user_id;
        }
        return "No User";
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public String getIp() {
        return this.ip;
    }

    public void setServer_port(Integer port) {
        this.server_port = port;
    }

    public Integer getServer_port() {
        return this.server_port;
    }

    public void setPeer_port(Integer port) {
        this.peer_port = port;
    }

    public Integer getPeer_port() {
        return this.peer_port;
    }

    public void StartThread() {
        this.serverThread = new Thread(new ServerThread());
        this.serverThread.start();
        killthread = true;
    }

    public void StopThread() {
        killthread = false;
        try {
            this.serverThread.join();
        } catch (InterruptedException e) {
            //e.printStackTrace();
        }
    }

    public boolean ThreadRunning() {
        return killthread;
    }

    public boolean isPacket() {
        return needs_run.isMessage();
    }

    public Packet getPacket() {
        Packet return_val = new Packet(needs_run);
        needs_run.clear();
        return return_val;
    }

    public String getPacketHeader() {
        return needs_run.getHeader();
    }

    public String getAlert_message() {
        String temp = alert_message;
        alert_message = "";
        return temp;
    }

    public DatagramSocket getClientSocket() {
        return serverSocket;
    }

    private class SendUDPMessage extends AsyncTask<String, Void, Void> {

        @Override
        protected Void doInBackground(String... params) {
            try {
                Integer port = getPeer_port();
                DatagramSocket client_socket = serverSocket;
                InetAddress IPAddress = InetAddress.getByName(params[0]);
                String value = message.send();
                Log.v(TAG, value);
                byte[] send_data;
                send_data = value.getBytes();
                DatagramPacket send_packet = new DatagramPacket(send_data, value.length(), IPAddress, port);
                client_socket.send(send_packet);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    class ServerThread extends Thread {
        private boolean bKeepRunning = true;
        private final String TAG = "thread";

        public void run() {
            String message;
            byte[] lmessage = new byte[1024];

            try {
                serverSocket = new DatagramSocket(getPeer_port());
            } catch (IOException e) {
                e.printStackTrace();
            }

            DatagramPacket packet = new DatagramPacket(lmessage, lmessage.length);
            while(killthread) {
                try {
                    serverSocket.setSoTimeout(10000);
                    serverSocket.receive(packet);
                    if (packet.getLength() != 0) {
                        message = new String(lmessage, 0, packet.getLength());
                        result.result(message, packet.getAddress().getHostAddress());
                        runResult();
                        Log.v(TAG, "Recieved UDP from " + packet.getAddress().getHostAddress());
                        Log.v(TAG, message);
                    }
                } catch (SocketTimeoutException e) {
                    //e.printStackTrace();
                } catch (Throwable e) {
                    Log.v(TAG, "Throwable");
                    //e.printStackTrace();
                }
            }

            if (serverSocket != null) {
                serverSocket.close();
                serverSocket = null;
            }
        }

        public void kill() {
            bKeepRunning = false;
        }
    }

    private void runResult() {
        Log.v(TAG, result.getHeader());
        if (result.getHeader().equals("CONFIRM")) {
            Log.v(TAG, "Running friend confirm.");
            this.runFriendConfirm();
        } else if (result.getHeader().equals("REJECT")) {
            Log.v(TAG, "Running friend deny.");
            this.runFriendDeny();
        } else if (result.getHeader().equals("FRIEND")) {
            Log.v(TAG, "Running friend request.");
            needs_run = new Packet(result);
        } else if (result.getHeader().equals("CHAT")) {
            Log.v(TAG, "Recieved Chat Request.");
            needs_run = new Packet(result);
        } else if (result.getHeader().equals("HI")) {
            Log.v(TAG, "Recieved HI Request.");
            this.runHi();
        }
        result.clear();
    }

    public void setNeeds_run(Packet p) {
        needs_run = new Packet(p);
    }

    private void runFriendConfirm() {
        FriendDB confirm;
        String id = result.getData().replace("%", "");
        confirm = db.getFriend(id);
        confirm.setAccepted(1);
        db.updateFriend(confirm);
        alert_message = "Got a confirm from " + confirm.getName();
    }

    private void runFriendDeny() {
        FriendDB deny;
        String id = result.getData().replace("%", "");
        deny = db.getFriend(id);
        deny.setAccepted(0);
        db.updateFriend(deny);
        alert_message = "Got a deny from " + deny.getName();
    }

    private void runHi() {
        FriendDB hi;
        String id = result.getData().replace("%", "");
        hi = db.getFriend(id);
        hi.setIp(result.getIP());
        db.updateFriend(hi);
        alert_message = "Got a HI from " + hi.getName() + " at IP " + hi.getIp();
    }

}