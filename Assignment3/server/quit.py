from database import *
from log import Log
from packet import Packet

class quit:
  '''Used on the server to log the user out'''

  def execute(self, data, body, conn):
    if len(data) < 2: 
      Log().error("Not enough argument for quit: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "Not Enough Arguments for quit"))
      return

    try:
      user = User.get(User.user_id == data[0])
    except:
      Log().error("User does not exist: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "User does not exist"))
      return

    if user.ip != conn.getpeername()[0]:
      Log().error("User does not exist on that ip: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "User does not exist on that IP"))
      return

    XML = user.profile
    first, dummy = XML.split("<ip>")
    dummy, second = XML.split("</ip>")
    user.profile = first + "<ip></ip>" + second
    Log().activity("User " + user.user_id + " logged out.")
    user.ip = ""
    user.online = False
    user.save()
