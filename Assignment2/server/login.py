from database import *
from log import Log
from packet import Packet

class login:
  '''Used on the server to log the user in'''

  def execute(self, data, body, conn):
    if len(data) < 2: 
      Log().error("Not enough argument for login: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "Not Enough Arguments for login"))
      return

    try:
      user = User.get(User.user_id == data[0])
    except:
      Log().error("User does not exist: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "User does not exist"))
      return

    # Add the user data
    Log().activity("User " + user.user_id + " logged in.")
    user.online = True
    user.ip = conn.getpeername()[0]
    user.save()

    # Things that need to be done when logged in
    XML = user.profile
    first, dummy = XML.split("<ip>")
    dummy, second = XML.split("</ip>")
    user.profile = first + "<ip>" + conn.getpeername()[0] + "</ip>" + second
    user.save()
