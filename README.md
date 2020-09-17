# MultiThreaded-Network-Quiz
-------------------------------
-------------------------------
#### Objective
To develop an online quiz for the users to take part in.

#### Tech Stack
* Python 3
* PyQt 5

#### Assumptions
* The client can connect to the server IP.
* The client has the server address.
* The server has a parameter   NUM_PLAYERS  restricting the number of players.
* The quiz will begin only when all players have joined.
* The folder structure of the project remains unchanged.
* The client tries to connect only when the server is up.
* There are no connection problems between the server and client in the duration of the quiz.

#### Execution Instructions
* Set the  ``` NUM_PLAYERS```.
* Pass the server IP address to the client.
* Start the server.
* Enter the quiz using the client file with updated server details.
* After the quiz ends exit the server.

#### Rules and Regulations
* Each participant will be given questions and options. 
* The participant has to select one of the four options.
* There is a time limit for each question.
* Each question is equally weighted.
* If none of the questions is marked at the end of the timer, a default wrong response gets recorded.
* If the user had selected an option but failed to submit the option by the end of the quiz, the selected option gets recorded.
* The scores of the participants are given at the end of the quiz.
* The tie-breaker in case of equal scores will be the time taken to choose the option.

#### User Interface
We have also added a user interface for the quiz, so instead of using the terminal, the participants in the quiz can select one radio button from a set of 4. We also have a submit button and a timer as part of the UI.
At the start of each question for a participant, the timer is set at 10 seconds (can be modified according to the constant parameter ```WAIT_TIME```), and if the participant fails to select and submit any of the options in that time, the question will be marked wrong and the next question will be loaded.
In case a button is selected but the submit button is not pressed within ```WAIT_TIME``` seconds, the selected button will be taken as the answer given by the participant.

> **_NOTE:_**  UI is done using PyQt5. The source can be found in ui/question.py.

#### Question  Bank
We also maintain a *questionBank.txt* file where all the questions to be asked are stored. The *getQuestions.py* contains a function which reads the file and updates the list of questions and solutions to be used by the server. The server upon starting calls this function to update the question and solution list.
The *questionBank.txt* is a self-explanatory file and any number of questions can be added to it.

#### Code Parameters
* ``WAIT_TIME`` : Specifies the amt of time for each question. Has to be changed in client.py.
* ``NUM_PLAYERS`` : Specifies the number of client connections required for the quiz. Given in server.py.
* ``SERVER`` : Sepcifies server address. Present in both client and server. Should be updated properly.
* ``PORT`` : Sepcifies port address. Present in both client and server. Should be updated properly.
* ``FORMAT`` : Specifies format of the packet that is sent or received over the network
* ``DISCONNECT_MSG`` : Specifies the message which when received causes the client to close. Indicates Game Over state.

#### Code
 - Server Side Code - [socket/server.py](socket/server.py)
 - Client Side Code - [socket/client.py](socket/client.py)
 - UI used - [ui/question.py](ui/question.py)
 - Helper Function to fetch questions - [socket/getQuestions.py](socket/getQuestions.py)