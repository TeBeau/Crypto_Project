#Client Portal
#expand based on functions and comunictaion dicussed 8/2/20
def dec2bin(n):
    #converts a decimal number to binary
    s=''
    while n!=0:
        s= str(n%2)+s
        n= n//2
    l= 8-len(s)
    while l>0:
        s= '0'+s
        l=8-len(s)
    return s
N= 101 #or random large prime
a= int(input("Enter Personal Key:"))

#Bank(amount, N) create bank file for client to work with
#key= negotiate(a, N)
#x= bank.authenticate(DES(3, key))
#bank recives a message for authentication
#bank authenticates itself by returning an encrypted 6 (2x3)
#if x!= 6: "error: line insecure"
#negotiate key
action= ''
amount= "00000000"
while action!= 'finished':
    action= input("Enter an action:")
    if action == "finished": break
    if action== 'deposit' or 'withdraw':
        amount= int(input("Enter amount of your transaction:"))
        amount= dec2bin(amount)
        message= action+amount
    else: message= action+ "00000000"
    #message= DES(message, key)+MAC(message, key)
    #encrypt messsage and add mac
    #x= Bank.action(message)
    #send this to bank server however this is defined later
