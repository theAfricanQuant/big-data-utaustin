#!/usr/bin/env python
import sys

currentFirstWord = None
currentFirstWordCount = 0

secondWords = dict()

def calculateForCurrentFirstWord():
    for k, v in secondWords.iteritems():
        percentage = int(round((float(v) / float(currentFirstWordCount)) * 100))
        print "P(%s|%s) = %s%%" % (k, currentFirstWord, percentage)

for line in sys.stdin:
    words = line.split()

    firstWord = words[0]
    secondWord = words[1]

    if firstWord == currentFirstWord:
        currentFirstWordCount += 1
        if secondWord in secondWords:
            secondWords[secondWord] += 1
        else:
            secondWords[secondWord] = 1
    else:
        if currentFirstWord:
            # calculate and print them
            calculateForCurrentFirstWord()
        currentFirstWord = firstWord
        currentFirstWordCount = 1
        secondWords.clear()
        secondWords[secondWord] = 1

# calculate and print the last one
calculateForCurrentFirstWord()
