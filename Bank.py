class Bank:

	# Initialize bank object- can provide optional argument to alter balance
	def __init__(self, balance=500.00):
		self.balance = balance

	# Deposit money- return new balance
	def deposit(self, amount):
		self.balance = self.balance + amount
		return self.balance

	# withdraw some money- return new balance
	def withdraw(self, amount):
		if self.balance-amount < 0:
			print("ERROR: Overdraw")
			return -1
			
		self.balance = self.balance - amount
		return self.balance

	# return current balance
	def queryBalance(self):
		return self.balance