#! /usr/bin/python

# Import standard packages
import sys
import os
import math

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


# Creates a list of k random pixel locations, given the width and height of the image,
# as well as the pixels of the image.
def random_pixels(k, width, height):
    random_pixels = list()
    for i in xrange(k):
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        random_pixels.append((x, y))

    return random_pixels


# Builds a dict of tuples where the first item is a centroid location
# and the second item is an empty list (for assignments)
def build_assignments_dict(centroids):
    assignments = dict()

    for centroid in centroids:
        assignments[centroid] = list()

    return assignments


# Assigns each pixel location to the nearest centriod location
# Returns a dict where the keys are the centroid locations,
# and the values are a list of points that are assigned to that centroid.
def assign(centroids, width, height):
    print "In assign"
    assignments = build_assignments_dict(centroids)

    for i in xrange(width):
        for j in xrange(height):
            smallest_distance = sys.maxint
            closest_centroid = None
            
            # Find distance to each centroid and keep the smallest
            for centroid in centroids:
                first_term = pow((centroid[1] - j), 2)
                #print first_term
                second_term = pow((centroid[0] - i), 2)
                #print second_term
                distance = math.sqrt(first_term + second_term)

                if distance < smallest_distance:
                    smallest_distance = distance
                    closest_centroid = centroid

            # Now put this point in the smallest's assignment group
            if closest_centroid is None:
                print "Something weird happened."
                sys.exit()

            assignments[closest_centroid].append((i, j))

    return assignments


def move_centroids():
    print "In move centroids"


# Runs k means iter number of times.
def k_means(centroids, width, height, iter=100):
    for i in xrange(iter):
        print assign(centroids, width, height)
        move_centroids()

    return

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
centroids = random_pixels(k, width, height)

# Run K-means
k_means(centroids, width, height, iter=1)

# Pixel modification (this is just an example. You may delete this line)
#px[0, 0] = (0, 0, 0);

# Display the image (this is just an example. You may delete this line)
#image.show()

# Save the image (this is just an example. You may delete this line)
#image.save("DELETE_ME.png")

