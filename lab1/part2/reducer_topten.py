#!/usr/bin/env python
import sys

topTen = {}
currentBigram = None
currentCount = 0

def updateTopTen():
    if not currentBigram:
        return
    if len(topTen) < 10:
        # If length is less than 10, can add this to the dict since we're keeping the top ten
        topTen[currentBigram] = currentCount
    else:
        # Get smallest
        minCount = min(topTen.itervalues())

        # Check if currentCount is greater than the smallest in the dict
        if currentCount > minCount:
            # Loop until find the smallest, then delete it
            for k, v in topTen.iteritems():
                if v == minCount:
                    del topTen[k]
                    break

            # Insert the new key
            topTen[currentBigram] = currentCount

# same as the mapper, input comes from the standard input line by line
for line in sys.stdin:
    # Get the bigram
    line = line.strip()
    bigram = line[:-2]

    if bigram == currentBigram:
        currentCount += 1
    else:
        updateTopTen()
        currentBigram = bigram
        currentCount = 1

# Remember to get the last one
updateTopTen()

# Print the top ten
for k in sorted(topTen, key=topTen.get, reverse=True):
    print "%s %s" % (k, topTen[k])
