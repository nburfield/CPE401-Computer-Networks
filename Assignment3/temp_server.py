import socket
import sys
from Crypto.PublicKey import RSA
from base64 import b64decode

def runServer(s):
  while True:
    # Get all the data from the sender
    conn, addr = s.accept()
    value = conn.recv(1024)
    print value
    conn.close()

    private_key_file = open("PrivateKey", 'r')
    rsa_key = RSA.importKey(private_key_file.read())
    private_key_file.close()
    raw_cipher_data = b64decode(value)
    decrypt = rsa_key.decrypt(raw_cipher_data)

    print "\n\n\n", decrypt


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
