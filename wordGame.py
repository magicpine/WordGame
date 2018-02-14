####################################
#        Python Word Game          #
####################################
#   Christian Bradford C00223037   #
####################################
import os
import requests
import pickle
import random
import enchant
from collections import Counter
from datetime import datetime
import sys


def checkSystem():
    if sys.platform == 'win32':
        return 'cls'
    return 'clear'


def setUpWordList(minLength):
    if (not(os.path.exists("words"))):
        try:
            page = requests.get('http://paulbarry.itcarlow.ie/words.txt')
        except:
            print("listen you need an internet connection. I'm Sorry")
            sys.exit()
        # get a string of all the words
        words = page.text
        words = words.split('\n')
        with open('words', 'wb') as fp:
            pickle.dump(words, fp)
    else:
        with open('words', 'rb') as fp:
            words = pickle.load(fp)
    return [bigWord for bigWord in words if (len(bigWord)) >= minLength]


def draw(sourceWord, guesses, totalGuessesNeeded, clearCommand):
    os.system(clearCommand)
    print("You need", totalGuessesNeeded -
          len(guesses), "more guesses to win the game")
    print("You can only type in one guess at a time!")
    print("You have", len(guesses), "guesses right: \n")
    print(*guesses, sep=',\n')
    print("\nThe word is:", sourceWord, "\n")


def init(correctGuesses, clearCommand):
    os.system(clearCommand)
    print("Welcome to the famous word game.")
    print("To play this game you must give the game", correctGuesses,
          "words using the letters of the chosen word.")
    print("The rules are: ")
    # Rules 1 and 2 where to long to have in a single print statement.
    print("\t1. Each word is made up from letters", end='')
    print(" contained within the source word.")
    print("\t2. Each word exists within the dictionary", end='')
    print(" (i.e., it's a “real” word).")
    print("\t3. The words all have three letters or more.")
    print("\t4. There are no duplicates.")
    print("\t5. None of the seven submitted words is the source word.")
    print("This is a race agaisnt the clock.")
    input("Press enter to start the game.")
    return datetime.now()


def logic(sourceWord, guesses, spellCheck):
    redo = True
    while(redo):
        redo = False
        inputedWord = (input("Enter a Word: ")).strip()
        if (inputedWord == ''):
            redo = True
            print("\tYou have to enter a word")
        else:
            inputedWord = inputedWord.lower()
            # Rule One
            cword = Counter(sourceWord)
            cword2 = Counter(inputedWord)
            ruleOneCheck = cword & cword2
            if (ruleOneCheck != cword2):
                redo = True
                print("\tMust only use letters in the source word.")
            # Rule Two
            if (not(spellCheck.check(inputedWord))):
                redo = True
                print("\tThe word must be a real word.")
            # Rule Three
            if (len(inputedWord) < 3):
                redo = True
                print("\tThe word must be longer then three characters long")
            # Rule Four
            if (inputedWord in guesses):
                redo = True
                print("\tYou have already guessed that word")
            # Rule Five
            if (inputedWord == sourceWord):
                redo = True
                print("\tYou can not put the same word as the sourceword")
    return inputedWord


################################################################
#                         Varibles                             #
################################################################
# Number of guesses to win the game
correctGuesses = 7
# Min length of characters for words to be used in source words
minLengthOfCharacters = 7
################################################################
#                      Run Only Once                           #
################################################################
# get list of words and source word
sourceWords = setUpWordList(minLengthOfCharacters)
spellCheck = enchant.Dict("en_US")
clearCommand = checkSystem()
################################################################
#                      Run For Each Game                       #
################################################################
if __name__ == '__main__':
	quitGame = False
	while (not(quitGame)):
		startTime = init(correctGuesses, clearCommand)
		isGameRunning = True  # A flag for the game to run
		guesses = []  # list of correct guesses
		sourceWord = (random.choice(sourceWords)).lower()
		while (isGameRunning):
			draw(sourceWord, guesses, correctGuesses, clearCommand)
			guess = logic(sourceWord, guesses, spellCheck)
			guesses.append(guess)
			if (len(guesses) >= correctGuesses):
				isGameRunning = False
				endTime = datetime.now()
		draw(sourceWord, guesses, correctGuesses, clearCommand)
		timetook = (endTime - startTime).total_seconds()
		os.system(clearCommand)
		print("Congratulations, you have won the game!!!!!")
		print("It took you", timetook, "seconds to beat the game\n")
		if (not(os.path.exists("scores"))):
			scores = [('aaa', 150, "TESTINGS"), ('bbb', 160, "TESTINGS"),
					  ('ccc', 170, "TESTINGS"), ('ddd', 180, "TESTINGS"),
					  ('eee', 190, "TESTINGS"), ('fff', 200, "TESTINGS"),
					  ('ggg', 210, "TESTINGS"), ('hhh', 220, "TESTINGS"),
					  ('iii', 230, "TESTINGS"), ('jjj', 240, "TESTINGS")]
			with open('scores', 'wb') as fp:
				pickle.dump(scores, fp)
		else:
			with open('scores', 'rb') as fp:
				scores = pickle.load(fp)
		name = input("Enter your name for the scores list: ")
		scores.append((name, timetook, sourceWord))
		scores = sorted(scores, key=lambda x: x[1])
		place = (scores.index((name, timetook, sourceWord))) + 1
		print(name, "you placed: ", place, "out of", len(scores))
		if (place < 11):
			print("Congratulations! You have placed in the top ten")
		for item in scores[:10]:
			print("Place:  ", scores.index(item) + 1, "| Name:  ", item[0], end='')
			print(" | Time:  ", item[1], " | Word:  ", item[2])
		with open('scores', 'wb') as fp:
			pickle.dump(scores, fp)
		quitGameInput = input("Would you like to play again (y|n)? ")
		if (quitGameInput.lower()[0] != "y"):
			quitGame = True
