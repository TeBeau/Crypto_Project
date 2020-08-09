class Bank:
	
	# Initialize bank object- can provide optional argument to alter balance
	def __init__(self, name):
		self.name = name
		self.d = dict()
		file = open("private_bank_info.txt", "r")
		for line in file:
			user = line[0:line.index(" ")]
			bal = float(line[line.index(" ")+1:])
			self.d[user] = bal
		file.close()
		self.balance = self.d[self.name]

	# Deposit money- return new balance
	def deposit(self, amount):
		self.balance = self.balance + amount
		self.d[self.name] = self.balance
		file = open("private_bank_info.txt", "w")
		for user in self.d:
			string = user + " " + str( self.d[user] ) + "\n"
			file.write(string)
		file.close()
		return self.balance

	# withdraw some money- return new balance
	def withdraw(self, amount):
		if self.balance-amount < 0:
			print("ERROR: Overdraw")
			return -1
		self.balance = self.balance - amount
		self.d[self.name] = self.balance
		file = open("private_bank_info.txt", "w")
		for user in self.d:
			string = user + " " + str( self.d[user] ) + "\n"
			file.write(string)
		file.close()
		return self.balance

	# return current balance
	def queryBalance(self):
		return self.balance

	