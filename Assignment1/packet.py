class Packet:
  '''Generates and Breaks down a Packet'''

  def generate(self, content, body):
    content = content.split(" ")
    header = content[0]
    data = ""
    for l in content[1:]:
      data = data + l + "&" 
    return header + "\r\n" + data + "\n\n" + body

  def divide(self, data):
    header, content = data.split("\r\n", 1)
    content, body = content.split("\n\n", 1)
    return header, content, body
