from skimage import io
from skimage.color import rgb2gray
import itertools

def imgload(fname, in_gray=False):
    """ Loads a image and convert it to the gray scale format(0 - 255), use in_gray=True for load 
    a image in gray scale """
    im = None
    if in_gray:
        im = io.imread(fname)
    else:
        im = io.imread(fname, as_gray=True)
        im = (im * 255).round()
    return im.astype('uint8')

def RGB2gray(image):
    """ Converts a RGB image to gray """
    g_scale = rgb2gray(image)
    im = (g_scale * 255).astype('uint8')
    return im

def N4(*x, filter=None):
    px, py = x
    n4 = [(px + 1, py),
          (px, py + 1),
          (px - 1, py),
          (px, py - 1)]
    return [n for n in n4 if filter(n)] if filter else n4

def inside(arr, idx:tuple):
    x, y = idx
    return all([x >= 0, y >= 0, x < len(arr), y < len(arr[0])]) 