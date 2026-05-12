import random
import re

class Hangman:
    def __init__(self):
        self.wordList = loadWordsFromFile("words.txt") #A list of words to pick from
        self.state = "" #A list that tracks the player's correct/incorrect guesses, ex. "f__t"
        
        self.lives = 10 #An int that represents the number of remaining attempts
        self.unguessedLettersRemaining = 0 #An int that represents the number of unguessed letters

        self.wordToGuess = "hello"
        self.alreadyAsked = []

    def playGame(self):
        "Begin the main game loop for a single game. Can be called again to start another game"
        #self.wordToGuess =  #Pick a random word
        self.setState()
        while True:
            self.sendStateToPlayer()
            userGuess = self.receiveInputFromPlayer()
            self.updateStateAccordingToGuess(userGuess)
            if self.unguessedLettersRemaining == 0:
                print(f"Congratulations! The correct word\
                      was indeed {self.wordToGuess}.\
                        Want to play again?")
                break
            elif self.lives == 0:
                print(f"Sorry, you have used up all 10 of your lives. \
                      The correct word was {self.wordToGuess}.\
                        Want to play again?")
                break
            #print(wordToGuess)
            #break #TODO: Remove later when done

    def sendStateToPlayer(self):
        "Displays the state on the player's end along with a reminder of how many lives are left"
        print(''.join(self.state))
        print(f"You have {self.lives} lives left.")

    def receiveInputFromPlayer(self):
        while True:
            guess = input("Input your guess: ")
            if re.fullmatch("[a-zA-Z]", guess) == None: #Use regex to verify that guess is a single letter
                print("Guess must be a single letter.")
                continue
            elif guess in self.alreadyAsked:
                print("You have already guessed this letter.")
                continue
            else:
                break
        return guess
    
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
        #self.wordToGuess = random.choice(self.wordList).rstrip()
        self.unguessedLettersRemaining = len(self.wordToGuess)
        self.lives = 10
        self.state = []
        for i in range(len(self.wordToGuess)):
            self.state.append("- ")

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