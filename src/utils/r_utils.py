import numpy as np


def newMod(a, b=2 * np.pi):
    res = np.mod(a, b)
    return res if not res else res - b if a < 0 else res


def Pi_mod(a):
    a = newMod(a)

    if (a > 0 and a > np.pi):
        a = a - 2 * np.pi
    elif (a < 0 and abs(a) > np.pi):
        a = 2 * np.pi + a
    return a


def matmul(f, s):
    dim = f.shape[1]
    rows_s = s.shape[0]
    if (dim != rows_s):
        raise Exception('not matching dims')

    mat = [[] for x in range(dim)]

    for i in (range(dim)):
        for j in range(dim):
            mat[i].append(f[i, :].dot(s[:, j]))

    return np.array(mat)
