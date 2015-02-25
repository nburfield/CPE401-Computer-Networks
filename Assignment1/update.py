import os
from database import User
import re

class Update:
  '''This is used for the update of a profile by both server and client'''

  def server(self, ID, contents):
    try:
      query = User.get(ident = ID)
    except:
      return False, "", "Could not update the user " + str(ID) + " with the file."

    query.profile = contents
    f = re.compile('<first>([^)]*)</first>').search(contents)
    l = re.compile('<last>([^)]*)</last>').search(contents)
    if f: query.first = f.groups()[0]
    if l: query.last = l.groups()[0]
    query.save()

    t = re.compile('<time>([^)]*)</time>').search(contents)
    if t:
      time = t.groups()[0]
    else:
      time = "Undefined"

    return True, time, ""



  def client(self, arguments):
    meta = arguments.split("&")

    if not os.path.isfile(meta[1]):
      return False, "File " + meta[1] + " not found."

    f = open(meta[1], "r")
    data = f.read()
    f.close()
    return data, ""
