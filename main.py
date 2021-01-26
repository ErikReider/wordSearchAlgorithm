#!/usr/bin/python3.9
import math
import time
import random
import string
from colorama import Fore, Back, Style

gridSize = 7
numberOfWords = gridSize**2 / 8
gridBlank = "_"

# Gets a list with random words
wordsList = open("./words.txt")
listy = wordsList.read().splitlines()
wordsList.close()
words: [str] = []
i = 0
while i < numberOfWords and len(listy) > 0:
    word = listy.pop(random.randint(0, len(listy) - 1))
    if len(word) > gridSize or len(word) < 3:
        continue
    words.append(word)
    i += 1


# Returns new grid with word in it if the word fits
def tryWord(tempGrid: [str], word: str, ori: str, pos: int):
    xPos = pos % gridSize
    yPos = math.floor(pos / gridSize)
    indexes: [int] = []
    diagInc = 0
    index = xPos if ori == 0 else yPos

    if (ori == 2 or ori == 0) and xPos > gridSize - len(word):
        return None
    if (ori == 2 or ori == 1) and yPos > gridSize - len(word):
        return None

    for char in word:
        i = (index + gridSize * yPos) if ori == 0 else (xPos + gridSize*index)
        if ori == 2:
            i += diagInc
            diagInc += 1
        if tempGrid[i] == gridBlank or tempGrid[i] == char:
            indexes.append(i)
            index += 1
        else:
            return None
    for i, pos in enumerate(indexes):
        tempGrid[pos] = "\033[91m" + word[i] + "\033[00m"
    return tempGrid


# Returns the complete grid
def getGrid(words: [str], fillBlank=True):
    grid = [gridBlank for i in range(gridSize**2)]
    usedWords: [str] = []
    wordIndex = 0
    orientations = [i for i in range(3)]
    positions = [i for i in range(gridSize**2)]
    currentPos = positions.pop(random.randint(0, len(positions) - 1))
    while wordIndex < len(words):
        if len(orientations) == 0:
            currentPos = positions.pop(random.randint(0, len(positions) - 1))
            orientations = [i for i in range(3)]
            continue
        if len(positions) == 0:
            positions = [i for i in range(gridSize**2)]
            wordIndex += 1
            continue
        ori = orientations.pop(random.randint(0, len(orientations) - 1))
        gridTry = tryWord(grid, words[wordIndex], ori, currentPos)
        if gridTry != None:
            usedWords.append(words[wordIndex])
            grid = gridTry
            wordIndex += 1
    if fillBlank:
        grid = list(map(lambda x: x if x != gridBlank else random.choice(
            string.ascii_lowercase), grid))
    return (grid, usedWords)


grid, usedWords = getGrid(words)

# Print the result
print("\n".join([" ".join(row) for row in [grid[i:i+gridSize]
                                           for i in range(0, len(grid), gridSize)]]))
