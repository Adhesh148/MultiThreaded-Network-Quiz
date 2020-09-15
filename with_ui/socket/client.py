import socket
import sys
import select

sys.path.append("/home/adheshreghu/Documents/SEM5/Networking/Lab/Week5/with_ui/ui/") 
from question import *

HEADER = 64
PORT = 9005
SERVER = "127.0.1.1"
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "Game Over"


def closeConn(client):
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
    MainWindow.show()
    sys.exit(app.exec_())

def recvMessageF(client,ui,MainWindow):
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
    
    # set the UI according to the new question receieved.
    ui.setupUi_1(MainWindow,question,options,client,ui)
   

def main(client):
    # Start listening for questions
    recvMessage(client)


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    # receive the welcome and rules message
    wlcm_msg = client.recv(4096).decode(FORMAT)
    print(wlcm_msg)
    main(client)

