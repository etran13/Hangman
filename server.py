import sys
import socket
from threading import *
import os

from hangman import *

class GameThread(Thread):
    def __init__(self, socketConnection):
        super().__init__()
        self.game = Hangman(socketConnection)

    def run(self):
         """Runs the hangman game"""
         self.game.playGame()


if __name__ == "__main__":
    #Set host IP and port number to listen on
    hostIP = '10.56.2.249' #The host IP of server VM
    portNum = 8080

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
                newGame = GameThread(conn)
                newGame.start() 
