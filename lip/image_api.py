import numpy as np
from utils import threshold, RGB2gray
from lipimage import LIPImage
from algorithms import *
from skimage import io
from skimage.transform import rescale
from skimage.data import camera, astronaut
import matplotlib.pyplot as plt

def threshold_kohler(img):
    t = lip_kohler(LIPImage(img))
   
    im = threshold(img, t)
    print(im)
    print("**************",t)

    plt.subplot(121)
    plt.imshow(img, cmap='gray')

    plt.subplot(122)
    plt.imshow(im, cmap='gray')
    plt.show()

def average_contrast(img):
    # img1 = LIPImage(img)
    m = np.zeros(img.gray_levels.shape)
    for i in range(img.gray_levels.shape[0]):
        for j in range(img.gray_levels.shape[1]):
            m[i, j] = lac_average_contrast(img,(i,j))

    plt.subplot(121)
    plt.imshow(255 - img.gray_levels, cmap='gray')

    plt.subplot(122)
    plt.imshow(m, cmap='gray')
    plt.show()

if __name__ == '__main__':
    im = LIPImage.from_file('~/Desktop/test.jpg', in_gray=True)
    # threshold_kohler(im)
    average_contrast(im)
    