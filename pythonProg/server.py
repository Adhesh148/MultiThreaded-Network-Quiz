import socket
import threading
import time

# Define const. parameters
MAX_LEN = 64
PORT = 9000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "Game Over"
WAIT_TIME = 30
NUM_PLAYERS = 2

# Global variables
client_list = []
time_taken = []
client_score = []
lock = 0
locked_client = []
thread_lock = threading.Lock()
init_time = 0

# Create server socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

# Define the question set to be used
questions = [	"What is the name of our planet ?\na.Earth\nb.Jupiter\nc.Mars\nd.Pluto",
				"What is the name of our Solar System ?\na.Earth\nb.Jupiter\nc.Mars\nd.Milky Way"]
solutions = ['a','d']

# Function to handle client responses concurrently
def handle_client(conn,addr):
	print(f"[NEW CONNECTION] {addr} connected.")
	msg = "Welcome to the Quiz. Waiting for other players..."
	msg = msg.encode(FORMAT)
	conn.send(msg)

	connected = True
	while connected:
		# receive response from the client
		start_time = time.time()
		response = conn.recv(1024).decode(FORMAT)
		end_time = time.time()
		conn_indx = client_list.index(conn)
		time_taken[conn_indx] =  time_taken[conn_indx] + (end_time - init_time)

		# Update score
		print(response)
		if(response == solutions[0]):
			client_score[conn_indx] = client_score[conn_indx] + 1

		locked_client.append(conn)
		print(len(locked_client))

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
				# conn.send(DISCONNECT_MSG.encode(FORMAT))
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
	init_time = time.time()

def end_quiz():
	broadcast("Game Over")
	print(time_taken)
	print(client_score)
	server.close()
	

def broadcast(message):
    for clients in client_list:
    	clients.send(message.encode(FORMAT))


# server start listening
def start():

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