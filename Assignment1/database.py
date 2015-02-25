import peewee
from peewee import *

# Database name, user to access that database, and password for user.
db = MySQLDatabase('social_db', user='social', passwd='password')

class User(peewee.Model):
  ident = peewee.IntegerField(unique = True)
  first = peewee.TextField()
  last = peewee.TextField()
  profile = peewee.TextField(null = True)
  online = peewee.BooleanField(default = False)
  port = peewee.IntegerField(null = True)
  ip = peewee.TextField(null = True)


  class Meta:
    database = db

class Friend_Request(peewee.Model):
  userone_id = peewee.IntegerField()
  usertwo_id = peewee.IntegerField()
  accepted = peewee.BooleanField(null = True)

  class Meta:
    database = db

class Message(peewee.Model):
  userfrom_id = peewee.IntegerField()
  userto_id = peewee.IntegerField()
  message = peewee.TextField()
  group = peewee.IntegerField()
  time = peewee.IntegerField()
  attachment = peewee.IntegerField()
  link = peewee.TextField(null = True)

  class Meta:
    database = db

class Chat_Message(peewee.Model):
  userfrom_id = peewee.IntegerField()
  userto_id = peewee.IntegerField()
  message = peewee.TextField()
  counter = peewee.IntegerField()
  read = peewee.BooleanField()

  class Meta:
    database = db

if __name__ == '__main__': 
  User.create_table()
  Message.create_table()
  Friend_Request.create_table()
  Chat_Message.create_table()
