import socket
import random
import encryptions as enc
import time
import mac as HMAC
import des as DES

# This function does the Diffie_Hellman Key Exchange Protocol
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


# Set up the TCP sockets to exchange messages
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( (socket.gethostname(), 1234) )

# Assume this is Completely Hidden
users= dict()
users['Lauren'] = 1013
users['Alex'] = 9742
users['JJ'] = 7959
# Assume this is Completely Hidden

# Ask the user to enter username (equivalent to inserting card) and pin
right_pin=False
while right_pin == False:
	username= input("Input your username:")
	pin= int(input("Input your pin#:"))
	if username in users:
		if users[username]==pin:
			right_pin=True
		else:
			print("Error: wrong pin #")
	if username not in users:
		print("Error: wrong username")


# Diffie Hellman_Key_Exchange
key = Diffie_Hellman_Key_Exchange()


select = random.choice(["DES", "BLUM", "3DES"])
s.send(username.encode())
s.recv(1024)
s.send(select.encode())

# Blum Goldwasser Key Exchange
# Generate keys
n, a, b, p, q = enc.get_Blum_Gold_Keys()
# Get public key from the bank
msg = s.recv(1024).decode("utf-8")
n_bank = int(msg)
print("Recieved public key from Bank: {}".format(n_bank) )

# Send over public key for the bank
send = str(n)
print("Sending over public key n:", n)
s.send(send.encode())
print()


# will use this bool to find if under overdraws
withdrawFlag = False;
quitFlag = False

run = True
while run:
	# Get the instuction, only 4 instructions exist
	message = input("Send instruction ( Deposit / Withdraw / Check Balance / Quit ):\n")
	if(message == "Check Balance"):
		pass
	elif(message == "Deposit" or message == "Withdraw"):
		# Get the amount
		amount = input("Enter the amount you wish to deposit or withdraw:\n")
		if int(amount) <= 0:
			print("Invalid amount requested... Must be greater than 0")
			continue
		message = message + " " + amount

		withdrawFlag = True
	elif(message == "Quit"):
		# Don't break out yet, need to tell server we are quitting
		run = False
		quitFlag = True
	else:
		print("Invalid input... Must match exact instructions")
		continue;
	# Add a time stap to the message to void replay attacks
	message = message + " -" + str(int(time.time()))
	# Gererate random quadratic residuosity
	x0 = random.randint(100001, 1000001 )
	# Encrypt the message
	if( select == "BLUM" ):
		cipher = enc.Blum_Gold_Encrypt(n_bank, x0, message )
	elif( select == "DES" ):
		cipher = DES.encrypt( message, key )
	else:
		# 3 DES
		cipher = DES.encrypt3( message, key )

	# Get the MAC
	mac = HMAC.mac(message, key)
	# # Send over the Encrypted message
	send = cipher + " MAC = " + mac 
	print("Sending the ciphertext:", send)
	s.send(send.encode())
	print()

	# Recieve Response
	data = s.recv(1024).decode("utf-8")

	data_no_mac = data[:data.index("M") - 1]
	# print(data_no_mac)
	if quitFlag == False:
		print(data)
	if( select == "BLUM"):
		msg = enc.Blum_Gold_Decrypt(n, a, b, p, q, data)
	elif( select == "DES" ):
		msg = DES.decrypt( data_no_mac, key )
	else:
		# 3 DES
		msg = DES.decrypt3( data_no_mac, key )
	
	# Look at MAC recieved from the BANK
	user_mac = enc.parse_mac(data)
	mac = HMAC.mac(msg, key)		
	# Get Just the Message
	message = msg[:msg.index("-")]
	# Get the TimeStamp
	time_msg = int( msg[msg.index("-") + 1:])

	# if user said 'Quit', don't print out any message verification stuff, just exit
	if quitFlag == True:
		break
	# Check that the MAC and TimeStamp Match
	if(mac == user_mac and (time_msg < time.time() + 1)):
		print("Verified message from the Bank:")
		print(message)
		if withdrawFlag == True and message == "Transaction unsuccessful ":
			print("ERROR: Overdraw")
			withdrawFlag = False
	else:
		print("Could not verify the message from the Bank")
	print()
# Close the socket
s.close()
print("Closed ATM")
