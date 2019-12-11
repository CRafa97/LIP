from utils import N4, N8, inside
from lipimage import LIPImage
import math

def add_log(f, g):
    return int(f + g - ((f * g) / 256))

def sub_log(f, g):
    return ((f - g) / (1 - g / 256))

def mul_log(k, f):
    return int(256 - 256 * (1 - f/256)**k)

def lmc(px, py):
    try:
        if px == py:
            return 1
        return math.log(1 - max(px, py) / 256) / math.log(1 - min(px, py) / 256)
    except ZeroDivisionError:
        p = max(px, py)
        return math.log(1 - p / 256) / math.log(1 - 1 / 256) 

def lac(px, py):
    n = abs(px - py)
    d = (1 - min(px, py) / 256)
    return n / d
    
def kohler_contrast(px, py, t, contrast=lac):
    return min(contrast(px, t), contrast(py, t))

def lip_kohler(image: LIPImage, contrast=lac):
    to = -1
    x, y = image.dim
    for t in range(256):
        cl_contrast = 0
        count = 0
        for i in range(x):
            for j in range(y):
                if image[i,j] < t:
                    neighbors = N4(i, j, filter = lambda x: inside(image.gray_levels, x) and image[x] >= t)
                    for n in neighbors:
                        cl_contrast = add_log(cl_contrast, kohler_contrast(image[i,j], image[n], t, contrast=contrast))
                    count += len(neighbors)
        try:
            to = max(to, mul_log(1 / count, cl_contrast))
        except:
            pass

    return to

def lac_average_contrast(img: LIPImage, p):
    x, y = p
    c = 0
    for n in N8(x, y, filter=lambda x: inside(img.gray_levels, x)):
        c = add_log(c, lac(img[p], img[n]))
    return mul_log(1/8, c)

def lmc_average_contrast(img: LIPImage, p):
    x, y = p
    c = 0
    for n in N8(x, y, filter=lambda x: inside(img.gray_levels, x)):
        c += lmc(img[p], img[n])
    return 1/8 * c

def maximal_contrast(img: LIPImage, p, contrast=lac):
    x, y = p
    c = 0
    for n in N8(x, y, filter=lambda x: inside(img.gray_levels, x)):
        c = max(c, contrast(img[p], img[n]))
    return int(c)

def maximal_dynamic_range(img: LIPImage):
    fa = img.gray_levels.max()
    fb = img.gray_levels.min()
    
    da = math.log(1 - fa / 256)
    db = math.log(1 - fb / 256)

    return math.log( da / db ) / math.log( db / da )