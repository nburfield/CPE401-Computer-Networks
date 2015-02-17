import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1) 

webpage = '<html><head><title>NOLAN</title></head><body><h1>Test Page</h1><p><a href="page2.html">It Worked</a></p></body></html>'
page2 = '<html><head><title>NOLAN</title></head><body><h1>Test Page</h1><p><font color="green">Page 2</font></p></body></html>'
errpage = '<html><head><title>ERROR</title></head><body><h1>Error Page</h1><p><font color="green">ERROR</font></p></body></html>'
form = '<html><body><form action="something.py">First Name:<br><input type="text" name="firstname">Last Name:<br><input type="text" name="lastname"><br><br><input type="submit" value="submit"></form></body></html>'

on = True
while on:
  try:
    conn, addr = s.accept()
    print 'Connection address:', addr
    data = conn.recv(BUFFER_SIZE)
    get, body = data.split('\r\n', 1)
    print "received data:", data
    t, page, ver = get.split(' ')
    if 'GET' == t:
      if page == '/':
        conn.send(form)
      elif page == '/page2.html':
        conn.send(page2)
      else:
        conn.send(errpage)
    conn.close()
  except KeyboardInterrupt:
    on = False
    print
  except:
    print "There was an Error."

