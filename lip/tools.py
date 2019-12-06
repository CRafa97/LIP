def lac(x, y, f):
    f_x = f[x]
    f_y = f[y]
    M = f.M
    return abs(f_x - f_y) / (1 - min(f_x, f_y) / M)