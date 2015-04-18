from database import *
from log import Log
from packet import Packet
import datetime

class register:
  '''Used to register a user to the database'''

  def execute(self, data, body, conn):
    if len(data) < 4: 
      Log().error("Not enough argument for register: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "Not Enough Arguments for register"))
      return

    XML = "<profile><info><user_id>" + data[0] + "</user_id><first>" + data[1] + "</first><last>" + data[2] + "</last><ip>" + conn.getpeername()[0] + "</ip><updated>" + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + "</updated></info></profile>"

    try:
      User(user_id=data[0], first=data[1], last=data[2], profile=XML).save()
    except:
      Log().error("Improper user name: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "Improper User Name."))
      return

    Log().activity("Added User: " + str(data) + " to the system.")
    conn.send(Packet().build("ACK " + data[0] + " " + conn.getpeername()[0] + " " + str(conn.getpeername()[1]), "User Registered"))
