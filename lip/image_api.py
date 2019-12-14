from .utils import threshold, RGB2gray
from .lipimage import LIPImage
from .algorithms import *
from skimage import io
from skimage.transform import rescale
from skimage.io import imsave
from skimage.data import camera, astronaut
import matplotlib.pyplot as plt
import numpy as np

def grays(img: LIPImage, folder):
    im = 255 - img.gray_levels
    pth = folder + 'grays.jpg'
    imsave(pth, im)
    return pth

def _immap(img: LIPImage, func, folder, name):
    pth = folder + name
    im = np.zeros(img.gray_levels.shape)
    for i in range(img.gray_levels.shape[0]):
        for j in range(img.gray_levels.shape[1]):
            im[i, j] = func(img,(i,j))
    imsave(pth, im)
    return name

def lac_avg(img: LIPImage, folder):
    return _immap(img, lac_average_contrast, folder, 'lac_avg.jpg')
    
def lac_max(img: LIPImage, folder):
    return _immap(img, lambda im, p: maximal_contrast(im, p, contrast=lac), folder, 'lac_max.jpg')
    
def lmc_avg(img: LIPImage, folder):
    return _immap(img, lmc_average_contrast, folder, 'lmc_avg.jpg')

def lmc_max(img: LIPImage, folder):
    return _immap(img, lambda im, p: maximal_contrast(im, p, contrast=lmc), folder, 'lmc_max.jpg')

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

