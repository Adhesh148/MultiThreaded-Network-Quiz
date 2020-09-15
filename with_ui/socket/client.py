import socket
import sys
import select

sys.path.append("/home/adheshreghu/Documents/SEM5/Networking/Lab/Week5/with_ui/ui/") 
from question import *
from home import *

HEADER = 64
PORT = 9004
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
   

if __name__ == "__main__":

    # create home application
    # home_app  = QtWidgets.QApplication(sys.argv)
    # home_MainWindow = QtWidgets.QMainWindow()
    # home_ui = Ui_MainWindow()
    # home_ui.setupUi(home_MainWindow,ADDR)
    # home_MainWindow.show()
    # sys.exit(home_app.exec_())

    clientS = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientS.connect(ADDR)
    # receive the welcome and rules message
    wlcm_msg = clientS.recv(4096).decode(FORMAT)
    print(wlcm_msg)
    # close this application
    recvMessage(clientS)

