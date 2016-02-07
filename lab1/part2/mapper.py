#!/usr/bin/env python
import sys

# Input comes from the standard input line by line (not word by word!)
for line in sys.stdin:
    lastWord = None

    line = line.strip().lower()
    words = line.split()

    for i in range(len(words)):
        if lastWord:
            print "%s %s %s" % (lastWord, words[i], 1)
        lastWord = words[i]

