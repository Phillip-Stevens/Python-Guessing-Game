# Import the files we need to use
import socket;
import re;
import sys;

# Variables and Messages
running = True;
Hello = 'Hello';
guess = 0;
valid = False;

# Connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.connect(('127.0.0.1', 4000));

while(running == True):

    # Set the message received to what was recovered
    message = sock.recv(80).decode();

    if(message == "Greetings\r\n"):
        print("Welcome to Guess the Number game! (Range: 1-20)\n");
        valid = False;
    elif(message == "Correct\r\n"):
        print("You guessed correctly!");
        #input();
        running = False;
        valid = True;
    elif(message == "Close\r\n"):
        print("You are close!");
        valid = False;
    elif(message == "Far\r\n"):
        print("You are way off!");
        valid = False;
    else:
        print("Another message!");
    if(valid == False):

        try:
            # Guess the number
            guess = input("What is your guess: ");
            validGuess = re.findall(r'\d{1,2}', guess);
            guess = int(validGuess[0]);

            # If the user guess is valid but over 20 we need to raise a Value Error Exception
            if(guess > 20 or guess < 0):
                raise ValueError;
            else:
                valid = True;

        # Throw this exception when the value doesn't meet the requirements
        except ValueError:
            print("\nYou entered a number not within the range or another invalid input!");
            continue;
    
    # Once we have confirmed that its a valid guess send it to the server
    sock.send(str(guess).encode());

# Close the socket
sock.close();
sys.exit();
