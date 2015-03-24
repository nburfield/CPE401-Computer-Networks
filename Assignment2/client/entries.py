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

class entries:
  '''User to get wall messages from friends that are online.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    search_time = raw_input("Enter the hours back to look for wall posts: ")

    queries_sent = 0
    XML = "<wallsearch>\n"
    for f in Friend.select().where((Friend.accepted == True)):
      if f.ip:
        queries_sent += 1
        self.connection.UDPConnection(f.ip)
        self.connection.send(Packet().build("ENTRIES " + self.connection.user + " " + search_time, ""))
        pack = ""
        self.connection.timeout(30.0)
        pack = self.connection.recieve(5006)
        if pack:
          dummy, meta_2, body_2 = Packet().divide(pack)
          while len(body_2) < meta_2[0]:
            body_2 += self.connection.recieve(5006)
          XML += body_2
    XML += "\n</wallsearch>"

    Log().activity("Sent the wall requests with time: " + search_time + " to " + str(queries_sent) + " friends.")

    f = open("wallsearch.xml", "w")
    f.write(XML)
    f.write("</file>")
    t = threading.Thread(name="file-open", target=FileOpen, args=(f,))
    t.start()
    f.close()

    return None, None

  def run(self, ip, data):
    header, meta, body = Packet().divide(data)

    print "Recieved a wall query... "

    if Friend.select().where((Friend.accepted == True) & (Friend.friend_id == meta[0])) > 0:
      friend = True
    else: 
      friend = False

    XML = ""
    if friend:
      for f in Friend.select().where((Friend.accepted == True) & (Friend.friend_id != meta[0]) & (Friend.ip != ip)):
        if f.ip:
          self.connection.UDPConnection(f.ip)
          self.connection.send(Packet().build("ENTRIES " + meta[0] + " " + meta[1], ""))
          self.connection.timeout(5.0)
          pack = self.connection.recieve(5006)
          dummy, meta_2, body_2 = Packet().divide(pack)
          while len(body_2) < int(meta_2[0]):
            body_2 += self.connection.recieve(5006)
          XML += body_2

      for m in Wall.select().where((Wall.time > int(time.time())-int(meta[1]))):
        XML += "<post>\n"
        XML += m.message
        XML += "\n</post>\n"

    else:
      for m in Wall.select().where((Wall.time > int(time.time())-int(meta[1])) & (Wall.message_type != 1)):
        XML += "<post>\n"
        XML += m.message
        XML += "\n</post>\n"

    print "... Sending results of " + XML + " " + type(XML)
    self.connection.UDPConnection(ip)
    self.connection.send(Packet().build("WALL " + str(len(XML)), XML), 5006)

    return None, None
