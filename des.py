import random
import encryptions as enc
import mac

# Usage: call the encrypt or the decrypt functions, with the message in regular string format, and the shared key between the client and the server (in int form)

initial_perm = [58, 50,	42,	34,	26,	18,	10,	2, 
				60, 52, 44, 36, 28, 20, 12, 4,
				62,	54,	46,	38,	30,	22,	14,	6,
				64,	56,	48,	40,	32,	24,	16,	8,
				57,	49,	41,	33,	25,	17,	9,  1,
				59,	51,	43,	35,	27,	19,	11,	3,
				61,	53,	45,	37,	29,	21,	13,	5,
				63,	55,	47,	39,	31,	23,	15,	7]

key_perm = 	[57, 49, 41, 33, 25, 17, 9,
			 1, 58, 50, 42, 34, 26, 18,
			 10, 2, 59, 51, 43, 35, 27,
			 19, 11, 3, 60, 52, 44, 36,
			 63, 55, 47, 39, 31, 23, 15,
			 7, 62, 54, 46, 38, 30, 22,
			 14, 6, 61, 53, 45, 37, 29,
			 21, 13, 5, 28, 20, 12, 4]

final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
			  39, 7, 47, 15, 55, 23, 63, 31,
			  38, 6, 46, 14, 54, 22, 62, 30,
			  37, 5, 45, 13, 53, 21, 61, 29,
			  36, 4, 44, 12, 52, 20, 60, 28,
			  35, 3, 43, 11, 51, 19, 59, 27,
			  34, 2, 42, 10, 50, 18, 58, 26,
			  33, 1, 41, 9,  49, 17, 57, 25]

expansion_perm = 	[32, 1,  2,  3,  4,  5,  4,  5 ,  
  		    		 6,  7,  8,  9,  8,  9,  10, 11, 
			 		 12, 13, 12, 13, 14, 15, 16, 17,
			 		 16, 17, 18, 19, 20, 21, 20, 21, 
					 22, 23, 24, 25, 24, 25, 26, 27, 
					 28, 29, 28, 29, 30, 31, 32, 1 ]

straight_perm = [16, 7,  20, 21, 29, 12, 28, 17,
				 1,  15, 23, 26, 5,  18, 31, 10,
				 2,	 8,  24, 14, 32, 27, 3,  9 ,
				 19, 13, 30, 6,  22, 11, 4,  25]

compression_perm = [14, 17, 11, 24,	1,  5,  3,  28, 
					15, 6,  21, 10, 23, 19, 12, 4 , 
					26, 8,  16, 7,  27, 20, 13, 2 ,
					41, 52, 31, 37, 47, 55, 30, 40,
					51, 45,	33, 48, 44, 49, 39, 56, 
					34, 53, 46, 42, 50, 36, 29, 32]

sboxes = [[[14, 4,  13, 1,  2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0,  7 ],
		   [0,  15, 7,  4,  14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3,  8 ],
		   [4,  1,  14, 8,  13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5,  0 ],
		   [15, 12, 8,  2,  4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6,  13]],

		  [[15, 1,  8,  14, 6,  11, 3,  4,  9,  7,  2,  13, 12, 0,  5,  10],
		   [3,  13, 4,  7,  15, 2,  8,  14, 12, 0,  1,  10, 6,  9,  11, 5 ],
		   [0,  14, 7,  11, 10, 4,  13, 1,  5,  8,  12, 6,  9,  3,  2,  15],
		   [13, 8,  10, 1,  3,  15, 4,  2,  11, 6,  7,  12, 0,  5,  14, 9 ]],

		  [[10, 0,  9,  14, 6,  3,  15, 5,  1,  13, 12, 7,  11, 4,  2,  8 ],
		   [13, 7,  0,  9,  3,  4,  6,  10, 2,  8,  5,  14, 12, 11, 15, 1 ],
		   [13, 6,  4,  9,  8,  15, 3,  0,  11, 1,  2,  12, 5,  10, 14, 7 ],
		   [1,  10, 13, 0,  6,  9,  8,  7,  4,  15, 14, 3,  11, 5,  2,  12]],

		  [[7,  13, 14, 3,  0,  6,  9,  10, 1,  2,  8,  5,  11, 12, 4,  15],
		   [13, 8,  11, 5,  6,  15, 0,  3,  4,  7,  2,  12, 1,  10, 14, 9 ],
		   [10, 6,  9,  0,  12, 11, 7,  13, 15, 1,  3,  14, 5,  2,  8,  4 ], 
		   [3,  15, 0,  6,  10, 1,  13, 8,  9,  4,  5,  11, 12, 7,  2,  14]],

		  [[2,  12, 4,  1,  7,  10, 11, 6,  8,  5,  3,  15, 13, 0,  14, 9 ],
		   [14, 11, 2,  12, 4,  7,  13, 1,  5,  0,  15, 10, 3,  9,  8,  6 ],
		   [4,  2,  1,  11, 10, 13, 7,  8,  15, 9,  12, 5,  6,  3,  0,  14],
		   [11, 8,  12, 7,  1,  14, 2,  13, 6,  15, 0,  9,  10, 4,  5,  3 ]],

		  [[12, 1,  10, 15, 9,  2,  6,  8,  0,  13, 3,  4,  14, 7,  5,  11],
		   [10, 15, 4,  2,  7,  12, 9,  5,  6,  1,  13, 14, 0,  11, 3,  8 ],
		   [9,  14, 15, 5,  2,  8,  12, 3,  7,  0,  4,  10, 1,  13, 11, 6 ],
		   [4,  3,  2,  12, 9,  5,  15, 10, 11, 14, 1,  7,  6,  0,  8,  13]],

		  [[4,  11, 2,  14, 15, 0,  8,  13, 3,  12, 9,  7,  5,  10, 6,  1 ],
		   [13, 0,  11, 7,  4,  9,  1,  10, 14, 3,  5,  12, 2,  15, 8,  6 ],
		   [1,  4,  11, 13, 12, 3,  7,  14,	10, 15, 6,  8,  0,  5,  9,  2 ],
		   [6,  11, 13, 8,  1,  4,  10, 7,  9,  5,  0,  15, 14, 2,  3,  12]],

		  [[13, 2,  8,  4,  6,  15, 11, 1,  10, 9,  3,  14, 5,  0,  12, 7 ],
		   [1,  15, 13, 8,  10, 3,  7,  4,  12, 5,  6,  11, 0,  14, 9,  2 ],
		   [7,  11, 4,  1,  9,  12, 14,	2,  0,  6,  10, 13, 15, 3,  5,  8 ],
		   [2,  1,  14, 7,  4,  10, 8,  13, 15, 12, 9,  0,  3,  5,  6,  11]]]


def createMessageChunks(message, n):
	word_list = []
	word = ""

	for i in range(len(message)):
		if i % n == 0 and i != 0:
			word_list.append(word)
			word = ""
		word = word + message[i]
	if word != "" and word != " ":
		word_list.append(word)
	return word_list

def BinaryToDecimal(binary):  
         
    binary1 = binary  
    decimal, i, n = 0, 0, 0
    while(binary != 0):  
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)  
        binary = binary//10
        i += 1
    return (decimal)

def bin_to_string(bin_data):
	str_data = ""
	for i in range(0, len(bin_data), 8):
		temp_data = int(bin_data[i:i + 8])
		decimal_data = BinaryToDecimal(temp_data)
		str_data = str_data + chr(decimal_data)
	return str_data

def string_to_bin(string):
	binStr = ""
	for i in string:
		binStr += bin(ord(i))[2:].zfill(8)
	return binStr

def permute(text, table):
	perm = ""
	for i in table:
		perm += text[i-1]
	return perm

def leftshift(key, n):
	for j in range(n):
		newK = ""
		for i in range(1,28):
			newK += key[i]

		newK += key[0]
		key = newK
	return newK

def xor(a, b):
	xor = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			xor = xor + '0'
		else:
			xor = xor + '1'
	return xor


def getKeys(k):
	keys = []
	key = permute(k, key_perm)

	leftKey = key[:28]
	rightKey = key[28:]
	
	for i in range(16):
		if i == 0 or i == 1 or i == 8 or i == 15:
			n = 1
		else:
			n = 2


		leftKey = leftshift(leftKey, n)
		rightKey = leftshift(rightKey, n)

		newKey = leftKey + rightKey
		keys.append(permute(newKey, compression_perm))

	return keys

def f(key, right):
	rightExp = permute(right, expansion_perm)

	rightExp = xor(rightExp, key)

	sboxResult = ""
	for i in range(8):
		chunk = rightExp[i*6:(i+1)*6]

		row = int((chunk[0] + chunk[5]),2)
		col = int(chunk[1:5],2)

		output = sboxes[i][row][col]

		sboxResult = sboxResult + bin(output)[2:].zfill(4)

	sboxResult = permute(sboxResult, straight_perm)
	return sboxResult


# call with message (in binary string form), key(also in binary string form), and bool. flag should be true
# when encrypting and false if decrypting
def des(message, key, encryptFlag):
	# get all subkeys
	keys = getKeys(key)

	# reverse keys if decrypting
	if encryptFlag == False:
		keys.reverse()

	# perform initial permutation
	m = permute(message, initial_perm)
	# split string into left and right halves
	left = m[:32]
	right = m[32:]

	# start 16 rounds of encryption
	for i in range(16):
		temp = right
		fResult = f(keys[i], right)
		right = xor(left, fResult)
		left = temp

	final = right + left
	final = permute(final, final_perm)

	return final

def encrypt(m, k):
	random.seed(k)
	iv = ""
	for i in range(64):
		iv += str(random.randint(0,1))

	m = string_to_bin(m)

	key = bin(k)[2:]
	if len(key) > 64:
		key = bin(mac.sha1(key))
		key = key[len(key)-64:]
	while len(key) < 64:
		key = key + '0'

	i = 0
	ciphertexts = [iv]
	while True:
		chunk = m[i*64:(i+1)*64]
		if chunk == "" or chunk == " ":
			break

		if len(chunk) < 64:
			num = (64 - len(chunk))//8
			numString = bin(num)[2:].zfill(8)
			
			for j in range(num):
				chunk += numString

		cipher = des(xor(chunk, ciphertexts[i]), key, True)
		ciphertexts.append(cipher)

		i += 1

	message = ""
	for i in range(1, len(ciphertexts)):
		message += ciphertexts[i]
	return message

def decrypt(m, k):
	random.seed(k)
	iv = ""
	for i in range(64):
		iv += str(random.randint(0,1))

	key = bin(k)[2:]
	if len(key) > 64:
		key = bin(mac.sha1(key))
		key = key[len(key)-64:]
	while len(key) < 64:
		key = key + '0'

	i = 0
	ciphertexts = [iv]
	plaintexts = []
	while True:
		plaintext = ""
		chunk = m[i*64:(i+1)*64]
		if chunk == "" or chunk == " ":
			break
		ciphertexts.append(chunk)
		plain = xor(des(chunk, key, False), ciphertexts[i])

		if (i+1)*64 >= len(m):
			num = plain[56:64]
			padding = int(num, 2)
			if padding < 8:
				plaintext = plain[:64 - (8*padding)]
			else:
				plaintext = plain

		else:
			plaintext = plain

		plaintexts.append(plaintext)
		i += 1

	message = ""
	for i in range(len(plaintexts)):
		message += plaintexts[i]
	return bin_to_string(message)


def encrypt3(m, k):
	# seed the random generator with the key so that each key 
	# will always generate the same three 64-bit keys
	random.seed(k)

	m = string_to_bin(m)

	keys = []
	for i in range(3):
		tempKey = ""
		for i in range(64):
			tempKey += str(random.randint(0,1))
		keys.append(tempKey)

	iv = ""
	for i in range(64):
		iv += str(random.randint(0,1))

	# create list of ciphertexts starting with initial vector
	i = 0
	ciphertexts = [iv]
	while True:
		chunk = m[i*64:(i+1)*64]
		if chunk == "":
			break

		# do PKCS#5 padding if less than 64 bit message chunk
		if len(chunk) < 64:
			num = (64 - len(chunk))//8
			numString = bin(num)[2:].zfill(8)
			
			for j in range(num):
				chunk += numString

		# xor with previous cipher or IV before encryption
		chunk = xor(chunk, ciphertexts[i])
			
		# encrypt decrypt encrypt
		step1 = des(chunk, keys[0], True)
		step2 = des(step1, keys[1], False)
		step3 = des(step2, keys[2], True)

		ciphertexts.append(step3)

		i += 1

	message = ""
	for i in range(1, len(ciphertexts)):
		message += ciphertexts[i]

	return message

def decrypt3(m, k):
	random.seed(k)

	keys = []
	for i in range(3):
		tempKey = ""
		for i in range(64):
			tempKey += str(random.randint(0,1))
		keys.append(tempKey)

	iv = ""
	for i in range(64):
		iv += str(random.randint(0,1)) 

	i = 0
	ciphertexts = [iv]
	plaintexts = []
	while True:
		plaintext = ""
		chunk = m[i*64:(i+1)*64]
		if chunk == "" or chunk == " ":
			break
		ciphertexts.append(chunk)

		step1 = des(chunk, keys[2], False)
		step2 = des(step1, keys[1], True)
		step3 = des(step2, keys[0], False)

		step3 = xor(step3, ciphertexts[i])

		if (i+1)*64 >= len(m):
			num = step3[56:64]
			padding = int(num, 2)
			if padding < 8:
				plaintext = step3[:64 - (8*padding)]
			else:
				plaintext = step3

		else:
			plaintext = step3

		plaintexts.append(plaintext)
		i += 1

	message = ""
	for i in range(len(plaintexts)):
		message += plaintexts[i]
	return bin_to_string(message)


if __name__ == "__main__":

	message = "1001011001101001010100010100101001101001101010101000000101101011"

	key     = "1001001010111011110110100010110100110101011011101001001010010000101100101101101010111010"
	

	message = "cryptozz"
	ciphertext = encrypt3(message, key)
	print("CIPHER:", ciphertext)
	plaintext = decrypt3(ciphertext, key)
	print("PLAIN: ", plaintext)
	print("ORIGIN:", message)
	
	print("----------------------------------------------\n\n")

	message = "mac 1100101"
	#print(string_to_bin(message))
	#print(bin_to_string(string_to_bin(message)))


	print("PLAIN: ", string_to_bin(message))
	ciphertext = encrypt(message, int(key,2))
	print("CIPHER:", ciphertext)
	plaintext = decrypt(ciphertext, int(key,2))
	print("PLAIN: ", plaintext)

	print("----------------------------------------------\n\n")

	ciphertext = encrypt3(message, int(key,2))
	print("CIPHER:", ciphertext)
	plaintext = decrypt3(ciphertext, int(key,2))
	print("PLAIN: ", plaintext)
	print("ORIGIN:", message)

	print("----------------------------------------------\n\n")

	ciphertext = encrypt(message, int(key,2))
	print("CIPHER:", ciphertext)
	plaintext = decrypt(ciphertext, int(key,2))
	print("PLAIN: ", plaintext)
	print("ORIGIN:", message)