import random

class Hangman:
    def __init__(self):
        self.wordList = loadWordsFromFile("words.txt") #A list of words to pick from
        self.state = "" #A list that tracks the player's correct/incorrect guesses, ex. "f__k"
        #print(self.wordList)
        self.lives = 10 #An int that represents the number of remaining attempts

    def playGame(self):
        "Begin the main game loop for a single game. Can be called again to start another game"
        wordToGuess = random.choice(self.wordList).rstrip() #Pick a random word
        self.setState(wordToGuess)
        while True:
            self.sendStateToPlayer()
            #print(wordToGuess)
            break #TODO: Remove later when done

    def sendStateToPlayer(self):
        print()
    
    def setState(self, word):
        "Sets self.state based on the word"
        self.state = len(word) * "_"
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
string = "hi"
string[1] = "a"
print(string)