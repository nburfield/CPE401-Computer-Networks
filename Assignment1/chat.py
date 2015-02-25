from database import Message
from database import User
from database import Friend_Request
from database import Chat_Message
import time
import datetime

class Chat:
  '''This is the chat function used by the server to send the messages.'''

  def post(self, ID, group, message, content):
    if ID == None: return "No user logged in."

    # Get the proper type of attachment to the post
    content = content.split("&")
    if content[0].lower() == "text":
      a = 0 
      l = None
    elif content[0].lower() == "image":
      a = 1
      l = content[1]
    elif content[0].lower() == "video":
      a = 2
      l = content[1]
    elif content[0].lower() == "audio":
      a = 3
      l = content[1]
    else:
      return "There was a malformend packet when trying to make a wall post."

    # Get the proper group to post to
    if group.lower() == "friend":
      g = 1
    elif group.lower() == "circle":
      g = 2
    elif group.lower() == "public":
      g = 3
    else:
      return "There was a malformend packet when trying to make a wall post."

    # Compile the list of friends with their user ID
    try:
      people = []
      people.append(ID)
      if g == 1 or g == 2:
        for f in Friend_Request.select().where((Friend_Request.userone_id == ID) & (Friend_Request.accepted == True)):
          people.append(f.usertwo_id)

      people_2 = []
      if g == 2:
        for person in people:
          for f in Friend_Request.select().where((Friend_Request.userone_id == person) & (Friend_Request.accepted == True)):
            if not f.usertwo_id in people:
              people_2.append(f.usertwo_id)

      for person in people_2:
        people.append(person)


      if g == 3:
        for f in User.select():
          if not f.ident in people: people.append(f.ident)

      for person in people:
        m = Message(userfrom_id = ID, userto_id = person, message = message, group = g, time = int(time.time()), attachment = a, link = l)
        m.save()

      return None
    except:
      return "There was an error when adding all the messages to the database."

  
  def entries(self, ID, t):
    if ID == None: return True, "No user logged in."
    XML = "<content>\n"
    for m in Message.select().where((Message.userto_id == ID) & (((int(time.time())/3600) - (Message.time/3600)) < t)):
      XML += "  <post>\n"
      XML += "    <to>"
      if m.group == 1:
        XML += "friend"
      elif m.group == 2: 
        XML += "circle"
      else:
        XML += "public"
      XML += "</to>\n"
      user = User.get(User.ident == m.userfrom_id)
      XML += "    <from>" + user.first + " " + user.last + "</from>\n"
      XML += "    <time>" + str(datetime.datetime.fromtimestamp(m.time).strftime('%Y-%m-%d %H:%M:%S')) + "</time>\n"
      XML += "    <type>"
      if m.attachment == 0:
        XML += "text</type>\n"
      elif m.attachment == 1:
        XML += "image</type>\n"
        XML += "    <item>\n"
        XML += "      " + str(m.link) + "\n"
        XML += "    </item>\n"
      elif m.attachment == 2:
        XML += "video</type>\n"
        XML += "    <item>\n"
        XML += "      " + str(m.link) + "\n"
        XML += "    </item>\n"
      else:
        XML += "audio</type>\n"
        XML += "    <item>\n"
        XML += "      " + str(m.link) + "\n"
        XML += "    </item>\n"

      XML += "    <info>\n" + m.message + "    </info>\n"
      XML += "  </post>\n"


    XML += "</content>"

    return False, XML


  def search(self, ID, key):
    if ID == None: return True, "No user logged in."

    XML = "<search>\n"
    id_keep = 0
    for user in User.select():
      if key.lower() in user.profile.lower():
        XML += "  <find id='" + str(id_keep) + "'>\n"
        id_keep += 1
        XML += user.profile
        XML += "  </find>\n"

    XML += "</search>"
    return False, XML

  def chat(self, ID, reciever, body):
    if ID == None: return "No user logged in.", False

    try:
      r = User.get(User.ident == reciever)
    except:
      return "No user with the user id: " + str(reciever) + " exists.", False

    body = "\r\n\r" + body.replace("\r\n\r", "\n")
    try: 
      message = Chat_Message.select().where((Chat_Message.userfrom_id == ID) or (Chat_Message.userto_id == ID))
      for i in message:
        if i.userfrom_id == reciever or i.userto_id == reciever:
          message = i 
          break
      message.userfrom_id = ID
      message.userto_id = reciever
      message.message += body
      message.counter += 1
      message.read = False
      message.save()
    except:
      message = Chat_Message(userfrom_id = ID, userto_id = reciever, message = body, counter = 0, read = False)
      message.save()

    return "", r.online



















