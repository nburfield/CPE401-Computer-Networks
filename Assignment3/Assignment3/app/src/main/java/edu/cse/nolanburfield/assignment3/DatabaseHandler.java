package edu.cse.nolanburfield.assignment3;

import java.sql.SQLClientInfoException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

/**
 * Created by nolanburfield on 4/13/15.
 */

public class DatabaseHandler extends SQLiteOpenHelper {

    // All Static variables
    // Database Version
    private static final int DATABASE_VERSION = 1;

    // Database Name
    private static final String DATABASE_NAME = "peer_peer";

    // Contacts table name
    private static final String TABLE_FRIENDS = "friends";
    private static final String TABLE_CHAT = "chat";
    private static final String TABLE_WALL = "wall";

    // Tables Columns names
    private static final String ID = "id";
    private static final String FRIEND_ID = "name";
    private static final String ACCEPTED = "accepted";
    private static final String IP = "ip";
    private static final String MESSAGE = "message";
    private static final String COUNTER = "counter";
    private static final String TIME = "time";
    private static final String MESSAGE_TYPE = "message_type";

    public DatabaseHandler(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    // Creating Tables
    @Override
    public void onCreate(SQLiteDatabase db) {
        String CREATE_FRIENDS_TABLE = "CREATE TABLE " + TABLE_FRIENDS + "("
                + ID + " INTEGER PRIMARY KEY," + FRIEND_ID + " TEXT UNIQUE,"
                + ACCEPTED + " INTEGER," + IP + " TEXT" + ")";
        db.execSQL(CREATE_FRIENDS_TABLE);

        String CREATE_CHAT_TABLE = "CREATE TABLE " + TABLE_CHAT + "("
                + ID + " INTEGER PRIMARY KEY," + FRIEND_ID + " TEXT UNIQUE,"
                + COUNTER + " INTEGER," + MESSAGE + " TEXT" + ")";
        db.execSQL(CREATE_CHAT_TABLE);

        String CREATE_WALL_TABLE = "CREATE TABLE " + TABLE_WALL + "("
                + ID + " INTEGER PRIMARY KEY," + MESSAGE + " TEXT,"
                + TIME + " INTEGER," + MESSAGE_TYPE + " INTEGER" + ")";
        db.execSQL(CREATE_WALL_TABLE);
    }

    // Upgrading database
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // Drop older table if existed
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_FRIENDS);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_CHAT);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_WALL);

        // Create tables again
        onCreate(db);
    }

    /**
     * All CRUD(Create, Read, Update, Delete) Operations
     */

    // Adding new friend
    void addFriend(String name, Integer accepted, String ip) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(FRIEND_ID, name);
        values.put(ACCEPTED, accepted);
        values.put(IP, ip);

        // Inserting Row
        db.insert(TABLE_FRIENDS, null, values);
        db.close(); // Closing database connection
    }

    // Adding new chat
    void addChat(String name, String message) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(FRIEND_ID, name);
        values.put(COUNTER, 0);
        values.put(MESSAGE, message);

        // Inserting Row
        db.insert(TABLE_CHAT, null, values);
        db.close(); // Closing database connection
    }

    // Adding new wall
    void addWall(String type, String message) {
        SQLiteDatabase db = this.getWritableDatabase();
        Date date = new Date();
        ContentValues values = new ContentValues();
        values.put(MESSAGE, message);
        values.put(MESSAGE_TYPE, type);
        values.put(TIME, date.getTime());

        // Inserting Row
        db.insert(TABLE_FRIENDS, null, values);
        db.close(); // Closing database connection
    }

    // Getting single friend
    FriendDB getFriend(String friend_id) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor;
        try {
            cursor = db.query(TABLE_FRIENDS, new String[]{ID,
                            FRIEND_ID, ACCEPTED, IP}, FRIEND_ID + "=?",
                    new String[]{friend_id}, null, null, null, null);

        } catch (SQLiteException e) {
            return null;
        }

        if (cursor != null && cursor.moveToNext())
            cursor.moveToFirst();
        else {
            return null;
        }
        FriendDB friend = new FriendDB(Integer.parseInt(cursor.getString(0)),
                cursor.getString(1), Integer.parseInt(cursor.getString(2)), cursor.getString(3));

        // return contact
        return friend;
    }

    // Updating friend
    public int updateFriend(FriendDB friend) {

        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(FRIEND_ID, friend.getName());
        values.put(ACCEPTED, friend.getAccepted());
        values.put(IP, friend.getIp());

        // updating row
        return db.update(TABLE_FRIENDS, values, ID + " = ?",
                new String[] { String.valueOf(friend.getID()) });
    }

    // Getting All Contacts
    public List<FriendDB> getAllFriends() {
        List<FriendDB> friendList = new ArrayList<FriendDB>();

        // Select All Query
        String selectQuery = "SELECT  * FROM " + TABLE_FRIENDS;

        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.rawQuery(selectQuery, null);

        // looping through all rows and adding to list
        if (cursor.moveToFirst()) {
            do {
                FriendDB contact = new FriendDB();
                contact.setID(Integer.parseInt(cursor.getString(0)));
                contact.setName(cursor.getString(1));
                contact.setAccepted(Integer.parseInt(cursor.getString(2)));
                contact.setIp(cursor.getString(3));
                friendList.add(contact);
            } while (cursor.moveToNext());
        }

        // return contact list
        return friendList;
    }

    /*
    // Deleting single contact
    public void deleteContact(Contact contact) {
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(TABLE_CONTACTS, KEY_ID + " = ?",
                new String[] { String.valueOf(contact.getID()) });
        db.close();
    }


    // Getting contacts Count
    public int getContactsCount() {
        String countQuery = "SELECT  * FROM " + TABLE_CONTACTS;
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(countQuery, null);
        cursor.close();

        // return count
        return cursor.getCount();
    }
    */
}
