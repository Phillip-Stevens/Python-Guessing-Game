# List of Imports
import socket;
import sys;

# Messages
greetings = 'Hello/r/n';

# Setup Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.connect(('127.0.0.1', 4001));

# Send the greetins to the server 
sock.send(greetings.encode());

# Receive the message and display it
msg = sock.recv(80).decode();
print(str(msg));

# Listen to the messages sent and print the string. If no more messages are received
# exit the client.
while True:
    msg = sock.recv(80).decode();
    print(str(msg)+ '\n');

    if(str(msg) == ""):
        break;

input("Press Any Key to Close");
sock.close();
    
