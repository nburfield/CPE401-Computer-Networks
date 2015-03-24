from packet import Packet
from connect import Connect
from log import Log
from database import *
import re

class friend:
  '''User to create a friend request.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    user_request = raw_input("Enter the user to friend: ")

    self.connection.TCPConnect()
    self.connection.send(Packet().build("SEARCH " + user_request, ""))
    Log().activity("Sent the packet: SEARCH " + user_request)

    data = self.connection.recieve()
    header, meta, body = Packet().divide(data)
    while len(body) < int(meta[0]):
      data += self.connection.recieve()
    self.connection.close()
 
    header, meta, body = Packet().divide(data)
    f = re.compile('<find>([^)]*)</find>').search(body)
    ip_address = None
    for u in f.groups():
      value = re.compile('<user_id>([^)]*)</user_id>').search(u)
      if value.groups()[0] == user_request:
        value = re.compile('<ip>([^)]*)</ip>').search(u)
        ip_address = value.groups()[0]
        break

    if ip_address:
      try:
        Friend(friend_id=user_request, ip=ip_address).save()
      except:
        Log().error("Friend request with the user with name: " + user_request + " exists.")
        return None, None
      self.connection.UDPConnection(ip_address)
      self.connection.send(Packet().build("FRIEND " + user_request, ""))
      Log().activity("Sent the friend request to user: " + user_request + " at IP: " + ip_address)
    else:
      Log().error("No user with name, or they are not online: " + user_request + " exists.")

    return None, None

  def run(self, ip, data):
    self.connection.TCPConnect()
    self.connection.send(Packet().build("SEARCH " + ip, ""))
    Log().activity("Sent the packet: SEARCH " + ip)

    data = self.connection.recieve()
    header, meta, body = Packet().divide(data)
    while len(body) < int(meta[0]):
      data += self.connection.recieve()
    self.connection.close()
 
    header, meta, body = Packet().divide(data)
    f = re.compile('<find>([^)]*)</find>').search(body)
    ip_address = None
    for u in f.groups():
      value = re.compile('<ip>([^)]*)</ip>').search(u)
      if value.groups()[0] == ip:
        value = re.compile('<user_id>([^)]*)</user_id>').search(u)
        user_id = value.groups()[0]
        break

    try:
      Friend(friend_id=user_id, ip=ip).save()
    except:
      Log().error("Friend request with the user with name: " + user_id + " exists.")
      return None, None

    print "Recieved a friend request from: " + user_id
    Log().activity("Recieved a friend request from: " + user_id)
