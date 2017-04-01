#rgb2grayscale
#https://samarthbhargav.wordpress.com/2014/05/05/image-processing-with-python-rgb-to-grayscale-conversion/

from scipy import misc
import matplotlib.pyplot as plt # import
import numpy as np
import matplotlib.cm as cm #

def weightedAverage(pixel):
	return 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]

image_path = 'images/'
image_name = 'captcha'
image_ext = '.jpg'

image = misc.imread(image_path+image_name+image_ext)

# plt.imshow(image)

grey = np.zeros((image.shape[0], image.shape[1])) # init 2D numpy array
for rownum in range(len(image)):
	for colnum in range(len(image[rownum])):
		grey[rownum][colnum] = weightedAverage(image[rownum][colnum])

# plt.imshow(grey, cmap = cm.Greys_r)
# plt.show()

misc.imsave(image_path+image_name+'grey'+image_ext, grey)
