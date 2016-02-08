#!/usr/bin/env python
import sys

currentBigram = None
totalCount = 0

# same as the mapper, input comes from the standard input line by line
for line in sys.stdin:
    # Get the bigram by taking the string without the count value
    line = line.strip()
    bigram = line[:-2]

    if bigram == currentBigram:
        continue
    else:
        if currentBigram:
            totalCount += 1
        currentBigram = bigram

# Don't forget the last one
if currentBigram:
    totalCount += 1

print "%s" % (totalCount)

