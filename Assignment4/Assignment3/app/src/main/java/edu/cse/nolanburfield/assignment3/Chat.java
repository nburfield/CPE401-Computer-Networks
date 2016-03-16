package edu.cse.nolanburfield.assignment3;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.view.ViewGroup.LayoutParams;
import android.widget.TextView;
import android.view.inputmethod.InputMethodManager;
import android.content.Context;
import android.text.method.ScrollingMovementMethod;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;

import javax.crypto.KeyGenerator;


public class Chat extends Activity {

    private DatabaseHandler db = new DatabaseHandler(this);
    private static final String TAG = "chat";
    private String friend_id = "";
    private FriendDB friend = null;
    private Integer counter = 0;
    private AppState global;
    private boolean killthread = false;
    private DatagramSocket serverSocket = null;
    private static Packet result = new Packet("", "", "");
    Thread serverThread = null;
    private Packet message;
    Key symKey;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        TextView reg_id = (TextView) findViewById(R.id.friends);

        List<FriendDB> all = new ArrayList<FriendDB>();
        all = db.getAllFriends();
        String friends = "";
        for (int i = 0; i < all.size(); i++) {
            friends += all.get(i).getName() + "\n";
        }
        reg_id.setText(friends);
        TextView chat = (TextView) findViewById(R.id.chat);
        chat.setMovementMethod(new ScrollingMovementMethod());

        try {
            symKey = KeyGenerator.getInstance("RSA").generateKey();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }

        global  = (AppState)getApplication();
        global.StopThread();

        try {
            serverSocket = new DatagramSocket(global.getPeer_port());
        } catch (IOException e) {
            e.printStackTrace();
        }
        killthread = true;
        this.serverThread = new Thread(new ServerThread());
        this.serverThread.start();

        String[] data;
        data = new String[3];
        if (global.isPacket()) {
            Packet initial = global.getPacket();
            if (initial.getHeader().equals("CHAT")) {
                data = initial.getData().split("%");
                reg_id.setText(data[0]);
                friend_id = data[0];
                friend = db.getFriend(friend_id);
                if (friend == null) {
                    friend_id = "";
                } else {
                    reg_id.setText(friend_id);
                    Button send = (Button) findViewById(R.id.send);
                    send.setText("Send");
                    counter = Integer.parseInt(data[1]);
                    message = new Packet("DELIVERED", global.getUser() + "%" + counter.toString() + "%", "No Content");
                    String send_message = counter + ". " + initial.getBody() + "\n--------------\n";
                    chat.setText(send_message);
                    counter++;

                    String ip = friend.getIp();
                    SendUDPMessage sendMessageTask = new SendUDPMessage();
                    sendMessageTask.execute(ip);
                }
            }
        } else {
            Log.v(TAG, "No Packet");
        }
    }



    public void goBack(View v) {
        this.killthread = false;
        try {
            serverThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        global.StartThread();
        Intent intent = new Intent(this, Home.class);
        startActivity(intent);
    }

    public void onSend(View v) {
        EditText input = (EditText) findViewById(R.id.message);
        TextView chat = (TextView) findViewById(R.id.chat);
        String value = input.getText().toString();
        input.setText("");
        InputMethodManager inputManager = (InputMethodManager)
                getSystemService(Context.INPUT_METHOD_SERVICE);
        inputManager.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(),
                InputMethodManager.HIDE_NOT_ALWAYS);
        if (friend_id == "") {
            friend_id = value;
            friend = db.getFriend(friend_id);
            if (friend == null) {
                friend_id = "";
            }
            else {
                TextView reg_id = (TextView) findViewById(R.id.friends);
                reg_id.setText(friend_id);
                Button send = (Button) findViewById(R.id.send);
                send.setText("Send");
             }
        }
        else {
            message = new Packet("CHAT", global.getUser() + "%" + counter.toString() + "%", value);
            String ip = friend.getIp();
            SendUDPMessage sendMessageTask = new SendUDPMessage();
            sendMessageTask.execute(ip);
            String current_message = chat.getText().toString();
            String send_message = current_message + counter + ". " + value + "\n--------------\n";
            chat.setText(send_message);
            counter++;
        }
    }

    public void runResult() {
        if (!result.getHeader().equals("CHAT")) {
            global.setNeeds_run(result);
            this.goBack(this.getCurrentFocus());
            return;
        }
        TextView chat = (TextView) findViewById(R.id.chat);
        String[] data;
        data = new String[3];
        data = result.getData().split("%");
        if (!data[0].equals(friend_id)) {
            AlertDialog alt_bld = new AlertDialog.Builder(this).create();
            alt_bld.setMessage("Chat from " + data[0] + " received, but data was thrown out.");
            alt_bld.setCancelable(true);
            alt_bld.show();
        }
        else if (counter == Integer.parseInt(data[1])) {
            counter = Integer.parseInt(data[1]) + 1;
            message = new Packet("DELIVERED", global.getUser() + "%" + counter.toString() + "%", "No Content");
            String ip = friend.getIp();
            SendUDPMessage sendMessageTask = new SendUDPMessage();
            sendMessageTask.execute(ip);
            String current_message = chat.getText().toString();
            String send_message = current_message + (counter-1) + ". " + result.getBody() + "\n--------------\n";
            chat.setText(send_message);
        }
        result.clear();
    }

    private class SendUDPMessage extends AsyncTask<String, Void, Void> {

        @Override
        protected Void doInBackground(String... params) {
            try {
                Integer port = global.getPeer_port();
                DatagramSocket client_socket = serverSocket;
                InetAddress IPAddress = InetAddress.getByName(params[0]);
                String value = message.send();
                Log.v(TAG, value);
                byte[] send_data;
                send_data = value.getBytes();
                DatagramPacket send_packet = new DatagramPacket(send_data, value.length(), IPAddress, port);
                Log.v(TAG, "1.");
                client_socket.send(send_packet);
                Log.v(TAG, "2.");
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    class ServerThread extends Thread {
        private boolean bKeepRunning = true;
        private final String TAG = "chat_thread";

        public void run() {
            String message;
            byte[] lmessage = new byte[1024];

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

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_chat, menu);
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
