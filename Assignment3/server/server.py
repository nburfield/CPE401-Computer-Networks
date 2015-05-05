import socket
import sys
import importlib
from log import Log
from packet import Packet
from Crypto.PublicKey import RSA
from base64 import b64decode
from database import *

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
    ip = conn.getpeername()[0]
    try:
      user = User.get(User.ip == ip)
      private_key_file = open("PrivateKey", 'r')
      rsa_key = RSA.importKey(private_key_file.read())
      private_key_file.close()
      raw_cipher_data = b64decode(value)
      decrypt = rsa_key.decrypt(raw_cipher_data)
    except:
      decrypt = value

    print "\n", decrypt

    runPacket(decrypt, conn)

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




