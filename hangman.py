import random
import re

class Hangman:
    def __init__(self):
        self.wordList = loadWordsFromFile("words.txt") #A list of words to pick from
        self.state = "" #A list that tracks the player's correct/incorrect guesses, ex. "f__k"
        #print(self.wordList)
        self.lives = 10 #An int that represents the number of remaining attempts
        self.wordToGuess = "hello"

    def playGame(self):
        "Begin the main game loop for a single game. Can be called again to start another game"
        #self.wordToGuess = random.choice(self.wordList).rstrip() #Pick a random word
        self.setState()
        while True:
            self.sendStateToPlayer()
            userGuess = self.receiveInputFromPlayer()
            self.updateStateAccordingToGuess(userGuess)
            #print(wordToGuess)
            #break #TODO: Remove later when done

    def sendStateToPlayer(self):
        "Displays the state on the player's end along with a reminder of how many lives are left"
        print(''.join(self.state))
        print(f"You have {self.lives} left.")

    def receiveInputFromPlayer(self):
        while True:
            guess = input("Input your guess: ")
            if re.fullmatch("[a-zA-Z]", guess) == None: #Use regex to verify that guess is a single letter
                print("Guess must be a single letter.")
                continue
            else:
                break
        return guess
    
    def updateStateAccordingToGuess(self, userGuess):
        "Replaces the blank spaces if the user's guess is correct"
        for i in range(len(self.wordToGuess)):
            if self.wordToGuess[i] == userGuess:
                self.state[i] = userGuess + " "
        print(self.state)
    
    def setState(self):
        "Sets initial value of self.state based on the word"
        self.state = []
        for i in range(len(self.wordToGuess)):
            self.state.append("- ")
        #print(self.state)

def loadWordsFromFile(filename):
    "Reads the configuration file and returns a list of all its contents"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

h = Hangman()
h.playGame()