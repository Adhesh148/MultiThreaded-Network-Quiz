import socket
import sys
import select

HEADER = 64
PORT = 9000
SERVER = "127.0.1.1"
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

# receive the welcome and rules message
wlcm_msg = client.recv(4096).decode(FORMAT)
print(wlcm_msg)

while True:
	# Receive the question from the 
	q_msg = client.recv(4096).decode(FORMAT)
	print(q_msg)

	# If the received message is "Game Over" then exit
	if(q_msg == "Game Over"):
		break

	# If a valid question, wait for response from user - wait for WAIT_TIME
	response = input().strip()
	client.send(response.encode(FORMAT))

client.close()
sys.exit()
