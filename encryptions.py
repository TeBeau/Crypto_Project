import math
import random
import SDES

# Get primes from seperate file
file = open("primes1.txt","r")
read = file.read()
primes = read.split()

# Return a random prime
def get_prime():
	val = int( random.choice(primes) )
	return val

# Parse and get p and g
# Return tuple (p, g)
def get_p_and_g(string):
	wait = True
	p_index = string.index("p =")
	p = ""
	for i in range(p_index, len(string)):
		if(string[i].isdigit()):
			wait = False
			p += string[i]
		else:
			if(wait == False):
				p = int(p)
				break
	wait = True
	g_index = string.index("g =")
	g = ""
	for i in range(g_index, len(string)):
		if(string[i].isdigit()):
			wait = False
			g += string[i]
		else:
			if(wait == False):
				g = int(g)
				break
	return(p, g)

# x0 is the first qr, n is n, size if the size we want
# Returns list of all of them
def get_quadratic_residues(x0, n, size):
	pos = 1
	x = [x0]	
	while( pos != size ):
		temp_x = (x[pos-1]*x[pos-1]) % n	# x_i = x_(i-1)^2 mod n
		x.append(temp_x)
		pos += 1
	return x

# Converts a string to binary, each letter is 8 bits (ie, can have leading zeros)
def convert_string_to_binary(string):
	bin_string = ''.join(format(ord(i),'b').zfill(8) for i in string)
	binary = []
	for i in bin_string:
		binary.append(int(i))
	return binary

# Convert a binary to a string
def convert_binary_to_string(binary):
	string = ""
	for i in range(0, len(binary), 8):
		string += chr(binary_to_int(binary[i:i+8]))
	return string

# Converts a binary to a string
def binary_to_int(binary):
	num = 0
	pos = len(binary) - 1
	for i in binary:
		if(i == 1):
			num += math.pow(2, pos)
		pos -= 1
	return (int)(num)

# Converts an int to a binary
def int_to_binary(num, size):
	binary = []
	while(num > 0):
		if(num % 2 == 0):
			binary.insert(0,0)
		else:
			binary.insert(0,1)
		num = num // 2
	while(len(binary) < size):
		binary.insert(0,0)
	return binary

# Gets the num least sig bits of the binary sequence
def get_least_significant_bits(binary, num):
	return binary[len(binary)-num:]

# XOR two binary numbers, must be same size
def XOR(bin1, bin2):
	binary = []
	for i in range(len(bin1)):
		if(bin1[i] == bin2[i]):
			binary.append(0)
		else:
			binary.append(1)
	return binary

# Function does num^exp mod mod
def mod(num, exp, mod):
	result = 1
	for i in range(exp):
		result *= num
		result = result % mod
	return result

# Returns a clear string as the binary
def binary_as_string(binary):
	string = ""
	for i in binary:
		string += str(i)
	return string

# Do the Blum Goldwasser Encrpytion
def Blum_Gold_Encrypt(n, x0, string):
	# Calculate k floor( lg n )
	k = math.floor( math.log( n, 2 ) ) # lg is log_2
	h = math.floor( math.log( k, 2 ) )

	# BEGIN ENCRYPTION PART -----------------------------------------------------------------
	binary = convert_string_to_binary(string) # Binary Sequence of the string

	# Get t --> number of m in the string
	t = len(binary) // h

	# Get the Quadratic Residues
	x = get_quadratic_residues(x0, n, t+5)

	ciphertext = [] # This will hold (c1, c2, c3, ..., ct, x_(t+1) )

	# Do the encryption:
	counter = 1
	for i in range(0, len(binary), h):
		mi = binary[i:i+h]
		while(len(mi) < h):
			mi.insert(0,0)
		# print("Mi",mi)
		xi = x[counter]
		counter += 1
		pi = get_least_significant_bits( int_to_binary( xi, h ), h )
		# print("pi", pi)
		c = XOR( pi, mi )
		ciphertext.append(c)
	ciphertext.append(x[counter]) # Add the x_(t+1) to the end of the ciphertext
	
	string = ""
	for i in range(len(ciphertext)-1):
		for j in range(len(ciphertext[i])):
			string += str(ciphertext[i][j])
	return str((string, ciphertext[-1]))
	# END OF ENCRYPTION PART -----------------------------------------------------------------

# Decrypt using Blum Goldwasser
def Blum_Gold_Decrypt(n, a, b, p, q, string):
	binary = []
	start = False
	for i in string:
		if(start):
			if(i == "'"):
				break
			binary.append(int(i))
		if(i == "'"):
			start = True
	index = string.index(",") + 2
	index2 = string.index(")")
	val = ""
	for i in range(index, index2):
		val += string[i]
	x = int(val)

	k = math.floor( math.log( n, 2 ) ) # lg is log_2
	h = math.floor( math.log( k, 2 ) )
	# Get t --> number of m in the string
	t = len(binary) // h

	d1 = mod( (p+1)//4, t+1, p-1)			# Formula from Notes
	d2 = mod( (q+1)//4, t+1, q-1)			# Formula from Notes
	u = mod( x, d1, p ) 					# Formula from Notes
	v = mod( x, d2, q ) 					# Formula from Notes
	x0 = ( v*a*p + u*b*q ) % n 						# Formula from Notes

	decryption = []		# Will hold decryption binary number

	x = get_quadratic_residues( x0, n, t+5)
	# Do the Decryption
	counter = 1
	for i in range(0, len(binary), h):
		mi = binary[i:i+h]
		while(len(mi) < h):
			mi.insert(0,0)
		# print("Mi",mi)
		xi = x[counter]
		counter += 1
		pi = get_least_significant_bits( int_to_binary( xi, h ), h )
		# print("pi", pi)
		d = XOR( pi, mi )
		for bit in d:
			decryption.append(bit)

	# Decryption binary convert to string
	string = convert_binary_to_string(decryption)
	return string

# Returns (n, a, b, p, q)
def get_Blum_Gold_Keys():
	r_msg = "Hello"
	msg = ""
	while(r_msg != msg):
		# print(".")
		p = get_prime()
		q = p 
		while (p == q):
			q = get_prime()
		if(p < q):
			temp = p
			p = q
			q = temp
		b, a = Euclidean(p, q)
		n = p * q
		# Encrypt
		x0 = random.randint(100001, 1000001 )
		cipher = Blum_Gold_Encrypt(n, x0, r_msg )
		# Decrypt
		msg = Blum_Gold_Decrypt(n, a, b, p, q, cipher )
		if(msg == r_msg):
			break
	return (n, a, b, p, q)

# Returns a and p such that pa + qb = 1
def Euclidean(p, q):
	r = p % q 
	d = p // q
	a_old = 1
	b_old = -1 * d
	if(r == 1):
		return (a_old, b_old)
	p = q
	q = r
	r = p % q 
	d = p // q
	a_new = -1 * d * a_old
	b_new = 1 + (d* b_old * -1)
	if(r == 1):
		return (a_new, b_new)
	p = q
	q = r
	while (r!=1):
		r = p % q 
		d = p // q
		a = a_old - (d * a_new)
		b = b_old - (d * b_new)
		a_old = a_new
		b_old = b_new
		a_new = a
		b_new = b
		p = q
		q = r
	return (b, a)

# Get the MAC from the Message, check to see if it is valid
def parse_mac(string):
	index = string.index("MAC =")
	start = False
	mac = ""
	for i in range(index, len(string)):
		if(string[i].isdigit()):
			start = True
		if(string[i].isdigit() and start):
			mac += string[i]
	return mac

