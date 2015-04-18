CPE 401
Assignment 2

Nolan Burfield

========================

 SETUP
=======

First setup the database for the server to run on MySQL

Run these commands in MySQL:
# mysql -u root -p
# CREATE USER 'social_peer'@'localhost' IDENTIFIED BY 'password';
# CREATE DATABASE social_peer_db;
# GRANT ALL ON social_peer_db.* TO 'social_peer'@'localhost';
# exit

Then from the server directory run: 
    python database.py

* This will need peewee installed

** In database.py there is the data used to access the database **

Running the App on emulator.

To Run the app running on a emulator will require port forwarding from the selected Peer Port to the emulator


 USAGE 
=======

To exit from the server side hit control-c.



The app will run all the server commands, and will run a HI message, and Chat messages.

The application should be intuitive with the commands. 

To do a Chat there will be a list of friends, and then type in the friend name initially to chat to. This will then change for a message to be sent. Type that in, and then the message will be sent b UDP to the receiving friend. 
