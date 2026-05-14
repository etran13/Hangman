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
        letter = input("Input your guess: ")
        return letter

if __name__ == "__main__":
    """Make the connection to the server
    using the argument passed in"""
    hostIP = '10.56.2.249' #The host IP of server VM, hardcoded for now
    portNum = int(sys.argv[1]) 
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((hostIP, portNum)) 

    "Get input, send, print response loop"
    while True:
        messageToSend = getSingleLetterFromPlayer() 
        socket.sendall(messageToSend.encode()) 
        data = socket.recv(1024)
        print(data.decode())
        