#!/usr/bin/env python
import sys

# Input comes from the standard input line by line (not word by word!)
for line in sys.stdin:
        # Clean whitespace at front and end, then split into a list of words
        line = line.strip()
        words = line.split()

        for word in words:
            # Output each word as the key, with 1 as the value (count of word)
	    print "%s %s" % (word, 1)

