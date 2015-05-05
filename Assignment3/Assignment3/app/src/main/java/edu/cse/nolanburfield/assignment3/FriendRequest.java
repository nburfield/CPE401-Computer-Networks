package edu.cse.nolanburfield.assignment3;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;
import android.widget.TextView;
import android.view.View;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;


public class FriendRequest extends Activity {

    private AppState global;
    private static final String TAG = "friend_request";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;
    private Packet result;
    byte[] send_data = new byte[1024];
    private DatabaseHandler db = new DatabaseHandler(this);
    private Boolean accept;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_friend_request);
        TextView reg_id = (TextView) findViewById(R.id.request_name);
        global = (AppState)getApplication();
        result = global.getPacket();
        String id = result.getData().replace("%", "");
        reg_id.setText(id);
    }

    public void doAccept(View v) {
        String data = result.getData().replace("%", "") + "%";
        message = new Packet("SEARCH", data, "");
        accept = true;
        SendMessage sendMessageTask = new SendMessage();
        sendMessageTask.execute();
        Intent intent = new Intent(this, Home.class);
        startActivity(intent);
    }

    public void doDeny(View v) {
        String data = result.getData().replace("%", "") + "%";
        message = new Packet("SEARCH", data, "");
        accept = false;
        SendMessage sendMessageTask = new SendMessage();
        sendMessageTask.execute();
        Intent intent = new Intent(this, Home.class);
        startActivity(intent);
    }

    private class SendMessage extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            try {
                String ip = global.getIp();
                Integer port = global.getServer_port();
                client = new Socket(ip, port);
                printwriter = new PrintWriter(client.getOutputStream(), true);
                String value = message.send();
                printwriter.write(value);
                printwriter.flush();

                ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream(1024);
                byte[] buffer = new byte[1024];
                int bytesRead;
                String data = "";
                InputStream inputStream = client.getInputStream();

                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    byteArrayOutputStream.write(buffer, 0, bytesRead);
                    data += byteArrayOutputStream.toString("UTF-8");
                }

                result = new Packet("", "", "");
                result.result(data, ip);
                String [] xml_data;
                xml_data = new String [2];
                xml_data = result.getBody().split("<ip>");
                xml_data = xml_data[1].split("</ip>");
                String discovered_ip = xml_data[0];
                if (discovered_ip != "") {
                    xml_data = result.getBody().split("<user_id>");
                    xml_data = xml_data[1].split("</user_id>");
                    String user_id = xml_data[0];

                    xml_data = result.getBody().split("<public_key>");
                    xml_data = xml_data[1].split("</public_key>");
                    String public_key = xml_data[0];

                    if (accept) {
                        db.addFriend(user_id, 1, discovered_ip, public_key);
                        message = new Packet("CONFIRM", global.getUser() + "%", "");
                    } else {
                        db.addFriend(user_id, 0, discovered_ip, public_key);
                        message = new Packet("REJECT", global.getUser() + "%", "");
                    }

                    port = global.getPeer_port();
                    DatagramSocket client_socket = global.getClientSocket();
                    InetAddress IPAddress =  InetAddress.getByName(discovered_ip);

                    value = message.send();
                    Log.v(TAG, value);
                    send_data = value.getBytes();
                    DatagramPacket send_packet = new DatagramPacket(send_data, value.length(), IPAddress, port);
                    client_socket.send(send_packet);
                }
                Log.v(TAG, discovered_ip);
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

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_friend_request, menu);
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
