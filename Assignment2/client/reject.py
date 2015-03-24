from packet import Packet
from connect import Connect
from log import Log
from database import *

class reject:
  '''User to deny a friend request.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    for f in Friend.select().where(Friend.accepted >> None):
      print "Unconfirmed Request: ", f.friend_id
    user_request = raw_input("Enter the user to deny a friend request: ")

    try:
      f = Friend.select().where((Friend.friend_id == user_request) and (Friend.accepted >> None))[0]
      f.accepted = False
      f.save()
    except:
      Log().error("No open friend request with name: " + user_request + " exists.")
      return None, None

    self.connection.UDPConnection(f.ip)
    self.connection.send(Packet().build("REJECT " + user_request, ""))
    Log().activity("Sent the friend request rejection to user: " + user_request + " at IP: " + f.ip)
    return None, None

  def run(self, ip, data):
    try:
      f = Friend.select().where((Friend.ip == ip) and (Friend.accepted >> None))[0]
      f.accepted = False
      f.save()
    except:
      Log().error("No open friend request with name: " + user_request + " exists.")
      return None, None
    print "Ran A Rejection from IP: " + ip
    return None, None
