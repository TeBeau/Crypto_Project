import socket
import random
import encryptions as enc
import time

def Diffie_Hellman_Key_Exchange():
	# Diffie Helman Key Exchange
	s = ""
	p = random.choice(primes)
	g = p
	while (g == p):
		g = random.choice(primes)
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

primes = [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
		,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
		,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
		,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
		,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
		,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
		,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
		,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
		,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
		,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]

# Set up the TCP Server
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.bind( (socket.gethostname(), 1234 ) )
s.listen( 5 ) # Queue of 5
c, addr = s.accept()
print('Got connection from ', addr)
print()

# Key Exchange for SSL
key = Diffie_Hellman_Key_Exchange()

# Exchange n for Blum Gold
r_msg = "Hello"
msg = ""
while(r_msg != msg):
	p = random.choice(primes)
	q = p 
	while (p == q):
		q = random.choice(primes)
	if(p < q):
		temp = p
		p = q
		q = temp
	b, a = enc.Euclidean(p, q)
	n = p * q
	time.sleep(.5)
	send = str(n)
	c.send(send.encode())

	# Decrypt
	data = c.recv(1024).decode()
	msg = enc.Blum_Gold_Decrpyt(n, a, b, p, q, data )
	if(msg == r_msg):
		print("Exchange Complete\n")
		send = "Exchange Complete"
		c.send(send.encode())
		break
	else:
		send = "error"
		c.send(send.encode())

# Read the Messages from the ATM
while(True):
	data = c.recv(1024).decode()
	print("Recieved:", data)
	msg = enc.Blum_Gold_Decrpyt(n, a, b, p, q, data )
	user_mac = enc.parse_mac(data)
	print("user_mac is", user_mac)
	mac = enc.getMAC(msg, key)
	print("mac is", mac)
	print("After Decription:", msg)

	if(mac == user_mac):
		print("Verified that the MAC is correct")
	print()

