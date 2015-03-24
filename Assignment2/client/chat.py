from packet import Packet
from connect import Connect
from log import Log
from database import *

class chat:
  '''User to chat with friends that are online.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    for f in Friend.select():
      print f.friend_id

    user = raw_input("Enter the user to send a message to: ")

    try:
      f = Friend.select().where((Friend.friend_id == user))[0]
    except: 
      Log().error("There is no user with that name: " + user)
      return None, None

    if not f.ip:
      Log().error("The user is not logged in: " + user)
      return None, None

    try:
      c = Chat.select().where((Chat.friend_id == user))[0]
    except:
      c = Chat(message="", counter=0, friend_id=user)

    m = True
    post = ""
    while m:
      print "Enter the chat message here: MAX 1024 length or hit enter twice to end"
      print "======================================================================"
      while len(post) < 983:
        post += raw_input()
        post += "\n"
        if "\n\n" in post:
          break

      print "\n\n", post
      print "\nSelect what to do with the chat message above:"
      print "1. <S>end As Is"
      print "2. Re-Do <P>ost"
      inp = raw_input()

      if inp == "1" or inp == "S" or inp == "s":
        m = False
      else:
        m = True

    post = post.replace("\r\n\r", "")
    c.counter = c.counter + 1
    c.message = c.message + post + "\r\n\r"
    c.save()
    self.connection.UDPConnection(f.ip)
    self.connection.send(Packet().build("CHAT " + user + " " + str(c.counter) , post))
    print self.connection.recieve()
    Log().activity("Sent the chat to user: " + user + " - message: " + post)

    return None, None

  def run(self, ip, data):
    header, meta, body = Packet().divide(data)
    print header
    print meta
    print body
    self.connection.UDPConnection(ip)
    self.connection.send(Packet().build("DELIVERED " + connection.user + " " + meta[1], ""))
    return None, None
