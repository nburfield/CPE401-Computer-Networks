from packet import Packet
from connect import Connect
from log import Log
from database import *

class chat:
  '''User to chat with friends that are online.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    for f in Friend.select().where((Friend.accepted == True)):
      print f.friend_id

    user = raw_input("Enter the user to send a message to: ")

    try:
      f = Friend.select().where((Friend.friend_id == user) & (Friend.accepted == True))[0]
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

      print post
      print "\nSelect what to do with the chat message above:"
      print "1. <S>end As Is"
      print "2. Re-Do <P>ost"
      inp = raw_input()

      if inp == "1" or inp == "S" or inp == "s":
        m = False
      else:
        post = ""
        m = True

    post = post.replace("\r\n\r", "")
    post = post.replace("\n\n", "")
    c.counter = c.counter + 1
    c.message = c.message + post + "\r\n\r"
    c.save()
    self.connection.UDPConnection(f.ip)
    self.connection.send(Packet().build("CHAT " + user + " " + str(c.counter) , post))

    index = 0
    while index < 3:
      try:
        self.connection.timeout(10.0)
        data = self.connection.recieve(5006)
        if data:
          header, meta, body = Packet().divide(data)
          if header.lower() == "delivered":
            Log().activity("Got the delivered message: header - " + header + " meta-data - " + str(meta) + " body - " + body)
            index = 3
          else:
            Log().error("Recieved bad packet: header - " + header + " meta-data - " + str(meta) + " body - " + body)
        else:
          throw
      except:
        self.connection.UDPConnection(f.ip)
        self.connection.send(Packet().build("CHAT " + user + " " + str(c.counter) , post))
      index += 1

    Log().activity("Sent the chat to user: " + user + " - message: " + post)

    return None, None

  def run(self, ip, data):
    header, meta, body = Packet().divide(data)

    try:
      f = Friend.select().where((Friend.ip == ip))[0]
    except: 
      Log().error("There is no user with that ip: " + ip)
      return None, None

    print "Recieved a message from: ", f.friend_id
    print "Message"
    print "======="
    print body

    try:
      c = Chat.select().where((Chat.friend_id == f.friend_id))[0]
    except:
      c = Chat(message="", counter=meta[1], friend_id=f.friend_id)

    c.counter = meta[1]
    c.message = c.message + body + "\r\n\r"
    c.save()

    self.connection.UDPConnection(ip)
    self.connection.send(Packet().build("DELIVERED " + self.connection.user + " " + meta[1], ""), 5006)
    return None, None
