package edu.cse.nolanburfield.assignment3;

/**
 * Created by nolanburfield on 4/12/15.
 */

import android.util.Log;

public class Packet {

    private String header;
    private String data;
    private String body;

    private static final String TAG = "packet";

    public Packet(String header, String data, String body) {
        this.header = header;
        this.data = data;
        this.body = body;
        Log.v(TAG, "Packet Created: " + this.header + " " + this.data + " " + this.body);
    }

    public String send() {
        Log.v(TAG, "Packet " + this.header + " Returned.");
        return this.header + "\r\n\r" + this.data + "\r\n\r" + this.body;
    }

    public void result(String value) {
        String[] data;
        data = new String[3];
        data = value.split("\r\n\r");
        this.header = data[0];
        this.data = data[1];
        this.body = data[2];
    }

    public String getHeader() {
        return this.header;
    }

    public String getData() {
        return this.data;
    }

    public String getBody() {
        return this.body;
    }
}
