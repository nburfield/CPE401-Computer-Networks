from database import *
from log import Log
from packet import Packet
import datetime

class search:
  '''Used to search the database'''

  def execute(self, data, body, conn):
    if len(data) < 2: 
      Log().error("Not enough argument for Search: Data - " + str(data) + "  Body - " + body)
      conn.send(Packet().build("ERR", "Not Enough Arguments for search"))
      return

    XML = "<search>\n"
    for user in User.select():
      if data[0].lower() in user.profile.lower():
        XML += "<find>\n"
        XML += user.profile
        XML += "</find>\n"
    XML += "</search>\n"

    Log().activity("Return search XML: " + XML + " to the user.")
    conn.send(Packet().build("RESULTS " + str(len(XML)), XML))
