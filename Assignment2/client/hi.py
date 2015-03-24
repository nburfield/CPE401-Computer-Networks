from packet import Packet
from connect import Connect
from log import Log
from database import *

class hi:
  '''User to tell all friends they are online.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    for f in Friend.select():
      if f.ip:
        self.connection.UDPConnection(f.ip)
        self.connection.send(Packet().build("HI " + self.connection.user, ""))
        Log().activity("Sent the HI to user: " + f.friend_id)

    return None, None

  def run(self, ip, data):
    header, meta, body = Packet().divide(data)
    try:
      f = Friend.select().where((Friend.friend_id == meta[0]))[0]
      f.ip = ip
      f.save()
    except:
      Log().error("No open friend with name: " + meta[0] + " exists.")
      return None, None
    Log().activity("Ran A HI Message from IP: " + ip)
    print "Ran A HI Message from IP: " + ip
    return None, None
