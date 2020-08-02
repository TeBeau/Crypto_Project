import socket
import random
import encryptions as enc
import time

def Diffie_Hellman_Key_Exchange():
	# Diffie Hellman Key Exchange
	msg = s.recv(1024).decode("utf-8")
	print(msg)
	# get p and q from back
	p, g = enc.get_p_and_g(msg)
	print("Generating random a")
	# Generate private key
	private_a = random.randint(100, 1000)
	public_a = enc.mod(g, private_a, p)
	print("Sending Public Key:", public_a)
	send = str(public_a)
	s.send(send.encode())
	print()
	# Recieve Public Key from the Back
	msg = s.recv(1024).decode("utf-8")
	public_b = int(msg)
	print("Recieved Public Key From Bank:", public_b)
	print()
	# Make Secret Key
	print("Generate Secret Key")
	secret = enc.mod(public_b, private_a, p)
	print()
	return secret

# random.seed(time.time() * 9827 % 45678)
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( (socket.gethostname(), 1234) )


key = Diffie_Hellman_Key_Exchange()

recieved = "Exchange Complete"
msg = ""
while (recieved != msg):
	msg = s.recv(1024).decode("utf-8")
	# print("Recieved n", msg)
	n = int(msg)
	message = "Hello"
	cipher = enc.Blum_Gold_Encypt(n, 159201, message )
	s.send(cipher.encode())
	msg = s.recv(1024).decode("utf-8")


print("Recieved n = {} for Blum Gold Encryption".format(n) )
while True:
	message = input("Type Message To send to the Bank\n")
	cipher = enc.Blum_Gold_Encypt(n, 159201, message )
	mac = enc.getMAC(message, key)
	send = cipher + " MAC = " + mac
	print("Sending the ciphertext")
	print(send)
	s.send(send.encode())
	print()