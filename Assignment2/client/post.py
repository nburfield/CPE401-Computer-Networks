from packet import Packet
from connect import Connect
from log import Log
from database import *

class post:
  '''User to post wall messages with friends that are online.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    messageType = ""
    messageNumber = ""
    while not messageType:
      print "Select Wall Post Type"
      print "====================="
      print "1. <F>riends"
      print "2. Friends-<o>f-Friends"
      print "3. <P>ublic"
      i = raw_input("Enter the selection: ")

      if "1" or "F" or "f":
        messageNumber = 1
        messageType = "friends"
      elif "2" or "O" or "o":
        messageNumber = 2
        messageType = "friends-of-friends"
      elif "3" or "P" or "p":
        messageNumber = 3
        messageType = "public"
      else:
        messageNumber = ""

    m = True
    post = ""
    while m:
      print "Enter the wall message here: MAX 1024 length or hit enter twice to end"
      print "======================================================================"
      while len(post) < 1024:
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
    XML = "<wall>\n<type>" + messageType + "</type>\n<id>" + str(messageNumber) + "</id>\n<message>\n" + post + "\n</message>\n</wall>\n"
    Wall(message=XML).save()  

    for f in Friend.select():
      if f.ip:
        self.connection.UDPConnection(f.ip)
        self.connection.send(Packet().build("POST " + self.connection.user + " " + str(len(XML)), XML))

    Log().activity("Sent the xml wall with type: " + messageType + " - message: " + XML)
    return None, None

  def run(self, ip, data):
    header, meta, body = Packet().divide(data)

    self.connection.UDPConnection(ip)
    while len(body) < int(meta[1]):
      body += self.connection.recieve()

    print "Recieved a Wall Message from: ", meta[0]
    print "Message"
    print "======="
    print body

    return None, None
