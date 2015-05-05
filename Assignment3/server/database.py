import peewee
from peewee import *

# mysql -u root -p
# CREATE USER 'social_peer'@'localhost' IDENTIFIED BY 'password';
# CREATE DATABASE social_peer_db;
# GRANT ALL ON social_peer_db.* TO 'social_peer'@'localhost';
# exit
# Database name, user to access that database, and password for that user
db = MySQLDatabase('social_peer_db', user='social_peer', passwd='password')

class User(peewee.Model):
  user_id = peewee.CharField(unique = True)
  first = peewee.CharField()
  last = peewee.CharField()
  profile = peewee.TextField()
  ip = peewee.CharField(default="")
  online = peewee.BooleanField(default=False)
  public_key = peewee.CharField()

  class Meta:
    database = db

if __name__ == '__main__':
  User.create_table()
