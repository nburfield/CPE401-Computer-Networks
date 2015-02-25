from database import User
import datetime

class Register:
  
  def server(self, content):
    ID = content.split("&")

    if len(ID) < 4:
      return False, "Do not leave a field blank, required data is: <user-id> <user-firstname> <user-lastname>"

    XML = "<profile>\n  <info>\n    <ID>" + ID[0] + "</ID>\n    <first>" + ID[1] + "</first>\n    <last>" + ID[2] + "</last>\n    <time>" + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + "</time>\n  </info>\n</profile>"
    try:
      user = User(ident = ID[0], first = ID[1], last = ID[2], profile = XML, online = False, port = None, ip = None)
      user.save()
      return str(ID[0]), ""
    except:
      return False, "Registration of user: ID => " + ID[0] + " First => " + ID[1] + " Last => " + ID[2] + " Failed. Selected ID is not available."
