#!/usr/bin/env python
import sys

# Input comes from the standard input line by line (not word by word!)
for line in sys.stdin:
        # Clean whitespace at front and end, then split into a list of words
        line = line.strip()
        words = line.split()

        for word in words:
            # First do the contraction check
            lower = word.lower()
            firstWord = None
            secondWord = None

            if lower == "i\'m":
                firstWord = word[:1]
                secondWord = "a" + word[2:]
            elif lower == "i\'ve":
                firstWord = word[:1]
                secondWord = "ha" + word[2:]
            elif lower == "aren\'t":
                firstWord = word[:3]
                secondWord = word[3] + "o" + word[5]
            elif lower == "can\'t":
                firstWord = word[:3]
                secondWord = "no" + word[4]
            elif lower == "didn\'t":
                firstWord = word[:3]
                secondWord = word[3] + "o" + word[5]
            elif lower == "couldn\'t":
                firstWord = word[:5]
                secondWord = word[5] + "o" + word[7]
            elif lower == "shouldn\'t":
                firstWord = word[:6]
                secondWord = word[6] + "o" + word[8]
            elif lower == "isn\'t":
                firstWord = word[:2]
                secondWord = word[2] + "o" + word[4]
            elif lower == "you\'re":
                firstWord = word[:3]
                secondWord = "a" + word[-2:]

            if firstWord:
	        # firstWord and secondWord must always both be populated, so we only need to check for one
                print "%s %s" % (firstWord, 1)
	        print "%s %s" % (secondWord, 1)
            else:
                # Output the word as the key, with 1 as the value (count of word)
	        print "%s %s" % (word, 1)

