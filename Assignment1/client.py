# Libraries
import socket
import sys
import time
import os

# Built classes
from packet import Packet
from register import Register
from log import Log
from update import Update

'''
  This is a simple client side of a social network. To start the program run python client.py <user-ID> <server-IP> <port-number>
'''

# Connection data
USER = int(sys.argv[1])
TCP_IP = sys.argv[2]
TCP_PORT = int(sys.argv[3])
BUFFER_SIZE = 1024

# Functions

def connect(ip, port):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s
  except:
    Log().client_error("There was an error connection to IP => " + ip + " Port => " + str(port))
    exit()

def response(data, val, val_2 = ""):
  head, content, body = Packet().divide(data)
  if head == val or head == val_2: 
    Log().client_activity("Head: " + head + " Meta-data: " + content + " Body: " + body)
  else:
    Log().client_error("Head: " + head + " Meta-data: " + content + " Body: " + body)  
  print body 

def response_file(data, val, s):
  head, content, body = Packet().divide(data)
  if head == val:
    if len(data) == BUFFER_SIZE:
      MSGLEN = int(content.split("&")[0])
      bytes_recd = len(body)
      while len(body) < MSGLEN:
        data_recv = s.recv(min(MSGLEN - bytes_recd, BUFFER_SIZE))
        if data_recv == b'':
          print "... File data failed."
          Log().server_error("Socket connection broken when updating profile.")
          break
        body = body + data_recv

    Log().client_activity("Head: " + head + " Meta-data: " + content + " Body: " + body)
  else:
    Log().client_error("Head: " + head + " Meta-data: " + content + " Body: " + body) 
  f = open(content.split("&")[1], "w")
  f.write(body)
  f.close() 
  print body 

# Loop until complete
on = True
while on:
  # Run the typical TCP server
  try:
    select = raw_input("Enter Packet Data: ")
    MESSAGE = Packet().generate(select, "")
    header, meta, body = Packet().divide(MESSAGE)

    # Here is the register command, this will send the message, and attempt 3 times if no response.
    if header == "REGISTER":
      s = connect(TCP_IP, TCP_PORT)
      s.send(MESSAGE)
      for i in range(2):
        data = ''

        try:
          s.settimeout(10.0)
          data = s.recv(BUFFER_SIZE)
          break

        except:
          s.send(MESSAGE)
          print "Timeout Hit, Attempt Resend number ", i+1

      if not data:
        Log().client_error("Three attempts to register failed, server is down.")
      else:
        response(data, "ACK")

      s.close()

    # Here is the update, this will send the file data at the specified location, and then get the SUCCESS packet
    elif header == "UPDATE":
      FILE_MESSAGE, error = Update().client(meta)

      if not FILE_MESSAGE:
        print error
        Log().client_error(error)
        break

      # Check that the file message is the correct length
      length = meta.split("&")[0]
      MESSAGE = MESSAGE.replace(length, str(len(FILE_MESSAGE)))
      s = connect(TCP_IP, TCP_PORT)
      s.send(MESSAGE)
      s.send(FILE_MESSAGE)

      try:
        s.settimeout(10.0)
        data = s.recv(BUFFER_SIZE)

      except:
        s.send(MESSAGE)
        Log().client_error("The server did not respond with successful update.")
        break   

      response(data, "SUCCESS")
      s.close()

    # This is for the POST message, the client still needs to write the message
    elif header == "CHAT":
      s = connect(TCP_IP, TCP_PORT)
      s.send(MESSAGE)
      m = True
      while m:
        print "Enter the chat message here: MAX 1024 length or hit control-c to end: "
        post = ""
        while len(post) < 1024:
          try:
            post += raw_input()
            post += "\n"
          except KeyboardInterrupt:
            break

        print "\n\n", post
        print "\nSelect what to do with the chat message above:"
        print "1. <S>end As Is"
        print "2. Re-Do <P>ost"
        inp = raw_input()

        if inp == "1" or inp == "S" or inp == "s":
          s.send(Packet().generate("CHAT post", post))
          m = False

        else:
          m = True

      try:
        s.settimeout(10.0)
        data = s.recv(BUFFER_SIZE)
        response(data, "OFFLINE", "DELIVERED")

      except:
        pass

      s.close()

    # This is for the POST message, the client still needs to write the message
    elif header == "POST":
      s = connect(TCP_IP, TCP_PORT)
      s.send(MESSAGE)
      m = True
      while m:
        print "Enter the post here: MAX 1024 length or hit control-c to end: "
        post = ""
        while len(post) < 1024:
          try:
            post += raw_input()
            post += "\n"
          except KeyboardInterrupt:
            break

        print "\n\n", post
        print "\nSelect what to do with the post above:"
        print "1. Add <I>mage Link"
        print "2. Add <A>udio Link"
        print "3. Add <V>ideo Link"
        print "4. Re-Do <P>ost"
        print "5. <S>end As Is"
        inp = raw_input()

        if inp == "1" or inp == "I" or inp == "i":
          link = raw_input("Enter Image Link: ")
          s.send(Packet().generate("POST image " + link, post))
          m = False

        elif inp == "2" or inp == "A" or inp == "a":
          link = raw_input("Enter Audio Link: ")
          s.send(Packet().generate("POST audio " + link, post))
          m = False

        elif inp == "3" or inp == "V" or inp == "v":
          link = raw_input("Enter Video Link: ")
          s.send(Packet().generate("POST video " + link, post))
          m = False

        elif inp == "5" or inp == "S" or inp == "s":
          s.send(Packet().generate("POST text", post))
          m = False

        else:
          m = True

      try:
        s.settimeout(10.0)
        data = s.recv(BUFFER_SIZE)
        response(data, "")

      except:
        pass

      s.close()

    # This is in reply to ENTERIES
    elif header == "ENTRIES":
      s = connect(TCP_IP, TCP_PORT)
      s.send(MESSAGE)
      data = s.recv(BUFFER_SIZE)
      response_file(data, "", s)

    # This is in reply to SEARCH
    elif header == "SEARCH":
      s = connect(TCP_IP, TCP_PORT)
      s.send(MESSAGE)
      data = s.recv(BUFFER_SIZE)
      response_file(data, "", s)
      s.close()

    # Send all other packets
    else:
      s = connect(TCP_IP, TCP_PORT)
      s.send(MESSAGE)
      try:
        s.settimeout(10.0)
        data = s.recv(BUFFER_SIZE)
        response(data, "")

      except:
        pass

      s.close()

  # Catch the control-c end
  except KeyboardInterrupt:
    # End connection
    print
    try:
      s = connect(TCP_IP, TCP_PORT)
      s.send(Packet().generate("QUIT " + str(USER), ""))
      s.settimeout(10.0)
      data = s.recv(BUFFER_SIZE)
      print
      response(data, "")
      s.close()
    except:
      pass
    on = False

  # Catch any other errors
  except Exception as err:
    print type(err)
    print err.args
    print err

