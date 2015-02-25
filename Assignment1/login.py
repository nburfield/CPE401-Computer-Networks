from database import User
from database import Friend_Request
from database import Message
from database import Chat_Message
import time

class Login:
  '''This is used to start a user logged in, and end a user log in.'''

  def login(self, ID, ip, port):
    try:
      user = User.get(User.ident == ID)
    except:
      return "User " + str(ID) + " does not exist.", ""

    f_requests = ""
    for r in Friend_Request.select().where(Friend_Request.usertwo_id == ID, Friend_Request.accepted == None):
      f_requests += "\nUser " + str(r.userone_id) + " wants to be your friend."

    if f_requests: f_requests = " Friend Requests\n=================\n" + f_requests + "\n\n"

    m = ""
    for r in Message.select().where(Message.userto_id == ID, Message.group == 0):
      m += "\n" + r.message
      r.delete_instance()

    if m: m = " Messages\n==========\n" + m + "\n\n"

    c = ""
    for r in Chat_Message.select().where(Chat_Message.userto_id == ID & Chat_Message.read == False):
      c += "\n" + r.message
      r.read = True
      r.save()
      mess = Message(userfrom_id = ID, userto_id = r.userfrom_id, message = str(ID) + " read your chat.", group = 0, time = int(time.time()), attachment = 0, link = None)
      mess.save()

    if c: c = " Unread Chat\n============\n" + c + "\n\n"

    user.online = True
    user.port = port
    user.ip = ip
    user.save()
    return None, "\n" + f_requests + m + c

  def logout(self, ID, ip):
    try:
      user = User.get(User.ident == ID)
    except:
      return "User " + str(ID) + " does not exist."

    if user.ip != ip or not user.online:
      return "User " + str(ID) + " was not logged in on that IP address."

    user.online = False
    user.save()
    return None

