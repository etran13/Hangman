import sys
import socket
from threading import *
import os

from hangman import *

"""FILE HANDLING- Generate list from file passed in"""

def loadWordsFromFile(filename):
    "Reads the configuration file and returns a list of all its contents"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            file.close()
            return lines
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

class GameThread(Thread):
    def __init__(self, socketConnection, listOfWords):
        super().__init__()
        self.conn = socketConnection
        self.game = Hangman(socketConnection, listOfWords)

    def run(self):
        """Runs the hangman game, catches premature disconnects"""
        try:
            self.game.playGame()
        except BrokenPipeError:
            print("Player has disconnected")
        self.conn.close()
        sys.exit()

if __name__ == "__main__":
    #Set the filename/path
    try:
        filename = sys.argv[1]
    except:
        print("Invalid or missing file name")
        os._exit(0)

    #Set host IP and port number to listen on
    hostIP = '10.56.2.249' #The host IP of server VM

    try:
        portNum = int(sys.argv[2])
    except:
         print("Invalid or missing port number")
         os._exit(0)

    #Create the list
    listOfWords = loadWordsFromFile(filename)

    #Create a socket to listen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initialServer:
            initialServer.bind((hostIP, portNum))
            initialServer.listen() 
            print(f"Server listening on address {hostIP}, port {portNum}")

            '''Main loop- Repeatedly accept connections and 
            create GameThreads for game instances'''
            while True:
                conn, addr = initialServer.accept() #Blocks until accept

                #Create and start a game for the client
                newGame = GameThread(conn, listOfWords)
                newGame.start() 
