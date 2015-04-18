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

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class Update extends Activity {

    private static final String TAG = "update";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_update);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_update, menu);
        return true;
    }

    public void onUpdate(View v) {
        AppState global = (AppState)getApplication();
        final EditText first_name = (EditText) findViewById(R.id.first_name);
        final EditText last_name = (EditText) findViewById(R.id.last_name);
        final EditText other_data = (EditText) findViewById(R.id.other_data);
        if (first_name.getText().toString() == "" || last_name.getText().toString() == "") {
            Intent intent = new Intent(this, Home.class);
            startActivity(intent);
        }
        SimpleDateFormat df = new SimpleDateFormat("dd MMM yyyy HH:mm:ss");
        Calendar c = Calendar.getInstance();
        String time = df.format(c.getTime());
        String body = "<profile><info><user_id>" + global.getUser() + "</user_id><first>" + first_name.getText().toString() + "</first><last>" + last_name.getText().toString() + "</last><ip></ip><updated>" + time + "</updated></info><data>" + other_data.getText().toString() + "</data></profile>\n";
        String data = Integer.toString(body.length()) + "%";
        message = new Packet("UPDATE", data, body);
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
