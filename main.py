import math
import random

wordsList = open("./words.txt")
listy = wordsList.read().splitlines()
wordsList.close()

gridSize = 10
grid = ["_" for i in range(gridSize**2)]

words = []

i = 0
while i < gridSize * 1.5:
    random.shuffle(listy)
    word = listy[0]
    if len(word) > 4 or len(word) < 3:
        continue
    words.append(word)
    listy.pop(0)
    i += 1


def tryWord(tempGrid: [str], word: str, ori: str, position: int):
    xPos = position % gridSize
    yPos = math.floor(position / gridSize)

    if ori == 0:
        if xPos > gridSize - len(word):
            return None
        index = xPos
        indexes = []
        for char in word:
            i = index + (gridSize * yPos)
            if tempGrid[i] == "_" or tempGrid[i] == char:
                indexes.append(i)
                index += 1
            else:
                return None
        for i, pos in enumerate(indexes):
            tempGrid[pos] = word[i]

    elif ori == 1:
        if yPos > gridSize - len(word):
            return None
        index = yPos
        indexes = []
        for char in word:
            i = xPos + (gridSize * index)
            if tempGrid[i] == "_" or tempGrid[i] == char:
                indexes.append(i)
                index += 1
            else:
                return None
        for i, pos in enumerate(indexes):
            tempGrid[pos] = word[i]

    elif ori == 2:
        if xPos > gridSize - len(word) or yPos > gridSize - len(word):
            return None
        index = yPos
        diag = 0
        indexes = []
        for char in word:
            i = xPos + (gridSize * index) + diag
            if tempGrid[i] == "_" or tempGrid[i] == char:
                indexes.append(i)
                index += 1
                diag += 1
            else:
                return None
        for i, pos in enumerate(indexes):
            tempGrid[pos] = word[i]

    return tempGrid

usedWords:[str] = []

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
        continue


printString = ""
for i, char in enumerate(grid):
    printString += " " + str(char)
    if i % gridSize == gridSize - 1 and i != len(grid) - 1:
        printString += "\n"
print(printString)
