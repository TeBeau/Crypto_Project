# HARD CODED VARIABLES
initial_permutation = [2, 6, 3, 1, 4, 8, 5, 7]
inverse_permutation = [4, 1, 3, 5, 7, 2, 8, 6]

# Used by f_function
expan_perm_4_to_8 = [4, 1, 2, 3, 2, 3, 4, 1]
last_perm = [2, 4, 3, 1]
s0 = [  [1, 0, 3, 2],
		[3, 2, 1, 0],
		[0, 2, 1, 3],
		[3, 1, 3, 2] ]

s1 = [  [0, 1, 2, 3],
		[2, 0, 1, 3],
		[3, 0, 1, 0],
		[2, 1, 0, 3] ]

# Used by get_Keys()
perm_10bit = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
perm_10_to_8 = [6, 3, 7, 4, 8, 5, 10, 9]


# Function takes the binary sequence and does permutation to the bit
def permutation(binary, perm):
	# New binary sequence
	new_binary = []
	for i in perm:
		# Add sequence in the order we want
		new_binary.append(binary[i-1])
	return new_binary

# This function splits the binary sequence into 2 binary sequences
# Example 8 bit --> 4 bit | 4 bit
# 		  10 bit--> 5 bit | 5 bit
# Return a tuple holding (b1, b2) --> b = b1 | b2 
def split(binary):
	# Find the center index
	middle = len(binary) // 2
	b1 = []
	b2 = []
	for i in range(middle):
		b1.append(binary[i])
		b2.append(binary[middle+i])
	return(b1, b2)

# This function combine the left and right bits into a single bit
# Example : 01 | 10 --> 0110 
def combine(bL, bR):
	new_binary = bL.copy()
	for i in range(len(bR)):
		new_binary.append(bR[i])
	return new_binary

# This function does a left cycle shift to the sequence
# Example 11011 ---> 10111
def leftShift(binary):
	new_binary = binary.copy()
	new_binary.pop(0)
	new_binary.append(binary[0])
	return new_binary

# This function does the XOR between two binary numbers
# Requires binary1 and binary2 to be same bit length
def XOR(binary1, binary2):
	new_binary = []
	for i in range(len(binary1)):
		# ^ performs xor between single bits
		new_binary.append( binary1[i] ^ binary2[i] )
	return new_binary

# This function goes through the Sub Matrix and returns a 2 bit
# Binary is 2 bits, s is a matrix 4x4
def sub_Matrix(binary, s):
	# Row is add of bit-1 and bit4
	row = get_value([binary[0], binary[3]])
	# Col is add of bit-2 and bit-3
	col = get_value([binary[1], binary[2]])
	# Look up the value in the s matrix and convert it to a 2 bit
	bit2 = get_binary( s[row][col] )
	# Return the 2 bit
	return bit2

# This function converts binary array to a integer val
def get_value(binary):
	val = 0
	size = len(binary) - 1
	for i in range(len(binary)):
		if( binary[i] == 1 ):
			val += 2**size
		size -= 1
	return val

# This function returns the 2 bit for the val given (0, 1, 2, 3)
def get_binary(val):
	if( val == 0 ):
		return [0,0]
	if( val == 1 ):
		return [0,1]
	if( val == 2 ):
		return [1,0]
	if( val == 3 ):
		return [1,1]
	#This should never get called given the sub matrix we have
	return [0,0]

# This is the f_function and takes a 4 bit binary sequence and a key
# Performs multiple operations and returns a 4 bit
def f_function(binary, key):
	# We get a 4 bit which we want to expand to an 8 bit
	bit8 = permutation(binary, expan_perm_4_to_8)

	# Now XOR this bit8 with an 8 bit key
	new_bit8 = XOR(bit8, key)

	# Now split 8 bit to two 4 bits
	bit4_L, bit4_R = split(new_bit8)

	# Now plug 2 bit into Substitution Matrix
	# Left side first
	bit2_L = sub_Matrix(bit4_L, s0)
	# Right side next
	bit2_R = sub_Matrix(bit4_R, s1)

	#Combine into 4 bit
	bit4 = combine(bit2_L, bit2_R)

	#Perform permutation and return the binary
	r_bit = permutation(bit4, last_perm)
	return r_bit

# This function takes an 10bit and returns 8 bit keys
# Cycle is 2 in this example, so it returns 2 keys
def get_keys(key, cycles):
	# List will hold the keys ---> [k1, k2, ....]
	r_keys = []

	#initital key is a 10 bit key, we must perm it
	bit10 = permutation(key, perm_10bit)

	#Split it into 5bits
	bit5_L, bit5_R = split(bit10)

	# We want to find multiple keys, in this example cycle will be 2
	while(cycles > 0):
		#Perform a left shift on both
		bit5_L = leftShift(bit5_L)
		bit5_R = leftShift(bit5_R)

		# Do a another left shift for the second one
		if(cycles == 1):
			bit5_L = leftShift(bit5_L)
			bit5_R = leftShift(bit5_R)

		# Combine L and R
		bit10 = combine(bit5_L, bit5_R)
		# Do perm
		tempkey = permutation(bit10, perm_10_to_8)
		# Add this key to the list
		r_keys.append(tempkey.copy())
		cycles -= 1
	# Return the keys
	return r_keys

# This function is main encryption and decryption part
# If encrypt is true, then you encypte, otherwise you decrypt
def DES(binary, key, cycles, encrypt):
	# Get the keys needed
	keys = get_keys(key, cycles)

	# binary is 8 bit plaintxt, we must perm it
	bit8 = permutation(binary, initial_permutation)

	# Must split the bits
	bit4_L, bit4_R = split(bit8)

	# If Encrypt is true, then want keys in order k1, k2
	if(encrypt):
		index = 0
	# Overwise, we want to decrypt and want keys in order k2, k1
	else:
		index = cycles - 1

	while(cycles > 0):
		# Temp values
		temp_R = bit4_R.copy()
		temp_L = XOR( bit4_L, f_function(bit4_R, keys[index]) )

		# Cross over
		bit4_L = temp_R.copy()
		bit4_R = temp_L.copy()

		# Keep Track of index and cycle
		if(encrypt):
			index += 1
		else:
			index -= 1

		cycles -= 1
	# Combine the bits
	bit8 = combine(bit4_R, bit4_L)

	# Permutation
	cipher = permutation(bit8, inverse_permutation)
	return cipher

def print_nice(plain, key, encrypt, decrypt):
	print("Plaintxt is :\t  ", bin_to_str(plain))
	print("Key is :\t", bin_to_str(key))
	print("Cipher is :\t  ", bin_to_str(encrypt))
	print("Answer is :\t  ", bin_to_str(decrypt))

# Display the binary in string of 0's and 1's for ease of view
def bin_to_str(binary):
	r_str = ""
	for i in binary:
		r_str = r_str + str(i)
	return r_str

# Conver the string to a binary sequence where each char is an 8 bit key
def string_to_bin(string):
	binary_str = []
	full = []
	for i in string:
		full.append(format(ord(i), 'b'))
	for i in full:
		temp = []
		for j in range(len(i)):
			temp.append((int)(i[j]))
		while (len(temp) < 8):
			# Make sure to add 0's to the front to make sre 8 bits
			temp.insert(0,0)
		for j in temp:
			binary_str.append(j)
	return binary_str

# Convert binary to string
def binary_to_string(binary):
	r_str = ""
	for i in range(0, len(binary), 8):
		# Move every 8 bits
		temp = binary[i:i+8]
		val = get_value(temp)
		r_str = r_str + chr(val)
	return r_str

# Add an arr to the end of the orginal array
def append_arr(original, add):
	for i in add:
		original.append(i)
