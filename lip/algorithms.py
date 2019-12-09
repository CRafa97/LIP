from utils import N4, inside
from lipimage import LIPImage

def add_log(f, g):
    return int(f + g - ((f * g) / 256))

def sub_log(f, g):
    return ((f - g) / (1 - g / 256))

def mul_log(k, f):
    return int(256 - 256 * (1 - f/256)**k)

def local_contrast(x,y,t):
    return min(sub_log(t, x) , sub_log(y, t))

def lip_kohler(image: LIPImage): 
    to = -1
    x, y = image.dim
    for t in range(256):
        cl_constrast = 0
        count = 0
        for i in range(x):
            for j in range(y):
                if image[i,j] < t:
                    neighbors = N4(i, j, filter = lambda x: inside(image.gray_levels, x) and image[x] >= t)
                    cl_constrast += sum(local_contrast(image[i,j],image[px,py], t) for px, py in neighbors)
                    count += len(neighbors)
        try:
            to = max(to, mul_log(1 / count, cl_constrast))
        except:
            pass

    return to

if __name__ == "__main__":
    from skimage.data import astronaut
    from skimage.transform import rescale
    from utils import RGB2gray
    im = RGB2gray(rescale(astronaut(), 0.1))

    im = LIPImage(im)
    print(lip_kohler(im))
        