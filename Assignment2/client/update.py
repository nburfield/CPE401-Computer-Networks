from packet import Packet
from connect import Connect
from log import Log

class update:
  '''This is to update a user profile'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    path = raw_input("Enter the path to the XML file: ")
    f = open(path, "r")
    body = f.read()
    length = len(body)
    f.close

    self.connection.TCPConnect()
    self.connection.send(Packet().build("UPDATE " + str(length), body))
    Log().activity("Sent the packet: UPDATE " + str(length))
    data = self.connection.recieve()
    self.connection.close()
    return data, "SUCCESS"
