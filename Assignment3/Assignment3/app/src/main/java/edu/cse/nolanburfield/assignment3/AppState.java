package edu.cse.nolanburfield.assignment3;

import android.app.Application;

/**
 * Created by nolanburfield on 4/13/15.
 */
public class AppState extends Application {
    private boolean loggedin = false;
    private String user_id = "";

    public boolean isLoggedIn() {
        return loggedin;
    }

    public void setLoggedOut() {
        loggedin = false;
        user_id = "";
    }

    public void setLoggedIn(String id) {
        loggedin = true;
        user_id = id;
    }
    public String getUser() {
        if (loggedin) {
            return user_id;
        }
        return "No User";
    }
}