import socket
import sys
import importlib
from log import Log
from packet import Packet
from connect import Connect
import threading

RUN = True
LOCKED_INPUT = False
LOCKED_UDP = False

# Functions
def runServer(connection):
  global RUN
  global LOCKED_INPUT
  while RUN:
    LOCKED_INPUT = False
    if not LOCKED_UDP:
      header = raw_input("Enter Packet Header: ")
      header = header.lower()
      if header == "end": 
        print "Cleaning up threads... "
        RUN = False
        print "Closing Program... "
        break
      try:
        somemodule = importlib.import_module(header)
        command = getattr(somemodule, header)
        while LOCKED_UDP: pass
        LOCKED_INPUT = True
        data, search = command(connection).execute()
        if data and search: response(data, search)
      except Exception as err:
        print type(err)
        print err.args
        print err
      except:
        Log().error("Recieved bad user input: " + header)
        print "Inproper Input."

def response(data, val):
  head, content, body = Packet().divide(data)
  if head == val: 
    Log().activity("Head: " + head + " Meta-data: " + str(content) + " Body: " + body)
  else:
    Log().error("Head: " + head + " Meta-data: " + str(content) + " Body: " + body)  
  print body

def PeerConnection(connection):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(('', 5005))
  global LOCKED_UDP
  while RUN:
    LOCKED_UDP = False
    if not LOCKED_INPUT:
      try:
        s.settimeout(10.0)
        data, addr = s.recvfrom(1024)
        header, meta, body = Packet().divide(data)
        header = header.lower()
        try:
          somemodule = importlib.import_module(header)
          command = getattr(somemodule, header)
          while LOCKED_INPUT: pass
          LOCKED_UDP = True
          data, search = command(connection).run(addr[0], data)
        except:
          Log().error("Bad Packet - Head: " + header + " Meta-data: " + str(meta) + " Body: " + body)
      except:
        pass

if __name__ == '__main__':
  # connection data
  USER = sys.argv[1]
  SERVER_IP = sys.argv[2]
  PORT = int(sys.argv[3])
  connection = Connect(SERVER_IP, PORT, USER)

  t = threading.Thread(name="peer-connection", target=PeerConnection, args=(connection,))
  r = threading.Thread(name="run-server", target=runServer, args=(connection,))
  r.start()
  t.start()
  t.join()
  somemodule = importlib.import_module("quit")
  command = getattr(somemodule, "quit")
  data, search = command(connection).execute()
  print "\nClient Exit"
