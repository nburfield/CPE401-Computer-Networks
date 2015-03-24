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

Second setup the database for the client to run on MySQL

Run these commands in MySQL:
# mysql -u root -p
# CREATE USER 'social_peer'@'localhost' IDENTIFIED BY 'password';
# CREATE DATABASE social_peer_db;
# GRANT ALL ON social_peer_db.* TO 'social_peer'@'localhost';
# exit

Then from the client directory run: 
    python database.py

* This will need peewee installed

** In database.py on both client/server there is the data used to access the database **

 USAGE 
=======

To exit from the client side type: 
  end

To exit from the server side hit control-c.

The commands that a client can take are (enter only the word and no spaces):
  * register
  * login
  * quit
  * update
  * search
  * friend
  * confirm
  * reject
  * hi
  * chat 
  * post
  * entries

Each will perform its task as described in the assignment, but the terminal will walk you through the entries after a 
command has been given.

User must type 'login' when they enter the system to log the IP, and 'hi' to let all other friends know their IP.

An error on Linux occures when displaying the XML file. It will not crash the system but outputs text to the screen, there was no errors on Mac though

While testing this there was no errors that were discovered, and all functionalities work.
** There of course may be overlooked use cases that break, but the system should stay running and throw an error only.
