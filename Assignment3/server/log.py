import datetime

class Log:
  '''This is used to log errors and activity'''

  def error(self, content):
    f = open("error.log", "a")
    f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " --> " + content.replace("\n", ""))
    f.write("\n")
    f.close()
    print "Error On Server Side\nCheck error.log for complete information."

  def activity(self, content):
    f = open("activity.log", "a")
    f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " --> " + content.replace("\n", ""))
    f.write("\n")
    f.close()

