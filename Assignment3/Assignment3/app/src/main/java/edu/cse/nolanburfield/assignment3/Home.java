package edu.cse.nolanburfield.assignment3;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;


public class Home extends Activity {

    private static final String TAG = "home";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        final TextView reg_id = (TextView) findViewById(R.id.user_id);
        AppState global = (AppState)getApplication();
        if (!global.isLoggedIn()) {
            Intent intent = new Intent(this, Login.class);
            startActivity(intent);
        }
        reg_id.setText(global.getUser());

        DatabaseHandler db = new DatabaseHandler(this);
        db.addFriend("tyler", 0, "127.0.0.1");
    }

    public void onLoggout(View v) {
        AppState global = (AppState)getApplication();
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

    public void performFriend(View v) {
        Intent intent = new Intent(this, Friend.class);
        startActivity(intent);
    }

    public void performHi(View v) {

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
                client = new Socket("10.0.2.2", 3000);
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
