package edu.cse.nolanburfield.assignment3;

import android.app.Activity;
import android.app.Application;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.util.Log;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class Login extends Activity {

    private static final String TAG = "login";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        DatabaseHandler db = new DatabaseHandler(this);

    }

    public void onLogin(View v) {
        final EditText login_id = (EditText) findViewById(R.id.login_id);
        String data = login_id.getText().toString() + "%";
        message = new Packet("LOGIN", data, "");
        SendMessage sendMessageTask = new SendMessage();
        sendMessageTask.execute();
        AppState global = (AppState)getApplication();
        global.setLoggedIn(login_id.getText().toString());
        Intent intent = new Intent(this, Home.class);
        startActivity(intent);
    }

    public void changeRegister(View view) {
        Intent intent = new Intent(this, Register.class);
        startActivity(intent);
    }

    private class SendMessage extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            try {
                client = new Socket("10.0.2.2", 3000);
                printwriter = new PrintWriter(client.getOutputStream(), true);
                String value = message.send();
                Log.v(TAG, value);
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
