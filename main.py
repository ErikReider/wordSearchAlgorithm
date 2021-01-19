#!/usr/bin/python3.9

import math
import random

wordsList = open("./words.txt")
listy = wordsList.read().splitlines()
wordsList.close()

gridBlank = "_"

gridSize = 10
grid = [gridBlank for i in range(gridSize**2)]

words: [str] = []

i = 0
while i < gridSize * 1.5:
    random.shuffle(listy)
    word = listy.pop(0)
    if len(word) > 4 or len(word) < 3:
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

    if xPos > gridSize - len(word) or yPos > gridSize - len(word):
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
        tempGrid[pos] = word[i]
    return tempGrid


usedWords: [str] = []

# Main loop
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

# Print the result
print("\n".join([" ".join(row) for row in [grid[i:i+gridSize] for i in range(0, len(grid), gridSize)]]))
