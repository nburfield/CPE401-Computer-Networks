from packet import Packet
from connect import Connect
from log import Log
from database import *
import re
import webbrowser
import os
import threading
import time

def FileOpen(f):
  webbrowser.open("file://" + os.path.abspath(f.name))

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

      if i == "1" or i == "F" or i == "f":
        messageNumber = 1
        messageType = "friends"
      elif i == "2" or i == "O" or i == "o":
        messageNumber = 2
        messageType = "friends-of-friends"
      elif i == "3" or i == "P" or i == "p":
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

    recipients = self.connection.user + "; "
    for f in Friend.select():
      if f.ip:
        recipients += f.friend_id + "; "

    post = post.replace("\r\n\r", "")
    post = post.replace("\n\n", "")
    XML = "<wall>\n<type>" + messageType + "</type>\n<id>" + str(messageNumber) + "</id>\n<recipients>" + recipients + "</recipients>\n<message>\n" + post + "\n</message>\n</wall>\n"
    Wall(message=XML, time=int(time.time()), message_type=messageNumber).save()  

    for f in Friend.select().where((Friend.accepted == True)):
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

    messageType = re.compile('<type>([^)]*)</type>').findall(body)[0]
    messageNumber = int(re.compile('<id>([^)]*)</id>').findall(body)[0])
    message = re.compile('<message>([^)]*)</message>').findall(body)[0]
    recipients = re.compile('<recipients>([^)]*)</recipients>').findall(body)[0]
    people = re.compile('([^; ]*)\S').findall(recipients)

    XML = body
    if messageNumber == 2:
      first, end = XML.split("<id>")
      dummy, end = end.split("</id>")
      XML = first + "<id>1</id>" + end

    if messageNumber == 2 or messageNumber == 3:
      for f in Friend.select():
        if f.ip:
          if not f.friend_id in people:
            recipients += f.friend_id + "; "

      first, end = XML.split("<recipients>")
      dummy, end = end.split("</recipients>")
      XML = first + "<recipients>" + recipients + "</recipients>" + end

      for f in Friend.select():
        if f.ip:
          if not f.friend_id in people:
            self.connection.UDPConnection(f.ip)
            self.connection.send(Packet().build("POST " + meta[0] + " " + str(len(XML)), XML))

    try:
      f = open("wall.xml", "r")
      browser = f.read()
      browser = browser.split("\n")
      browser.pop()
      f.close()
    except:
      browser = ["<file>"]

    f = open("wall.xml", "w")
    for l in browser:
      f.write(l)
    f.write(XML)
    f.write("</file>")
    t = threading.Thread(name="file-open", target=FileOpen, args=(f,))
    t.start()
    f.close()

    print "Recieved a Wall Message from: ", meta[0]
    print "Message has type: ", messageType
    print "Message"
    print "======="
    print message

    return None, None
