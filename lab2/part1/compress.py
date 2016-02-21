#! /usr/bin/python

# Import standard packages
import sys
import os

from PIL import Image, ImageFilter
from random import randint

# Parses the command line arguments. Expects 2 arguments.
# Returns the first argument (filename) as a string and the second (k value) as an int.
def parse_args():
    # Test for correct number of args
    if len(sys.argv) != 3:
        print "Incorrect number of arguments."
        sys.exit()

    return sys.argv[1], int(sys.argv[2])


# Creates a list of k random pixels, given the width and height of the image,
# as well as the pixels of the image.
def random_pixels(k, width, height, px):
    random_pixels = list()
    for i in xrange(k):
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        random_pixels.append(px[x, y])

    return random_pixels


image_name, k = parse_args()

# Read image
try:
    image = Image.open(image_name)
except (IOError):
    print "Error opening file. Please enter a valid filename as the first argument."
    sys.exit()

# Get properties of image
width, height = image.size
px = image.load()

# Get inital random pixels to act as centriods
centriods = random_pixels(k, width, height, px)

# Run K-means

# Pixel modification (this is just an example. You may delete this line)
#px[0, 0] = (0, 0, 0);

# Display the image (this is just an example. You may delete this line)
#image.show()

# Save the image (this is just an example. You may delete this line)
#image.save("DELETE_ME.png")

