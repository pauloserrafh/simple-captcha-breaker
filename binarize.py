#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-image-into-a-pure-black-and-white-image

"""Binarize (make it black and white) an image with Pyhton."""

from PIL import Image
from scipy.misc import imsave
import numpy
import matplotlib.pyplot as plt # import

def find_threshold(image):
    """Find the average value"""
    histo = image.histogram()
    max_val = max(histo)
    max_index = histo.index(max_val)
    return max_index


def binarize_image(img_path, target_path):
    """Binarize an image."""
    image_file = Image.open(img_path)
    image = image_file.crop((20,15, 45, 45))
    image = image.convert('L')  # convert image to monochrome
    threshold = find_threshold(image)
    image = numpy.array(image)
    image = binarize_array(image, threshold)
    imsave(target_path, image)


def binarize_array(numpy_array, threshold):
    """Binarize a numpy array."""
    #find the best cut off value
    cutoff = 30
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] < (threshold + cutoff) and \
                                    numpy_array[i][j] > (threshold - cutoff):
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array


if __name__ == "__main__":
    image_name = 'captcha'
    image_in = 'images/'+image_name+'.jpg'
    image_out= 'images/'+image_name+'out.jpg'

    binarize_image(image_in, image_out)
