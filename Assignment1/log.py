import datetime

class Log:
  '''This is used by both client and server to log errors and activity'''

  def server_error(self, content):
    f = open("server.error.log", "a")
    f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " --> " + content.replace("\n", ""))
    f.write("\n")
    f.close()
    print "Error On Server Side\nCheck server.error.log for complete information."

  def server_activity(self, content):
    f = open("server.activity.log", "a")
    f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " --> " + content.replace("\n", ""))
    f.write("\n")
    f.close()

  def client_error(self, content):
    f = open("client.error.log", "a")
    f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " --> " + content.replace("\n", ""))
    f.write("\n")
    f.close()
    print "Error On Client Side\nCheck client.error.log for complete information."

  def client_activity(self, content):
    f = open("client.activity.log", "a")
    f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " --> " + content.replace("\n", ""))
    f.write("\n")
    f.close()

