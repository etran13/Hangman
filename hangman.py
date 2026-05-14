import random
import re

class Hangman:
    def __init__(self, socketConnection):
        self.socketConnection = socketConnection #Responsible for sending across socket

        self.wordList = loadWordsFromFile("words.txt") #A list of words to pick from
        self.state = "" #A list that tracks the player's correct/incorrect guesses, ex. "f__t"
        
        self.lives = 10 #An int that represents the number of remaining attempts
        self.unguessedLettersRemaining = 0 #An int that represents the number of unguessed letters

        self.wordToGuess = ""
        self.alreadyAsked = []

    def playGame(self):
        "Begin the main game loop for a single game. Can be called again to start another game"
        #self.wordToGuess =  #Pick a random word
        playAgain = True
        while playAgain:
            self.setState()

            #Play 1 game
            while True:
                self.sendStateToPlayer()
                userGuess = self.receiveGuess()
                self.updateStateAccordingToGuess(userGuess)
                if self.unguessedLettersRemaining == 0:
                    self.sendStringToClient(f"Congratulations! The correct word "
                        f"was indeed {self.wordToGuess}. "
                            f"Enter y to play again, n to quit: ")
                    break
                elif self.lives == 0:
                    self.sendStringToClient("Sorry, you have used up all 10 of your lives. " 
                        f"The correct word was {self.wordToGuess}. "
                            "Enter y to play again, n to quit: ")
                    break

            #Update playAgain after 1 game
            playAgain = self.receivePlayAgainSignal()



    """HELPER FUNCTIONS to handle all send and recv from socket"""

    def sendStringToClient(self, messageToSend):
        try:
            self.socketConnection.sendall(messageToSend.encode())
            print(f"Sent: {messageToSend}")
            return 0
        except BrokenPipeError:
            return 1

    def recvFromClient(self):
        data = self.socketConnection.recv(1024)
        return data.decode()
    
    

    """Helpers to deal with player input that comes in"""
    
    def sendStateToPlayer(self):
        "Displays the state on the player's end along with a reminder of how many lives are left"
        self.sendStringToClient(''.join(self.state) + "\n" + f"You have {self.lives} lives left. \nInput your guess: ")

    def receiveGuess(self):
        while True:
            letter = self.recvFromClient()
            if re.fullmatch("[a-zA-Z]", letter) == None: #Use regex to verify that guess is a single letter
                self.sendStringToClient("Guess must be a single letter.\nInput your guess: ")
                continue
            elif letter in self.alreadyAsked:
                self.sendStringToClient("You have already guessed this letter.\nInput your guess: ")
                continue
            else:
                break
        return letter

    
    def receivePlayAgainSignal(self):
        """Returns true if user enters yes, false otherwise"""
        signal = self.recvFromClient()
        if re.fullmatch("yes|Yes|y|Y", signal):
            return True
        else:
            return False
    
    def updateStateAccordingToGuess(self, userGuess):
        "Replaces the blank spaces if the user's guess is correct"
        self.alreadyAsked.append(userGuess)
        if userGuess in self.wordToGuess:
            for i in range(len(self.wordToGuess)):
                if self.wordToGuess[i] == userGuess:
                    self.state[i] = userGuess + " "
                    self.unguessedLettersRemaining -= 1
        else:
            self.lives -= 1
    
    def setState(self):
        """Sets initial values at the beginning of every game
        Randomly selects a word from the list of words and
        sets other values based on that"""
        self.wordToGuess = random.choice(self.wordList).rstrip()
        self.unguessedLettersRemaining = len(self.wordToGuess)
        self.lives = 10
        self.state = []
        self.alreadyAsked = []
        for i in range(len(self.wordToGuess)):
            self.state.append("- ")

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
