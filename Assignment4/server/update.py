from database import *
from log import Log
from packet import Packet
import re

class update:
  '''Used on the server to update a profile'''

  def execute(self, data, body, conn):
    if len(data) < 2: 
      Log().error("Not enough argument for update: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "Not Enough Arguments for update"))
      return

    while len(body) < int(data[0]):
      body += conn.recv(1024)

    try:
      user = User.get(User.ip == conn.getpeername()[0])
    except:
      Log().error("User not logged in.")
      conn.send(Packet().build("ERR", "User not logged in."))
      return

    first, dummy = body.split("<ip>")
    dummy, second = body.split("</ip>")
    body = first + "<ip>" + conn.getpeername()[0] + "</ip>" + second

    user.profile = body
    f = re.compile('<first>([^)]*)</first>').search(body)
    l = re.compile('<last>([^)]*)</last>').search(body)
    if f: user.first = f.groups()[0]
    if l: user.last = l.groups()[0]
    user.save()

    t = re.compile('<updated>([^)]*)</updated>').search(body)
    if t:
      time = t.groups()[0]
    else:
      time = "Undefined"
    
    Log().activity("Updated the user profile with - Time: " + time + " Body - " + body)
    conn.send(Packet().build("SUCCESS " + time, "Update to the profile."))
