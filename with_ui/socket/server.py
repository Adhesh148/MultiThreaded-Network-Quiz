import socket
import threading
import time
import sys
import numpy as np
from getQuestions import *

# Define const. parameters
MAX_LEN = 64
PORT = 9002
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "Game Over"
WAIT_TIME = 30
NUM_PLAYERS = 1

# Global variables
client_list = []
client_names = []
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

	# receive the username of client
	username = conn.recv(1024).decode(FORMAT)
	indx = client_list.index(conn)
	client_names[indx] = username
	print("Name of client: ",username)
	
	connected = True
	while connected:
		# receive response from the client
		response = conn.recv(1024).decode(FORMAT)
		print(response)
		conn_indx = client_list.index(conn)
		time_duration = conn.recv(1024).decode(FORMAT)
		print(time_duration)
		time_duration_float = float(time_duration)
		print(time_duration_float)
		time_taken[conn_indx] =  time_taken[conn_indx] + time_duration_float

		# Update score
		if(response == solutions[0]):
			client_score[conn_indx] = client_score[conn_indx] + 1

		locked_client.append(conn)

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

	time.sleep(1)

	# calculate rank
	rank = [0]*NUM_PLAYERS
	# based on the key - lowest key value gets highest rank
	indices = [i for i in range(NUM_PLAYERS)]
	c = list(zip(client_score,time_taken,indices))
	c = sorted(c)
	for pos in range(len(c)):
		rank[c[pos][2]] = pos + 1
	print(rank)

	# Now broadcast the number of players
	broadcast(str(NUM_PLAYERS))
	time.sleep(1)

	for client in client_list:
		for player in client_list:
			indx = client_list.index(player)
			rank_msg = "Player "+ str(indx) + "-" + client_names[indx] 
			if(indx == client_list.index(client)):
				rank_msg = rank_msg + " [YOU]"
			rank_msg = rank_msg + "-" + str(rank[indx]) + "-" + str(client_score[indx]) + "-" + str(time_taken[indx])
			print(rank_msg)
			client.send(rank_msg.encode(FORMAT))
			time.sleep(0.1)
		time.sleep(0.3)
		final_msg = "Sorry. You came in " + str(rank[client_list.index(client)]) + ". Better Luck next time."
		if(rank[client_list.index(client)] == 1):
			final_msg = "Congrats! You have won the quiz."
		client.send(final_msg.encode(FORMAT))

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
		client_names.append("player")
		thread = threading.Thread(target=handle_client,args=(conn,addr))
		thread.start()
		if(len(client_list) == NUM_PLAYERS):						# Once we get [NUM_PLAYERS] connection - start the quiz
			time.sleep(2)
			start_quiz()

	conn.close()
	server.close()

start()