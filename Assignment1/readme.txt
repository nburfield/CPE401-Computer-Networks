CPE 401 Assignment 1
====================

Nolan Burfield
26 February 2015


Setup
=====

This program uses peewee for database manipulation on a MySQL database. 
Install peewee
	pip install peewee
Install either MySQLdb or PyMySQL
	pip install PyMySQL

Open the MySQL database and create a user and database with that user on it.
The configuration in database.py is for the below setup, the file can be
adjusted on line 4 with the proper user and database information.

	mysql -u root -p
	CREATE USER 'social'@'localhost' IDENTIFIED BY 'password';
	CREATE DATABASE social_db;
	GRANT ALL ON social_db.* TO 'social'@'localhost';
	exit

Then run the python database file to create the tables in the database.
	python database.py


Usage
=====

To start the system startup the python server with the port number on the command line.
To start the client start up with the User-ID, IP, and port.

The server will log activity in the server.activity.log, and errors in the server.error.log
There will also be ouptut to the monitor as it runs.

To interact with the system all commands are to be given to the client.
The client will give output, as well as log things in client.activity.log and client.error.log

The commands to give to the client are the creation of the application packet as specified in the project requierments.

From the client side there is the ouput from recieved packets that is sent to screen and activity file that connect to the server response that was required.

When logging into a user there will be a display of any new messages, chats, or unconfirmend friend requests.

Commands
========

To register a user. All user-ID are integer values!!!!!!!!!
    REGISTER <user-id> <first-name> <last-name>

To Update the profile.
    UPDATE <size-of-file, will be corrected by client server> <full-path-to-xml>

    The profile must have the following pieces in the XML file for proper database update
    <first><first-name></first>
    <last><last-name></last>
    <time><time-updated></time>

To login, or to refresh your page with any new messages, chats, or friend requests.
    LOGIN <user-id>

To logout.
    QUIT <user-id>

To create a friend connection, and accept/deny the friend request from another.
    FRIEND <friend-user-id>
    CONFIRM <friend-user-id>
    REJECT <friend-user-id>

To begin a chat message with someone.
    CHAT <user-id>

    This will then take you to a message entry platform that will read in text, and endline.
    To do a message enter it into the prompt, hit enter, then control-c to escape the message entry.
    Then there will be the selection to re-enter the message, or send it.

To do a message post to the wall.
    POST <message-type: 'friend' or 'circle' or 'public'>

    This will then take you to a message entry platform that will read in text, and endline.
    To do a message enter it into the prompt, hit enter, then control-c to escape the message entry.
    Then there will be the selection to re-enter the message, send the message, or add in some media link like a picture, video, or audio.

To get the wall messages in a certain ammount of hours.
  ENTRIES <number-of-hours-to-look-back>

  This will then get the entries, compile into an XML file, and return the file saving to the user directory, and outputting.

To serach for an item in a users profile.
  SEARCH <keyword>

  This will then get the entries, compile into an XML file, and return the file saving to the user directory, and outputting.


Problems
========

The server uses pool threading, and is successful in creating threads and running the thread queue.
The problem is however that the locks for users does not work, and so users get logged out if another user
logs in. 

