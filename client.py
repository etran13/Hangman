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
    "Prompt the user for input"
    while True:
        letter = input("")
        return letter

if __name__ == "__main__":
    """Make the connection to the server
    using the argument passed in"""
    #hostIP = '10.56.2.249' #The host IP of server VM, hardcoded for now
    try:
        hostIP = sys.argv[1]
    except IndexError:
        print("Missing IP address")
        os._exit(1)
    
    try:
        portNum = int(sys.argv[2]) 
    except IndexError:
        print("Missing port number")
        os._exit(1)
    except ValueError:
        print("Invalid port number")
        os._exit(1)
    
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((hostIP, portNum)) 

    "Print data received from server, get user input,"
    "send to server loop"
    while True:
        data = conn.recv(1024)

        #Check if the server sends an empty packet- shut down if so
        if not data:
            break

        print(data.decode(), end="")
        messageToSend = getSingleLetterFromPlayer() 
        conn.sendall(messageToSend.encode()) 

    #End of program
    conn.close()
        