#! /usr/bin/python

# Import standard packages
import sys
import os

# Import Pillow
from PIL import Image, ImageFilter

# Read image
im = Image.open('bird1.jpg')

# Load all the pixels
px = im.load()

# Pixel access (this is just an example. You may delete this line)
print px[0, 0]

# Pixel modification (this is just an example. You may delete this line)
px[0, 0] = (0, 0, 0);

# Display the image (this is just an example. You may delete this line)
im.show()

# Save the image (this is just an example. You may delete this line)
im.save("DELETE_ME.png")

