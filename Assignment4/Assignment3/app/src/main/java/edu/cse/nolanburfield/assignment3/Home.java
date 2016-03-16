package edu.cse.nolanburfield.assignment3;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.app.AlertDialog.Builder;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

public class Home extends Activity {

    private static final String TAG = "home";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;
    private DatabaseHandler db = new DatabaseHandler(this);
    private AppState global;
    private Packet result;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        final TextView reg_id = (TextView) findViewById(R.id.user_id);
        global  = (AppState)getApplication();

        if (!global.isLoggedIn()) {
            Intent intent = new Intent(this, Login.class);
            startActivity(intent);
        }
        reg_id.setText(global.getUser());

        if (!global.ThreadRunning()) {
            global.StartThread();
        }

        this.onRefresh(this.getCurrentFocus());
    }

    @Override
    protected void onStop() {
        super.onStop();
    }

    private void runResult() {
        String value = global.getPacketHeader();
        Log.v(TAG, value);
        if (value.equals("FRIEND")) {
            Intent intent = new Intent(this, FriendRequest.class);
            startActivity(intent);
        } else if (value.equals("CHAT")) {
            Intent intent = new Intent(this, Chat.class);
            startActivity(intent);
        }
    }

    public void onLoggout(View v) {
        AppState global = (AppState)getApplication();
        global.UserPrivateKey = null;
        String data = global.getUser() + "%";
        message = new Packet("QUIT", data, "");
        SendMessage sendMessageTask = new SendMessage();
        sendMessageTask.execute();
        global.setLoggedOut();
        Intent intent = new Intent(this, Login.class);
        startActivity(intent);
    }

    public void performUpdate(View v) {
        Intent intent = new Intent(this, Update.class);
        startActivity(intent);
    }

    public void performSearch(View v) {
        Intent intent = new Intent(this, Search.class);
        startActivity(intent);
    }

    public void onRefresh(View v) {
        if (global.isPacket()) {
            this.runResult();
        }

        String alert_message = global.getAlert_message();
        if (!alert_message.equals("")) {
            AlertDialog alt_bld = new AlertDialog.Builder(this).create();
            alt_bld.setMessage(alert_message);
            alt_bld.setCancelable(true);
            alt_bld.show();
        }
    }

    public void performFriend(View v) {
        Intent intent = new Intent(this, Friend.class);
        startActivity(intent);
    }

    public void performHi(View v) {
        List<FriendDB> all = new ArrayList<FriendDB>();
        all = db.getAllFriends();
        for (int i = 0; i < all.size(); i++) {
            String ip = all.get(i).getIp();
            SendUDPMessage sendMessageTask = new SendUDPMessage();
            sendMessageTask.execute(ip);
        }
    }

    public void performChat(View v) {
        Intent intent = new Intent(this, Chat.class);
        startActivity(intent);
    }

    public void performPost(View v) {
        Intent intent = new Intent(this, Post.class);
        startActivity(intent);
    }

    public void performEntries(View v) {
        Intent intent = new Intent(this, Entries.class);
        startActivity(intent);
    }

    private class SendMessage extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            try {
                AppState global = (AppState)getApplication();
                String ip = global.getIp();
                Integer port = global.getServer_port();
                client = new Socket(ip, port);
                printwriter = new PrintWriter(client.getOutputStream(), true);
                String value = global.encryptServerPublic(message.send());
                printwriter.write(value);
                printwriter.flush();
                printwriter.close();
                client.close();
            } catch (UnknownHostException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    private class SendUDPMessage extends AsyncTask<String, Void, Void> {

        @Override
        protected Void doInBackground(String... params) {
            try {
                Integer port = global.getPeer_port();
                DatagramSocket client_socket = global.getClientSocket();
                InetAddress IPAddress = InetAddress.getByName(params[0]);
                message = new Packet("HI", global.getUser() + "%", "");
                String value = message.send();
                Log.v(TAG, value);
                byte[] send_data = new byte[1024];
                send_data = value.getBytes();
                DatagramPacket send_packet = new DatagramPacket(send_data, value.length(), IPAddress, port);
                client_socket.send(send_packet);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_home, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
