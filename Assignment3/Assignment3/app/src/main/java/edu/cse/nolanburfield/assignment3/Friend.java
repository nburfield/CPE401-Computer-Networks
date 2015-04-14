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


public class Friend extends Activity {

    private static final String TAG = "search";
    private Socket client;
    private PrintWriter printwriter;
    private Packet message;
    private Packet result;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_friend);

        DatabaseHandler db = new DatabaseHandler(this);
        db.addFriend("tyler", 0, "127.0.0.1");
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
                client = new Socket("10.0.2.2", 3000);
                printwriter = new PrintWriter(client.getOutputStream(), true);
                String value = message.send();
                Log.v(TAG, value);
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
                result.result(data);
                
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
