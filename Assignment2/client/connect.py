import socket

class Connect:
  '''Used by the client to establish types of connections'''

  def __init__(self, ip, port, user):
    self.ip = ip
    self.udp_id = ""
    self.port = port
    self.user = user
    self.TCP = False
    self.UDP = False
    self.connected = False

  def TCPConnect(self):
    try:
      self.TCP = True
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.s.connect((self.ip, self.port))
      self.connected = True
    except:
      self.connected = False

  def UDPConnection(self, udp_id):
    try:
      self.UDP = True
      self.udp_id = udp_id
      self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.connected = True
    except:
      self.connected = False

  def send(self, message):
    if self.TCP and self.connected:
      self.s.send(message)
    elif self.UDP and self.connected:
      self.s.sendto(message, (self.udp_id, 5005))
    else:
      print "No Connection."

  def recieve(self):
    if self.TCP and self.connected:
      return self.s.recv(1024)
    elif self.UDP and self.connected:
      data, addr = sock.recvfrom(1024)
      return data
    else:
      print "No Connection"

  def timeout(self, time):
    if self.TCP and self.connected:
      self.s.settimeout(time)
    elif self.UDP and self.connected:
      pass
    else:
      print "No Connection"

  def close(self):
    if self.TCP and self.connected:
      self.s.close()
    else:
      print "No Connection."
    self.TCP = False
    self.UDP = False
    self.connected = False
