from database import User
from database import Friend_Request
from database import Message
import time

class Friend:
  '''This is used by the server to accept, reject, and create friend requests.'''

  def create(self, U_ID, TO_ID):
    if U_ID == None: return "No user logged in."
    if U_ID == TO_ID: return "User cannot be friend with them self."

    try: 
      user_two = User.get(User.ident == TO_ID)
    except:
      return "User " + str(TO_ID) + " does not exist."

    try:
      Friend_Request.get(userone_id = U_ID, usertwo_id = TO_ID)
      return "Friend request between " + str(U_ID) + " and " + str(TO_ID) + " already exists."
    except:
      pass

    f = Friend_Request(userone_id = U_ID, usertwo_id = TO_ID, accepted = None)
    f.save()
    return None

  def confirm(self, U_ID, TO_ID):
    if U_ID == None: return "No user logged in."
    if U_ID == TO_ID: return "User cannot be friend with them self."

    try:
      f = Friend_Request.select().where((Friend_Request.userone_id == TO_ID) & (Friend_Request.usertwo_id == U_ID) & (Friend_Request.accepted >> None))[0]
      f.accepted = True
      f.save()
      f = Friend_Request(userone_id = U_ID, usertwo_id = TO_ID, accepted = True)
      f.save()
      mess = "User " + str(U_ID) + " accepted your friend request."
      m = Message(userfrom_id = U_ID, userto_id = TO_ID, message = mess, group = 0, time = int(time.time()), attachment = 0, link = None)
      m.save()
      return None
    
    except:
      return "Pending Friend request between " + str(U_ID) + " and " + str(TO_ID) + " does not exists."

  def reject(self, U_ID, TO_ID):
    if U_ID == None: return "No user logged in."
    if U_ID == TO_ID: return "User cannot be friend with them self."

    try:
      f = Friend_Request.select().where((Friend_Request.userone_id == TO_ID) & (Friend_Request.usertwo_id == U_ID) & (Friend_Request.accepted >> None))[0]
      f.accepted = False
      f.save()
      f = Friend_Request(userone_id = U_ID, usertwo_id = TO_ID, accepted = False)
      f.save()
      return None

    except:
      return "Pending Friend request between " + str(U_ID) + " and " + str(TO_ID) + " does not exists."
