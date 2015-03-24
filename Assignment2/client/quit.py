from packet import Packet
from connect import Connect
from log import Log

class quit:
  '''This is used byt the user to end a session'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    self.connection.TCPConnect()
    self.connection.send(Packet().build("QUIT " + self.connection.user, ""))
    Log().activity("Sent the packet: QUIT " + self.connection.user)
    try:
      self.connection.timeout(10.0)
      data = self.connection.recieve()
      self.connection.close()
      return data, " "
    except:
      self.connection.close()
      return None, None
