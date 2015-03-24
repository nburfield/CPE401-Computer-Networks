from packet import Packet
from connect import Connect
from log import Log

class register:
  '''User for the client to register the client with the server.'''

  def __init__(self, connection):
    self.connection = connection

  def execute(self):
    user = raw_input("Enter a user name: ")
    first = raw_input("Enter first name: ")
    last = raw_input("Enter last name: ")
    self.connection.TCPConnect()
    self.connection.send(Packet().build("REGISTER " + user + " " + first + " " + last, ""))
    Log().activity("Sent the packet: REGISTER " + user + " " + first + " " + last)

    for i in range(2):
      data = ''

      try:
        self.connection.timeout(10.0)
        data = self.connection.recieve()
        break

      except:
        self.connection.send(Packet().build("REGISTER " + user + " " + first + " " + last, ""))
        print "Timeout Hit, Attempt Resend number ", i+1

    if not data:
      try:
        self.connection.timeout(10.0)
        data = self.connection.recieve()
      except:
        pass

    self.connection.close()
    if not data:
      Log().error("Three attempts to register failed, server is down.")
      print "Three attempts to register failed, server is down."
      return None, None
    else:
      return data, "ACK"
