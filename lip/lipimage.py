import numpy as np
import itertools

dirs8 = list(itertools.product([0,1,-1],[0,1,-1]))
dirs8.remove((0,0))

class LIPImage(object):
    def __init__(self, values, M=256):
        self.values = np.array(values)
        self.x = len(self.values)
        self.y = len(self.values[0])
        self.M = M

    def N8(self, x):
        px, py = x
        return [self.gray_levels[px+ dx][py + dy] for dx, dy in dirs8]

    def N4(self, x):
        px, py = x
        return [self.gray_levels[px - 1][py],
                self.gray_levels[px + 1][py],
                self.gray_levels[px][py - 1],
                self.gray_levels[px][py + 1]]

    def __add__(self, g):
        if isinstance(g, int):
            g = LIPImage.constant_image(g, self.dim)

        if self.dim != g.dim:
            raise Exception('Images dimensions don\'t match')
        
        m_f = self.gray_levels
        m_g = g.gray_levels
        M = self.M

        res = (m_f + m_g) - (m_f * m_g) / M
        return LIPImage(res, M)
    
    def __sub__(self, g):
        if isinstance(g, int):
            g = LIPImage.constant_image(g, self.dim)

        if self.dim != g.dim:
            raise Exception('Images dimensions don\'t match')

        m_f = self.gray_levels
        m_g = g.gray_levels
        M = self.M

        res = (m_f - m_g) / (1 - (m_g / M))
        return LIPImage(res, M)

    def __rmul__(self, r):
        m_f = self.gray_levels
        M = self.M

        res = M - M * (1 - m_f/M)**r
        return LIPImage(res, M)

    def __getitem__(self, tp):
        x, y = tp
        return self.values[x][y]

    def __repr__(self):
        return self.values.__repr__()

    def __str__(self):
        return self.values.__str__()

    @staticmethod
    def constant_image(k: int, dim: tuple):
        const = np.full(dim, k)
        return LIPImage(const)

    @property
    def dim(self):
        return self.x, self.y

    @dim.deleter
    def dim(self):
        raise Exception('Can not delete the dimension')

    @dim.setter
    def dim(self, *dim):
        raise Exception('Image dimension is constant')

    @property
    def gray_levels(self):
        return self.values

    @gray_levels.setter
    def gray_levels(self, gray_levels):
        raise Exception('Gray Levels are constants')

    @gray_levels.deleter
    def gray_levels(self):
        raise Exception('Can not delete the gray levels information')

    @property
    def M(self):
        return self.M

    @M.setter
    def M(self, m):
        raise Exception('M value is can not change')

    @M.deleter
    def M(self):
        raise Exception('Can not delete the M value')