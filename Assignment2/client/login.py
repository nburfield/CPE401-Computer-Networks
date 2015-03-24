from packet import Packet
from connect import Connect
from log import Log
from database import *
import re

class login:
  '''This is used to login to the server'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    self.connection.TCPConnect()
    self.connection.send(Packet().build("LOGIN " + self.connection.user, ""))
    Log().activity("Sent the packet: LOGIN " + self.connection.user)

    try:
      self.connection.timeout(10.0)
      error = self.connection.recieve()
      self.connection.close()
    except:
      self.connection.close()

    self.connection.TCPConnect()
    self.connection.send(Packet().build("SEARCH " + " " , ""))
    Log().activity("Sent the packet: SEARCH " + " ")

    data = self.connection.recieve()
    header, meta, body = Packet().divide(data)
    while len(body) < int(meta[0]):
      data += self.connection.recieve()
    self.connection.close()
 
    header, meta, body = Packet().divide(data)
    f = body.split("</find>")
    print "FIND\n", f
    for u in f:
      value = re.compile('.*<user_id>([^)]*)</user_id><.*').findall(u)
      print "VALUE\n", value
      try:
        f = Friend.select().where((Friend.friend_id == value[0]))[0]
        value = re.compile('<ip>([^)]*)</ip>').search(u)
        print value.groups()[0]
        f.ip = value.groups()[0]
        f.save()
      except:
        pass

    if error:
      return error, " "
    else:
      return None, None    
