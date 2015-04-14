package edu.cse.nolanburfield.assignment3;

/**
 * Created by nolanburfield on 4/13/15.
 */
public class FriendDB {

    Integer id;
    String friend_id;
    Integer accepted;
    String ip;

    FriendDB() {
    }

    FriendDB(Integer id, String friend_id, Integer accepted, String ip) {
        this.id = id;
        this.friend_id = friend_id;
        this.accepted = accepted;
        this.ip = ip;
    }

    void setID(Integer id) {
        this.id = id;
    }

    void setName(String name) {
        this.friend_id = name;
    }

    void setAccepted(Integer accepted) {
        this.accepted = accepted;
    }

    void setIp(String ip) {
        this.ip = ip;
    }

    Integer getID() {
        return id;
    }

    String getName() {
        return friend_id;
    }

    Integer getAccepted() {
        return accepted;
    }

    String getIp() {
        return ip;
    }
}
