package edu.cse.nolanburfield.assignment3;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.net.DatagramSocket;
import java.net.DatagramPacket;
import java.net.InetAddress;

public class Friend extends Activity {

    private static final String TAG = "friend";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;
    private Packet result;
    byte[] send_data = new byte[1024];
    private DatabaseHandler db = new DatabaseHandler(this);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_friend);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_friend, menu);
        return true;
    }

    public void onRequest(View v) {
        final EditText keyword = (EditText) findViewById(R.id.request);
        String data = keyword.getText().toString() + "%";
        message = new Packet("SEARCH", data, "");
        SendMessage sendMessageTask = new SendMessage();
        sendMessageTask.execute();
        Intent intent = new Intent(this, Home.class);
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
                String value = message.send();
                //Log.v(TAG, value);
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

                    db.addFriend(user_id, 0, discovered_ip, public_key);
                    port = global.getPeer_port();
                    DatagramSocket client_socket = new DatagramSocket(port);
                    InetAddress IPAddress =  InetAddress.getByName(discovered_ip);
                    message = new Packet("FRIEND", global.getUser() + "%", "");
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
