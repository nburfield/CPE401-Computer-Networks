from packet import Packet
from connect import Connect
from log import Log
import webbrowser
import os

class search:
  '''Used by the user to search the database.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    search = raw_input("Enter a search keyword: ")

    self.connection.TCPConnect()
    self.connection.send(Packet().build("SEARCH " + search, ""))
    Log().activity("Sent the packet: SEARCH " + search)

    data = self.connection.recieve()
    header, meta, body = Packet().divide(data)
    while len(body) < int(meta[0]):
      data += self.connection.recieve()

    header, meta, body = Packet().divide(data)
    f = open("search.xml", "w")
    f.write(body)
    webbrowser.open("file://" + os.path.abspath(f.name))
    f.close()

    self.connection.close()
    return data, "RESULTS"
