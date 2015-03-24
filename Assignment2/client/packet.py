from log import Log

class Packet:
  '''Used to Create and Dissemple a Packet'''

  def build(self, value, body):
    value = value.split(' ')
    packet = value[0] + '\r\n\r'
    for i in range(1, len(value)):
      packet += value[i] + '%'
    return packet + "\r\n\r" + body

  def divide(self, value):
    head = value.split('\r\n\r')
    meta = head[1].split('%')
    return head[0], meta, head[2]
