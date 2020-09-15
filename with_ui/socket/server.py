import socket
import threading
import time
import sys
from getQuestions import *

# Define const. parameters
MAX_LEN = 64
PORT = 9005
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.1.1"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "Game Over"
WAIT_TIME = 30
NUM_PLAYERS = 2

# Global variables
client_list = []
time_taken = []
client_score = []
locked_client = []
thread_lock = threading.Lock()

# Create server socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

# Define the question set to be used
questions = []
solutions = []

# Function to handle client responses concurrently
def handle_client(conn,addr):
	print(f"[NEW CONNECTION] {addr} connected.")
	# Welcome Message
	msg = "Welcome to the Quiz. Waiting for other players..."
	msg = msg.encode(FORMAT)
	conn.send(msg)
	
	connected = True
	while connected:
		# receive response from the client
		response = conn.recv(1024).decode(FORMAT)
		conn_indx = client_list.index(conn)
		time_duration = conn.recv(1024).decode(FORMAT)
		print(time_duration)
		time_duration_float = float(time_duration)
		print(time_duration_float)
		time_taken[conn_indx] =  time_taken[conn_indx] + time_duration_float

		# Update score
		print(response)
		if(response == solutions[0]):
			client_score[conn_indx] = client_score[conn_indx] + 1

		# thread_lock.acquire()
		locked_client.append(conn)
		# print(len(locked_client))
		# thread_lock.release()

		# Wait for the minute to get over
		while(len(locked_client)%NUM_PLAYERS !=0):
			pass

		thread_lock.acquire()
		if(locked_client[-1] == conn):
			print("pop")
			questions.pop(0)
			solutions.pop(0)

			# Pop already asked question and ask another question	
			if len(questions) == 0:
				end_quiz()
				break
			else:
				start_quiz()
		thread_lock.release()
	server.close()

def start_quiz():
	if(len(questions)!=0):
		for connection in client_list:
			connection.send(questions[0].encode(FORMAT))

def end_quiz():
	broadcast("Game Over")
	print(time_taken)
	print(client_score)
	# Close all connections
	for clients in client_list:
		clients.close()
	sys.exit()

def broadcast(message):
    for clients in client_list:
    	clients.send(message.encode(FORMAT))


# server start listening
def start():

	# Let us update the questions and solutions
	getQuestions(questions,solutions)

	server.listen()
	print(f"[LISTENING Server is listening on {SERVER}]")
	while True:
		conn,addr = server.accept()			
		client_list.append(conn)
		time_taken.append(0)
		client_score.append(0)
		thread = threading.Thread(target=handle_client,args=(conn,addr))
		thread.start()
		if(len(client_list) == NUM_PLAYERS):						# Once we get [NUM_PLAYERS] connection - start the quiz
			start_quiz()

	conn.close()
	server.close()

start()