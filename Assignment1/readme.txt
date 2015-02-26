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


	
