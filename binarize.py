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


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input",
                        dest="input",
                        help="read this file",
                        metavar="FILE",
                        required=True)
    parser.add_argument("-o", "--output",
                        dest="output",
                        help="write binarized file hre",
                        metavar="FILE",
                        required=True)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    binarize_image(args.input, args.output)
