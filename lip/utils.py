from skimage import io
from skimage.color import rgb2gray

def imgload(fname, in_gray=False):
    """ Loads a image and convert it to the gray scale format(0 - 255), use in_gray=True for load 
    a image in gray scale """
    im = None
    if in_gray:
        im = imread(fname)
    else:
        im = io.imread(fname, as_gray=True)
        im = (im * 255).round()
    return im.astype('uint8')

def RGB2gray(image):
    """ Converts a RGB image to gray """
    g_scale = rgb2gray(image)
    im = (g_scale*255).astype('uint8')
    return im