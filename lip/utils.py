from skimage import io
from skimage.color import rgb2gray
import numpy as np

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

def threshold(A, t):
    umb = lambda x: x if x >= t else 0
    m = np.zeros(A.shape)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            m[i, j] = umb(A[i, j])
    return m

def wavelet_threshold(t,*coef):
    WAs = [coef[0][0], coef[0][1], coef[0][2]]
    WTs = [np.zeros(coef[0][0].shape),np.zeros(coef[0][1].shape),np.zeros(coef[0][2].shape)]
   
    for k,wa in enumerate(WAs):
        for i in range(wa.shape[0]):
            for j in range(wa.shape[1]):
                if wa[i,j] != 0:
                    WTs[k][i, j] = max(1 - t/abs(wa[i, j]),0)*wa[i, j]
                else:
                    WTs[k][i, j] = 1
    return (WTs[0], WTs[1], WTs[2])

def N4(*x, filter=None):
    px, py = x
    n4 = [(px + 1, py),
          (px, py + 1),
          (px - 1, py),
          (px, py - 1)]
    return [n for n in n4 if filter(n)] if filter else n4

def N8(*x, filter=None):
    px, py = x
    n8 = [(px + 1, py),
          (px, py + 1),
          (px - 1, py),
          (px, py - 1),
          (px - 1, py - 1),
          (px + 1, py - 1),
          (px - 1, py + 1),
          (px + 1, py + 1)]
    return [n for n in n8 if filter(n)] if filter else n8

def inside(arr, idx:tuple):
    x, y = idx
    return all([x >= 0, y >= 0, x < len(arr), y < len(arr[0])]) 