import socket
import random
import encryptions as enc
import time
import Bank
import mac as HMAC
import des as DES

def Diffie_Hellman_Key_Exchange():
	# Diffie Helman Key Exchange
	s = ""
	p = enc.get_prime()
	g = p
	while (g == p):
		g = enc.get_prime()
	string = "Start DH Key Exchange\np = {}\ng = {}\n".format(p, g)
	print(string)
	c.send(string.encode("utf-8"))	
	# Get ATM Public Key
	data = c.recv(1024).decode()
	print("Received public key from ATM:", data)
	public_a = int(data)
	print()
	# Send Back Public Key Back
	private_b = random.randint(100, 1000)
	public_b = enc.mod(g, private_b, p)
	print("Sending Public Key to ATM:", public_b)
	print()
	send = str(public_b)
	c.send(send.encode())
	# Generate the secret key
	print("Generate Secret Key")
	secret = enc.mod(public_a, private_b, p)
	print()
	return secret


# Set up the TCP Server
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.bind( (socket.gethostname(), 1234 ) )
s.listen( 5 ) # Queue of 5
c, addr = s.accept()
print('Got connection from ', addr)
print()

# Key Exchange for SSL
key = Diffie_Hellman_Key_Exchange()

# Get the suite from the client
name = c.recv(1024).decode()
c.send("recieved".encode())
select = c.recv(1024).decode()
print(select)

# Exchange n for Blum Gold
# Send over bank's public key
# Generate Keys
n, a, b, p, q = enc.get_Blum_Gold_Keys()
print("Sending over public key n:", n)
send = str(n)
c.send(send.encode("utf-8"))
s
# Get ATM's public key
msg = c.recv(1024).decode()
n_ATM = int(msg)
print("Recieved ATM's public key:", n_ATM)

bank = Bank.Bank(name)	# <== Put the ATM users name here

# Read the Messages from the ATM
while(True):
	# Get the message
	data = c.recv(1024).decode()
	data_no_mac = data[:data.index("M") - 1]
	print("Recieved:", data)
	# Decrypt
	if(select == "BLUM"):
		msg = enc.Blum_Gold_Decrypt(n, a, b, p, q, data )
	elif( select == "DES" ):
		msg = DES.decrypt( data_no_mac, key )
	else:
		# 3 DES
		msg = DES.decrypt3( data_no_mac, key )

	# Get the mac the ATM send over
	user_mac = enc.parse_mac(data)
	# Get the mac of the message
	mac = HMAC.mac(msg, key)

	message = msg[:msg.index("-")]
	# Get the time stap of the message
	time_msg = int( msg[msg.index("-") + 1:])

	# Check that the MAC and TimeStamp Match
	if(mac == user_mac and (time_msg < time.time() + 1)):
		returnVal = -1

		if msg[0:7] == "Deposit":
			returnVal = bank.deposit(round(float(msg[8:msg.index("-")-1]), 2))
		elif msg[0:8] == "Withdraw":
			returnVal = bank.withdraw(round(float(msg[9:msg.index("-")-1]), 2))
		elif msg[0:13] == "Check Balance":
			returnVal = bank.queryBalance()
		elif msg == "Quit":
			send = "Quit"

		if returnVal == -1:
			send = "Transaction unsuccessful"
		else:
			send = "Transaction successeful. Balance: " + str(returnVal)
		#send = "Transaction successeful. Balance: " + str(returnVal)
	else:
		send = "Could not verify that it is you"

	# Attach the time stamp to the message
	send = send + " -" + str(int(time.time()))
	# Return an Encypted message
	x0 = random.randint(100001, 1000001 )
	# Get the mac
	mac = HMAC.mac(send, key)
	if( select == "BLUM" ):					
		send = enc.Blum_Gold_Encrypt(n_ATM, x0, send )
	elif( select == "DES" ):
		send = DES.encrypt( send, key )
	else:
		# 3 DES
		send = DES.encrypt3( send, key )

	send = send + " MAC = " + mac
	c.send(send.encode())
	print("Sent reply to ATM\n")
	if(message == "Quit "):
		break

c.close()
s.close()
print("Closed Server")

