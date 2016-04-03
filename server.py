import socket;
import random;
import sys;
import threading;
import select;

# Function to check if the users guess is within the range of the number
def within(value, goal, n):

    # Check if the value - goal is less than n
    if(abs(value - goal) <= n):
        return True;
    else:
        return False;

# Define the messages now!
Greetings = "Greetings\r\n";
Correct = "Correct\r\n";
Close = "Close\r\n";
Far = "Far\r\n";
AdminGreetings = "Greetings-Admin\r\n";

# Create a list to be updated with the users 
userList = [];
socks = [];

# A method to handle the Admin
def admin_handler(conn, addr):
    conn.recv(80).decode();

    conn.send(AdminGreetings.encode());

    # For each loop over each connection within the user list and then send it to the admin to post to their console window.
    for connection in userList:
        msg = str(connection);
        conn.send(msg.encode());
        
    conn.close();

# A method to handle each client on their thread
def client_handler(conn, addr):

    # Variables get defined here to ensure unique random number per user
    guess = 0;
    randomNum = random.randrange(1, 20);
    gameOver = False;
    score = 0;

    # Add the address to the userList.
    userList.append(str(addr));

    # Send the initial message to the user
    conn.send(str(Greetings).encode());
    
    # Game Logic
    while(gameOver == False):
        
        # Retreive the guess, cast it as an in
        message = conn.recv(80).decode();
        guess = int(message);
        score += 1;

        # Check the result!
        if(abs(randomNum - guess) != 0):
            # Check the result!
            result = within(guess, randomNum, 1);

            # Close to the target!
            if(result == True):
                conn.send(Close.encode());
            else:
                conn.send(Far.encode());
        else:
            # The user guessed correctly!
            conn.send(Correct.encode());

            # Open the file and save the score
            file = open('scores.txt', 'a');
            file.write(str(score));
            file.write("\n");
            file.close();

            # end the game loop
            gameOver = True;
            conn.close();

            return;

# Client Setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.bind(('127.0.0.1', 4000));

# Admin Socket
admin_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
admin_sock.bind(('127.0.0.1', 4001));

sock.listen(5);
admin_sock.listen(5);

# Append socket list so that the list contains both the client and the admin.
socks.append(sock);
socks.append(admin_sock);

while True:

    # Accept and confirm the connection has made it through
    (conection_input, connection_output, err) = select.select(socks, [], []);

    # For each over the list, check the connection input and see if it matches
    for conn_inp in conection_input:

        # Client
        if(conn_inp == sock):
            (conn, addr) = sock.accept();
            cthread = threading.Thread(target = client_handler, args = (conn, addr));
            cthread.start();

        # Admin
        elif(conn_inp == admin_sock):
            (conn, addr) = admin_sock.accept();
            athread = threading.Thread(target = admin_handler, args = (conn, addr));
            athread.start();
        else:
            continue;
            

    
