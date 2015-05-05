from Crypto.PublicKey import RSA
import base64
from base64 import b64decode

message = "Hello Here is a message to be sent\r\n\rYa"
print "Unchanged:\n", message, "\n\n\n"

new_key = RSA.generate(1024)
public = new_key.publickey()
private_file = open("PrivateKey", 'wb')
private_file.write(new_key.exportKey())
private_file.close()
public_file = open("PublicKey", 'wb')
public_file.write(public.exportKey())
public_file.close()


sutf8 = message.encode('utf8')
enc = public.encrypt(sutf8, None)[0]
value = base64.encodestring(enc)
print "Encrypted:\n", value, "\n\n\n"

private_key_file = open("PrivateKey", 'r')
rsa_key = RSA.importKey(private_key_file.read())
private_key_file.close()
raw_cipher_data = b64decode(value)
decrypt = rsa_key.decrypt(raw_cipher_data)
print "Decrypted:\n", decrypt, '\n\n\n'
