#!/usr/bin/env python
import sys

currentWord = None
currentCount = 0

# same as the mapper, input comes from the standard input line by line
for line in sys.stdin:
    # Split line by word and count
    word, cnt = line.split()

    if word == currentWord:
        currentCount += 1
    else:
        if currentWord:
            print "%s %s" % (currentWord, currentCount)
        
        # Now change the current word and count to the new key
        currentWord = word
        currentCount = 1

print "%s %s" % (currentWord, currentCount)

