import socket
import os
import sys
from Queue import Queue
from threading import Thread

# Import the built classes
from register import Register
from login import Login
from packet import Packet
from log import Log
from update import Update
from friend import Friend
from chat import Chat

'''
   This is a simple server side of a social network. To start the program run python server.py <port-number>
'''

# Setup Server Data
# TCP_IP = socket.gethostname()
# print TCP_IP
TCP_IP = "127.0.0.1"
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024

# Initilize the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

def server_loop(conn, addr):
  USER_ID = None

  on = True
  while on:
    # Run the typical TCP server
    try:
      if not conn: conn, addr = s.accept()
      print 'Connection address:', addr
      data = conn.recv(BUFFER_SIZE)

      if not data:
        data = Packet().generate("<NoData> <NoData>", "")

      # Run the recieved command
      header, content, body = Packet().divide(data)

      # Runs the register packet data
      if header == "REGISTER":
        print "Recieved Register Packet ... ",
        print "... Packet Processing ...",
        c, error =  Register().server(content)
        if c:
          print "... User " + c + " registered."
          conn.send(Packet().generate("ACK " + c + " " + str(addr[0]) + " " + str(addr[1]), "User " + c + " Registered"))
        else:
          Log().server_error(error)
          conn.send(Packet().generate("ERR", error))

        conn.close()
        conn = None

      # Runs the update of a user profile data
      elif header == "UPDATE":
        print "Recieved Update Packet ... ",
        print "... Getting all the file data ... ",
        MSGLEN = int(content.split("&")[0])
        bytes_recd = 0
        while len(body) < MSGLEN:
          data_recv = conn.recv(min(MSGLEN - bytes_recd, BUFFER_SIZE))
          if data_recv == b'':
            print "... File data failed."
            Log().server_error("Socket connection broken when updating profile.")
            break
          body = body + data_recv

        if not len(body) < MSGLEN:
          print "... Recieved all file data ... Adding record to database ...",
          success, time, error = Update().server(USER_ID, body)
          if success:
            print "... Profile successfully updated."
            conn.send(Packet().generate("SUCCESS " + str(time), "Profile was updated with the time: " + str(time)))
          else:
            Log().server_error(error)
            conn.send(Packet().generate("ERR", error))

        conn.close()
        conn = None

      # Login
      elif header == "LOGIN":
        print "Attempt to login user ...",
        USER_ID = int(content.split("&")[0])
        error, friends = Login().login(USER_ID, addr[0], addr[1])
        if error:
          print "... Login failed."
          Log().server_error(error)
          conn.send(Packet().generate("ERR", error))
        else:
          print "... Login Successful."
          Log().server_activity("Login of user: " + str(USER_ID))
          conn.send(Packet().generate("", "Login of user: " + str(USER_ID) + friends))

        conn.close()
        conn = None

      # Logout
      elif header == "QUIT":
        on = False
        print "Attempt to logout user ...",
        USER_ID = int(content.split("&")[0])
        error = Login().logout(USER_ID, addr[0])
        if error:
          print "... Logout failed."
          Log().server_error(error)
          conn.send(Packet().generate("ERR", error))
        else:
          print "... Logout Successful."
          Log().server_activity("Logout of user: " + str(USER_ID))
          conn.send(Packet().generate("", "Logout of user: " + str(USER_ID)))
          USER_ID = None

        conn.close()
        conn = None

      # Create friend request
      elif header == "FRIEND":
        print "Creating a friend request query ...",
        friend_id = int(content.split("&")[0])
        error = Friend().create(USER_ID, friend_id)
        if error:
          print "... request failed."
          Log().server_error(error)
          conn.send(Packet().generate("ERR", error))
        else:
          print "... request Successful."
          Log().server_activity("Friend request from user " + str(USER_ID) + " to user " + str(friend_id))
          conn.send(Packet().generate("", "Friend request from user " + str(USER_ID) + " to user " + str(friend_id)))

        conn.close()
        conn = None

      # Confirm an existing friend request
      elif header == "CONFIRM":
        print "Confirming a friend request query ...",
        friend_id = int(content.split("&")[0])
        error = Friend().confirm(USER_ID, friend_id)
        if error:
          print "... request failed."
          Log().server_error(error)
          conn.send(Packet().generate("ERR", error))
        else:
          print "... request Successful."
          Log().server_activity("Friend request from user " + str(USER_ID) + " to user " + str(friend_id) + " accepted.")
          conn.send(Packet().generate("", "Friend request from user " + str(USER_ID) + " to user " + str(friend_id) + " accepted."))

        conn.close()
        conn = None

      # Reject a friend request
      elif header == "REJECT":
        print "Rejecting a friend request query ...",
        friend_id = int(content.split("&")[0])
        error = Friend().reject(USER_ID, friend_id)
        if error:
          print "... request failed."
          Log().server_error(error)
          conn.send(Packet().generate("ERR", error))
        else:
          print "... request Successful."
          Log().server_activity("Friend request from user " + str(USER_ID) + " to user " + str(friend_id) + " rejected.")
          conn.send(Packet().generate("", "Friend request from user " + str(USER_ID) + " to user " + str(friend_id) + " rejected."))

        conn.close()
        conn = None

      # For the CHAT of users
      elif header == "CHAT":
        print "Sending a chat message ...",
        if not conn: conn, addr = s.accept()
        post = conn.recv(BUFFER_SIZE)
        header, dummy, body = Packet().divide(post)

        if not post or header != "CHAT":
          print "... chat failed, there was no message recieved."
          Log().server_error("Chat from user " + str(USER_ID) + " did not recieve data.")
          conn.send(Packet().generate("ERR", "Chat from user " + str(USER_ID) + " did not recieve data."))
          conn.close()
          conn = None
          break

        error, online = Chat().chat(USER_ID, int(content.split("&")[0]), body)
        if error:
          print "... chat failed."
          Log().server_error(error)
          conn.send(Packet().generate("ERR", error))
        else:
          print "... chat Successful."
          if online:
            Log().server_activity("Chat Message from " + str(USER_ID) + " to " + content.split("&")[0] + " sent.")
            conn.send(Packet().generate("DELIVERED " + content.split("&")[0], "Chat Message from " + str(USER_ID) + " to " + content.split("&")[0] + " sent."))
          else:
            Log().server_activity("Chat Message from " + str(USER_ID) + " to " + content.split("&")[0] + " saved to database, user is not online.")
            conn.send(Packet().generate("OFFLINE " + content.split("&")[0], "Chat Message from " + str(USER_ID) + " to " + content.split("&")[0] + " saved to database, user is not online."))

        conn.close()
        conn = None

      # This is a POST to a persons wall
      elif header == "POST":
        print "Adding a wall post ..."
        post = conn.recv(BUFFER_SIZE)
        header, c_type, body = Packet().divide(post)

        if not post or header != "POST":
          print "... post failed, there was no post recieved."
          Log().server_error("Post of wall post from user " + str(USER_ID) + " did not recieve data.")
          conn.send(Packet().generate("ERR", "Post of wall post from user " + str(USER_ID) + " did not recieve data."))
          conn.close()
          conn = None
          break

        error = Chat().post(USER_ID, content.split("&")[0], body, c_type)
        if error:
          print "... post failed."
          Log().server_error(error)
          conn.send(Packet().generate("ERR", error))
        else:
          print "... post Successful."
          Log().server_activity("Posting of wall post:\n" + body + "\nFrom user " + str(USER_ID) + " was successful.")
          conn.send(Packet().generate("", "Posting of wall post:\n" + body + "\nFrom user " + str(USER_ID) + " was successful."))

        conn.close()
        conn = None

      # This is an inquiry by a user for their wall
      elif header == "ENTRIES":
        print "Gathering wall post queries ... ",
        error, data = Chat().entries(USER_ID, int(content.split("&")[0]))
        if error:
          print "... wall return failed."
          Log().server_error("Return of the WALL queries From user " + str(USER_ID) + " failed.")
          conn.send(Packet().generate("ERR ", data))
        else:
          print "... wall return successful."
          Log().server_activity("Return of the WALL queries From user " + str(USER_ID) + " was successful.")
          conn.send(Packet().generate("WALL " + str(len(data)) + " wall_queries.xml", data))

        conn.close()
        conn = None

      # A search query by the user
      elif header == "SEARCH":
        print "Gathering user profile queries ... ",
        error, data = Chat().search(USER_ID, content.split("&")[0])
        if error:
          print "... profile return failed."
          Log().server_error("Return of the profile queries From user " + str(USER_ID) + " failed.")
          conn.send(Packet().generate("ERR ", data))
        else:
          print "... profile return successful."
          Log().server_activity("Return of the profile queries From user " + str(USER_ID) + " was successful.")
          conn.send(Packet().generate("RESULTS " + str(len(data)) + " profile_queries.xml", data))

        conn.close()
        conn = None

      # This is a bad packet, one the server does not recognize
      else:
        conn.close()
        conn = None
        Log().server_error("Recieved Back Packet: header => " + header + " content => " + content + "\n")

    # Catch the control-c end
    except KeyboardInterrupt:
      # Close the connection
      print
      if conn: conn.close()
      on = False
      print

    # Catch any other errors
    except Exception as err:
      print type(err)     # the exception instance
      print err.args      # arguments stored in .args
      print err           # __str__ allows args to printed directly

# Classes for running the thread pool
class Worker(Thread):
  '''This is used as the thread executer'''

  def __init__(self, tasks):
    Thread.__init__(self)
    self.tasks = tasks
    self.daemon = True
    self.start()

  def run(self):
    while True:
      func, args, kargs = self.tasks.get()
      try:
        func(*args, **kargs)
      except Exception, e:
        print e
      finally:
        self.tasks.task_done()

class ThreadPool:
  '''The thread pool.'''
  def __init__(self, num_threads):
    self.tasks = Queue(num_threads)
    for _ in range(num_threads): Worker(self.tasks)

  def add_task(self, func, *args, **kargs):
    '''Adds the task to the queue'''
    self.tasks.put((func, args, kargs))

  def wait_completion(self):
    '''Wait for the tasks to end'''
    self.tasks.join()


if __name__ == '__main__':
  pool = ThreadPool(5)
  while True:
      conn, addr = s.accept()
      pool.add_task(server_loop(conn, addr))

  pool.wait_completion()

