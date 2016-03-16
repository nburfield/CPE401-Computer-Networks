package edu.cse.nolanburfield.assignment3;

import android.app.Activity;
import android.app.Application;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Base64;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.util.Log;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.interfaces.RSAPrivateKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.ArrayList;
import java.util.List;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;

public class Login extends Activity {

    private static final String TAG = "login";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;
    private DatabaseHandler db = new DatabaseHandler(this);
    private AppState global;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        global = (AppState)getApplication();
        String ip = global.getIp();
        Integer peer_port = global.getPeer_port();
        Integer server_port = global.getServer_port();
        final EditText ip_input = (EditText) findViewById(R.id.ip_input);
        final EditText p_port = (EditText) findViewById(R.id.peer_port);
        final EditText s_port = (EditText) findViewById(R.id.server_port);
        ip_input.setText(ip);
        p_port.setText(Integer.toString(peer_port));
        s_port.setText(Integer.toString(server_port));
    }

    public void onLogin(View v) {
        final EditText login_id = (EditText) findViewById(R.id.login_id);
        final EditText ip_input = (EditText) findViewById(R.id.ip_input);
        final EditText p_port = (EditText) findViewById(R.id.peer_port);
        final EditText s_port = (EditText) findViewById(R.id.server_port);
        global.setIp(ip_input.getText().toString());
        global.setPeer_port(Integer.parseInt(p_port.getText().toString()));
        global.setServer_port(Integer.parseInt(s_port.getText().toString()));

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

        String data = login_id.getText().toString() + "%" + Base64.encodeToString(publicKey.getEncoded(), Base64.DEFAULT) + "%";
        message = new Packet("LOGIN", data, "");
        SendMessage sendMessageTask = new SendMessage();
        global.setLoggedIn(login_id.getText().toString());
        sendMessageTask.execute();
        if (global.isLoggedIn()) {
            Intent intent = new Intent(this, Home.class);
            startActivity(intent);
        }
    }

    public void changeRegister(View view) {
        Intent intent = new Intent(this, Register.class);
        startActivity(intent);
    }

    private class SendMessage extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            try {
                String ip = global.getIp();
                Integer port = global.getServer_port();
                try {
                    client = new Socket(ip, port);
                } catch (IOException e) {
                    Log.e(TAG, "Server Not Responding.");
                    global.setLoggedOut();
                    return null;
                }

                String encrypted = message.send();
                printwriter = new PrintWriter(client.getOutputStream(), true);
                Log.v(TAG, encrypted);
                printwriter.write(encrypted);
                printwriter.flush();
                printwriter.close();
                client.close();

                List<FriendDB> all = new ArrayList<FriendDB>();
                all = db.getAllFriends();
                for (int i = 0; i < all.size(); i++) {
                    Log.v(TAG, all.get(i).getName());
                    Log.v(TAG, all.get(i).getIp());
                    Packet ip_search = new Packet("SEARCH", all.get(i).getName() + "%", "");
                    encrypted = global.encryptServerPublic(ip_search.send());
                    Log.v(TAG, encrypted);
                    client = new Socket(ip, port);
                    printwriter = new PrintWriter(client.getOutputStream(), true);
                    printwriter.write(encrypted);
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

                    Packet result = new Packet("", "", "");
                    result.result(data, ip);
                    String [] xml_data;
                    xml_data = new String [2];
                    xml_data = result.getBody().split("<ip>");
                    xml_data = xml_data[1].split("</ip>");
                    String discovered_ip = xml_data[0];
                    all.get(i).setIp(discovered_ip);
                    db.updateFriend(all.get(i));
                    printwriter.close();
                    client.close();
                }
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
        getMenuInflater().inflate(R.menu.menu_login, menu);
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
