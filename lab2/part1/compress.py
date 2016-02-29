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
    assignments = build_assignments_dict(centroids)

    for i in xrange(width):
        for j in xrange(height):
            smallest_distance = sys.maxint
            closest_centroid = None
            
            # Find distance to each centroid and keep the smallest
            for centroid in centroids:
                first_term = pow((centroid[1] - j), 2)
                second_term = pow((centroid[0] - i), 2)
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


# Computes the average location for a given list of (x, y) pairs.
def get_average_location(points):
    count, x, y = 0, 0, 0
    for point in points:
        count += 1
        x += point[0]
        y += point[1]

    x = x / count
    y = y / count

    return (x, y)


# Creates a new list of centroids, given the current centroids
# and the dictionary of current assignments
def move_centroids(centroids, assignments):
    new_centroids = list()
    
    for centroid in centroids:
        average = get_average_location(assignments[centroid])
        new_centroids.append(average)

    return new_centroids

# Runs k means iter number of times.
def k_means(centroids, width, height, iter=100):
    old_centroids = centroids
    for i in xrange(iter):
        assignments = assign(centroids, width, height)
        centroids = move_centroids(centroids, assignments)

        # Check if centroids have convereged. If so, we're done
        if set(old_centroids) == set(centroids):
            break

        old_centroids = centroids

    return centroids


# Determines the color of each pixel at each point in the points list.
# Returns a list of colors as (R, G, B)
def get_colors(points, px):
    colors = list()

    for point in points:
        colors.append(px[point[0], point[1]])

    return colors


# Finds the color in a palette that is closest to the given color.
def closest_color(color, palette):
    smallest_distance = sys.maxint
    closest_color = None

    for c in palette:
        first_term = pow((c[0] - color[0]), 2)
        second_term = pow((c[1] - color[1]), 2)
        third_term = pow((c[2] - color[2]), 2)
        distance = math.sqrt(first_term + second_term + third_term)

        if distance < smallest_distance:
            smallest_distance = distance
            closest_color = c

    if closest_color is None:
        print "Error. Closest color is None"
        sys.exit()

    return closest_color


# Changes the image based on the new palette.
# Each pixel is replaced with the color on the palette that is closest
# to its original color.
def change_image(width, height, px, palette):
    for i in xrange(width):
        for j in xrange(height):
            px[i, j] = closest_color(px[i, j], palette)

    return px


## START EXECUTION ##
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
# TODO: stop if assignments don't change. Right now it does 100 iterations regardless.
centroids = k_means(centroids, width, height)

# Get the compressed palette
palette = get_colors(centroids, px)

# Change image
change_image(width, height, px, palette)
#image.show()

# Save the final image
image.save("result.png")

