import encryptions as enc

#helper function to split message into chunks of n size
def createMessageChunks(message, n):
	word_list = []
	word = ""

	i = 0
	while (True):
		if i % n == 0 and i != 0:
			word_list.append(word)
			word = ""
			if i == len(message):
				break
		word = word + message[i]
		i += 1

	return word_list

# helper function to left rotate the string by n bits
# necessary for the sha1 algorithm
def leftRotate(message, n):
	return ((message << n) | (message >> (32 - n)))

# helper function to do the sha1 hash
def sha1(message):
	# hard coded values
	h0 = int("0x67452301", 16)
	h1 = int("0xEFCDAB89", 16)
	h2 = int("0x98BADCFE", 16)
	h3 = int("0x10325476", 16)
	h4 = int("0xC3D2E1F0", 16)

	m1 = len(message)
	message = message + '1'

	# append bit '0' to the message until its length modulo 448 = 0 and then 
	while (len(message) + len(bin(m1)[2:])) % 512 != 0:
		message = message + '0'
	# append the length of the message in binary form
	message = message + bin(m1)[2:]

	# break the message into 512 bit chunks
	messageChunks = createMessageChunks(message, 512)
	for chunk in messageChunks:
		# break each chunk into 16 32 bit words
		w = createMessageChunks(chunk, 32)
		# convert chunks from bin strings to ints
		for i in range(16):
			w[i] = int(w[i], 2)

		# create 80 words using this formula
		for i in range(16,80):
			w.append(leftRotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))

		a = h0
		b = h1
		c = h2
		d = h3
		e = h4

		# following sha1 algorithm for this part
		for i in range(80):
			if i >= 0 and i < 20:
				f = (b & c) | ((~b)&d)
				k = int("0x5A827999", 16)
			elif i >= 20 and i < 40:
				f = b ^ c ^ d
				k = int("0x6ED9EBA1", 16)
			elif i >= 40 and i < 60:
				f = (b & c) | (b & d) | (c & d)
				k = int("0x8F1BBCDC", 16)
			else:
				f = b ^ c ^ d
				k = int("0xCA62C1D6", 16)

			temp = leftRotate(a, 5) + f + e + k + w[i] & 0xffffffff
			e = d
			d = c
			c = leftRotate(b, 30)
			b = a
			a = temp

		h0 = h0 + a
		h1 = h1 + b
		h2 = h2 + c
		h3 = h3 + d
		h4 = h4 + e

	hh = (h0 << 128) | (h1 << 96) | (h2 < 64) | (h3 < 32) | h4
	return hh

# main function to receive an HMAC, call with a key and the message to authenticate
# should only be calling this function from any other classes, all the others in this class are helper functions
def mac(message, keyInt):
	message = ""
	for i in enc.convert_string_to_binary(message):
		message = message + i
	print(message)
	# convert key to binary and message to binary
	k = bin(keyInt)[2:]

	# if key is longer than block size(64) then hash it
	if len(k) > 64:
		sha1(k)

	# pad key with 0's on the right if shorter than key size
	while len(k) < 64:
		k = k + '0'

	# hard code outer and inner pad values
	# 8 repeated bytes of 0x5c
	oPad = '0101110001011100010111000101110001011100010111000101110001011100'
	# 8 repeated bytes of 0x3c
	iPad = '0011011000110110001101100011011000110110001101100011011000110110'

	# xor key with corresponding pad  (both in int form) and convert back to binary string
	oPadKey = int(k, 2) ^ int(oPad, 2)
	oPadKey = bin(oPadKey)[2:]

	iPadKey = int(k, 2) ^ int(iPad, 2)
	iPadKey = bin(iPadKey)[2:]

	#print(iPadKey)
	#print(message)

	# The HMAC is the hash of the outer key concatenated with 
	# the hash of the inner key concatenated with the message
	innerConcatenate = bin(sha1(iPadKey + message))[2:]
	return bin(sha1(oPadKey + innerConcatenate))[2:]

if __name__ == "__main__":
	# dont run this file, only use the hmac function
	# this main function is just for debugging

	x = "11001010"
	print(createMessageChunks(x, 4))

	print(leftRotate(int(x,2), 4))

	#ans = sha1('01110100011001010111001101110100')
	#print(bin(ans)[2:])

	#print(bin(mac(0, "0"))[2:])

	ans = hex(mac("0", 0))[2:]
	print(ans)
	print(len(ans))