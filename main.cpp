#include <bits/types/FILE.h>
#include <math.h>
#include <stdio.h>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <random>

#include <cstdio>
#include <ctime>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

const char *gridBlank = "_";

static random_device rd;

template <typename T>
T popRandom(vector<T> *vec) {
    int index = rd() % vec->size();
    T value = vec->at(index);
    vec->erase(vec->begin() + index);
    return value;
}

vector<string> getAllWords(int *minWordLength, int *maxWordLength) {
    vector<string> allWords = {};
    errno = 0;
    FILE *file = fopen("./words.txt", "r");
    if (file == NULL) {
        cout << "Error! opening file: " << errno << endl;
        exit(1);
    }
    char *line = NULL;
    size_t len = 0;
    while (getline(&line, &len, file) != -1) {
        string strLine = string(line);
        strLine.erase(remove(strLine.begin(), strLine.end(), '\n'), strLine.end());
        if (strLine.length() >= *minWordLength && strLine.length() <= *maxWordLength) {
            allWords.push_back(strLine);
        }
    }
    fclose(file);
    return allWords;
}

vector<string *> getWords(vector<string> allWords,
                          int *wordCount,
                          int *minWordLength,
                          int *maxWordLength) {
    vector<string *> words = {};
    for (int i = 0; i < *wordCount; i++) {
        words.push_back(&allWords[rd() % (allWords.size() - 1)]);
    }
    return words;
}

bool tryWord(vector<char *> *grid, int gridSize, string *word, int ori, int pos) {
    int xPos = pos % gridSize;
    int yPos = floor(pos / gridSize);
    vector<int> indexes = {};
    int diagInc = 0;
    int index = ori == 0 ? xPos : yPos;

    if ((ori == 2 || ori == 0) && xPos > gridSize - (*word).length()) return false;
    if ((ori == 2 || ori == 1) && yPos > gridSize - (*word).length()) return false;

    for (char character : *word) {
        int i = ori == 0 ? (index + gridSize * yPos) : (xPos + gridSize * index);
        if (ori == 2) {
            i += diagInc;
            diagInc++;
        }
        if (grid->at(i) == gridBlank || grid->at(i) == &character) {
            indexes.push_back(i);
            index++;
        } else {
            return false;
        }
    }
    for (int i = 0; i < indexes.size(); i++) {
        grid->at(indexes.at(i)) = &(word->at(i));
    }
    return true;
}

vector<char *> getGrid(vector<string *> words, int *gridSize) {
    vector<char *> grid((*gridSize * *gridSize), const_cast<char *>(gridBlank));
    vector<string *> usedWords = {};
    int wordIndex = 0;

    vector<int> orientations = {0, 1, 2};

    vector<int> positions((*gridSize * *gridSize));
    iota(positions.begin(), positions.end(), 0);

    int currentPos = popRandom(&positions);

    while (wordIndex < words.size()) {
        if (orientations.size() == 0) {
            currentPos = popRandom(&positions);

            orientations = {0, 1, 2};
            continue;
        }
        if (positions.size() == 0) {
            vector<int> newPos((*gridSize * *gridSize));
            iota(newPos.begin(), newPos.end(), 0);
            positions = newPos;
            wordIndex++;
            continue;
        }
        string *currentWord = words.at(wordIndex);
        if (tryWord(&grid, *gridSize, currentWord, popRandom(&orientations), currentPos) == true) {
            usedWords.push_back(currentWord);
            wordIndex++;
        }
    }

    int i = 0;
    for (auto item : grid) {
        if (item == gridBlank) {
            // replaces empty char with a random character
            grid.at(i) = new char(97 + rd() % 26);
        }
        i++;
    }
    return grid;
}

int main(int argc, char *argv[]) {
    int minWordLength = 3;
    int gridSize = 7;
    int wordCount = gridSize * gridSize / 8;
    vector<string> allWords = getAllWords(&minWordLength, &gridSize);
    vector<char *> grid =
      getGrid(getWords(allWords, &wordCount, &minWordLength, &gridSize), &gridSize);

    int index = 1;
    for (auto character : grid) {
        cout << *character << (index % gridSize == 0 ? "\n" : " ");
        index++;
    }
    return 0;
}
