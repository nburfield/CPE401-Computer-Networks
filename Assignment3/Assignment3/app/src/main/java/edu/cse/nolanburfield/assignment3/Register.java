package edu.cse.nolanburfield.assignment3;
import edu.cse.nolanburfield.assignment3.Connection;
import edu.cse.nolanburfield.assignment3.Packet;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;

import android.app.Activity;
import android.app.Application;
import android.os.Bundle;
import android.util.Base64;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.view.View;
import android.util.Log;
import android.widget.EditText;
import android.os.AsyncTask;
import android.content.Intent;
import android.widget.TextView;

public class Register extends Activity {

    private static final String TAG = "register";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        final AppState global = (AppState)getApplication();

        String ip = global.getIp();
        Integer peer_port = global.getPeer_port();
        Integer server_port = global.getServer_port();
        final EditText ip_input = (EditText) findViewById(R.id.ip);
        final Button reg_button = (Button) findViewById(R.id.register_button);
        final EditText reg_id = (EditText) findViewById(R.id.register_id);
        final EditText reg_first = (EditText) findViewById(R.id.register_first);
        final EditText reg_last = (EditText) findViewById(R.id.register_last);
        final EditText p_port = (EditText) findViewById(R.id.peer_port);
        final EditText s_port = (EditText) findViewById(R.id.server_port);
        ip_input.setText(ip);
        p_port.setText(Integer.toString(peer_port));
        s_port.setText(Integer.toString(server_port));
        reg_button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Perform action on click
                KeyPairGenerator kpg;
                KeyPair kp;
                PublicKey publicKey = null;
                try {
                    kpg = KeyPairGenerator.getInstance("RSA");
                    kpg.initialize(1024);
                    kp = kpg.generateKeyPair();
                    publicKey = kp.getPublic();
                    global.UserPrivateKey = kp.getPrivate();
                } catch (NoSuchAlgorithmException e) {
                    e.printStackTrace();
                }

                String data = reg_id.getText().toString() + "%" + reg_first.getText().toString() + "%" + reg_last.getText().toString() + "%" + Base64.encodeToString(publicKey.getEncoded(), Base64.DEFAULT) + "%";
                reg_id.setText("");
                reg_first.setText("");
                reg_last.setText("");
                global.setIp(ip_input.getText().toString());
                global.setPeer_port(Integer.parseInt(p_port.getText().toString()));
                global.setServer_port(Integer.parseInt(s_port.getText().toString()));
                message = new Packet("REGISTER", data, "");
                SendMessage sendMessageTask = new SendMessage();
                sendMessageTask.execute();
                changeLogin(v);
            }
        });

    }

    public void changeLogin(View view) {
        Intent intent = new Intent(this, Login.class);
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

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_register, menu);
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
