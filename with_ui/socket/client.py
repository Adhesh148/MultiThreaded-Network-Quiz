import socket
import sys
import select

sys.path.append("../ui/") 
from question import *
from home import *

HEADER = 64
PORT = 11076
SERVER = "2.tcp.ngrok.io"
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "Game Over"


def closeConn(client):
    # Now let us print the leaderboard before closing connection
    print("**********************************LEADERBOARD******************************")
    print("---------------------------------------------------------------------------")
    number_players = client.recv(4096).decode(FORMAT)
    number_players = int(number_players)
    print("%-10s %-15s %-10s %-10s %-10s" %("Player No","Name","Rank","Points","Total Time"))
    for i in range(number_players):
        rank_msg = client.recv(4096).decode(FORMAT).split("-")
        print("%-10s %-15s %-10s %-10s %-10s" %(rank_msg[0],rank_msg[1],rank_msg[2],rank_msg[3],rank_msg[4]))

    final_msg = client.recv(4096).decode(FORMAT)
    print("---------------------------------------------------------------------------")
    print(final_msg)
    print("---------------------------------------------------------------------------")
    client.close()
    sys.exit()

def recvMessage(client):
    # Receive the question from the 
    q_msg = client.recv(4096).decode(FORMAT)
    print(q_msg)

    # If the received message is "Game Over" then exit
    if(q_msg == DISCONNECT_MSG):
        closeConn(client)

    # Extract question and options from the message.
    q_msg = q_msg.split("\n")
    question = q_msg[0]
    options = q_msg[1:]

    # Create the Application
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow1()
    
    # set the UI according to the new question receieved.
    ui.setupUi_1(MainWindow,question,options,client,ui)
    MainWindow.setWindowTitle("Quiz")
    MainWindow.show()
    sys.exit(app.exec_())

def recvMessageF(client,ui,MainWindow):
    # Receive the question from the 
    q_msg = client.recv(4096).decode(FORMAT)
    print(q_msg)

    # If the received message is "Game Over" then exit
    if(q_msg == DISCONNECT_MSG):
        MainWindow.close()
        closeConn(client)

    # Extract question and options from the message.
    q_msg = q_msg.split("\n")
    question = q_msg[0]
    options = q_msg[1:]
    
    # set the UI according to the new question receieved.
    ui.setupUi_1(MainWindow,question,options,client,ui)
    ui.updateQuestionIndex()
   

if __name__ == "__main__":

    # get username input
    print("Enter a username.")
    username = input().strip()
    
    clientS = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientS.connect(ADDR)
    # receive the welcome and rules message
    wlcm_msg = clientS.recv(4096).decode(FORMAT)
    print(wlcm_msg)

    # send the username to the server for the leaderboard
    clientS.send(username.encode(FORMAT))

    # close this application
    recvMessage(clientS)

