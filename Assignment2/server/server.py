import socket
import sys
import importlib
from log import Log
from packet import Packet

# Functions
def runPacket(packet, conn):
  # Run the packet information
  header, meta, body = Packet().divide(packet)
  header = header.lower()
  execute = False
  try:
    somemodule = importlib.import_module(header)
    command = getattr(somemodule, header)
    Log().activity("Got good Packet: " + header)
    execute = True
  except:
    Log().error("Recieved bad packet: " + header)
    print "Corrupt Packet"

  if execute:
    command().execute(meta, body, conn)

def runServer(s):
  while True:
    # Get all the data from the sender
    conn, addr = s.accept()
    value = conn.recv(1024)

    runPacket(value, conn)

    conn.close()

if __name__ == '__main__':
  # conneection data
  PORT = int(sys.argv[1])
  HOST = ''
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen(5)

  try:
    runServer(s)
  except KeyboardInterrupt:
    # Close the connection
    s.close()
    print "\nServer Exit"

  except Exception as err:
    print type(err)
    print err.args
    print err




