import sys
import socket
import os

import re

def shutdown():
    "This function prints a message to close the socket connection and terminate the program."
    print("Shutting down!")
    conn.close()
    os._exit(0)

def getSingleLetterFromPlayer():
    while True:
        if re.fullmatch("[a-zA-Z]", letter) == None: #Use regex to verify that guess is a single letter
            print("Guess must be a single letter.")
            continue
        elif letter in self.alreadyAsked:
            print("You have already guessed this letter.")
            continue
        else:
            break

if __name__ == "__main__":
    """Make the connection to the server
    using the argument passed in"""
    hostIP = '10.56.2.249' #The host IP of server VM, hardcoded for now
    portNum = int(sys.argv[1]) 
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((hostIP, portNum)) 

    while True:
        #print("Sending loop entered")
        messageToSend = getSingleLetterFromPlayer() 
        socket.sendall(messageToSend.encode()) #Send the message using the socket connection that was passed in