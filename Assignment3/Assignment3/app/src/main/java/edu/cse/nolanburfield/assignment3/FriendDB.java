package edu.cse.nolanburfield.assignment3;

/**
 * Created by nolanburfield on 4/13/15.
 */
public class FriendDB {

    Integer id;
    String friend_id;
    Integer accepted;
    String ip;
    String public_key;

    FriendDB() {
    }

    FriendDB(Integer id, String friend_id, Integer accepted, String ip, String public_key) {
        this.id = id;
        this.friend_id = friend_id;
        this.accepted = accepted;
        this.ip = ip;
        this.public_key = public_key;
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

    void setPublic_key(String public_key) { this.public_key = public_key;}

    String getPublic_key() { return public_key;}

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
