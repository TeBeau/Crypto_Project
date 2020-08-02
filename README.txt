
Run server.py
then run client.py

Hand Shake / Key Exchange:
- Use Diffie-Hellman protocol to accomplish this

After, server sends over public key n
- client encrypts using Blum-Goldwasser
- client also makes the MAC  				<------- Need to change to the better MAC in github
- client sends message ('encryption', x_n) MAC = mac_encrypy

Server recieves the message
- Decrypts the message
- Verify that the MACs match

