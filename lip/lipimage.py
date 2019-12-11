from .utils import imgload
import numpy as np
import itertools

class LIPImage(object):
    def __init__(self, values):
        self._values = 255 - np.array(values, dtype='uint8')
        self.x = len(values)
        self.y = len(values[0])

    def __add__(self, g):
        if isinstance(g, int):
            g = LIPImage.constant_image(g, self.dim)

        if self.dim != g.dim:
            raise Exception('Images dimensions don\'t match')
        
        m_f = self.gray_levels
        m_g = g.gray_levels

        res = (m_f + m_g) - (m_f * m_g) / 256
        return LIPImage(res)
    
    def __sub__(self, g):
        if isinstance(g, int):
            g = LIPImage.constant_image(g, self.dim)

        if self.dim != g.dim:
            raise Exception('Images dimensions don\'t match')

        m_f = self.gray_levels
        m_g = g.gray_levels

        res = (m_f - m_g) / (1 - (m_g / 256))
        return LIPImage(res)

    def __rmul__(self, r):
        m_f = self.gray_levels

        res = 256 - 256 * (1 - m_f/256)**r
        return LIPImage(res)

    def __getitem__(self, tp):
        return int(self._values[tp])

    def __repr__(self):
        return self._values.__repr__()

    def __str__(self):
        return self._values.__str__()

    @staticmethod
    def constant_image(k: int, dim: tuple):
        const = np.full(dim, k)
        return LIPImage(const)

    @staticmethod
    def from_file(fname, in_gray=False):
        im = imgload(fname, in_gray=in_gray)
        return LIPImage(im)

    @property
    def dim(self):
        return self.x, self.y

    @property
    def gray_levels(self):
        return self._values

    @property
    def M(self):
        return 256