import peewee
from peewee import *

# mysql -u root -p
# CREATE USER 'social_peer'@'localhost' IDENTIFIED BY 'password';
# CREATE DATABASE social_peer_db;
# GRANT ALL ON social_peer_db.* TO 'social_peer'@'localhost';
# exit
# Database name, user to access that database, and password for that user
db = MySQLDatabase('social_peer_db', user='social_peer', passwd='password')

class Friend(peewee.Model):
  friend_id = peewee.CharField(unique = True)
  accepted = peewee.BooleanField(null = True)
  ip = peewee.CharField()

  class Meta:
    database = db

class Chat(peewee.Model):
  message = peewee.TextField()
  counter = peewee.IntegerField()
  friend_id = peewee.CharField(unique = True)

  class Meta:
    database = db

if __name__ == '__main__':
  Friend.create_table()
  #Chat.create_table()
