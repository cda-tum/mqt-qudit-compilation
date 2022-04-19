import numpy as np
from numpy.linalg import inv

from src.utils.r_utils import matmul


class Verifier:

    def __init__(self, sequence, target, nodes, initial_map, final_map, dimension):
        self.decomposition = sequence
        self.target = target.matrix.copy()
        self.dimension = dimension
        self.permutation_matrix_initial = self.get_perm_matrix(nodes, initial_map)
        self.permutation_matrix_final = self.get_perm_matrix(nodes, final_map)
        self.target = matmul(self.permutation_matrix_initial, self.target)

    def get_perm_matrix(self, nodes, mapping):
        # sum ( |phy> <log| )
        perm = np.zeros((self.dimension, self.dimension))

        for i in range(self.dimension):
            a = [0 for i in range(self.dimension)]
            b = [0 for i in range(self.dimension)]
            a[nodes[i]] = 1
            b[mapping[i]] = 1
            narr = np.array(a)
            marr = np.array(b)
            perm = perm + np.outer(marr, narr)

        return perm

    def verify(self):
        target = self.target.copy()

        for rotation in self.decomposition:
            target = matmul(rotation.matrix, target)
            deb = target.round(2)

        target = matmul(inv(self.permutation_matrix_final), target)

        res = (abs(target - np.identity(self.dimension, dtype='complex')) < 10e-5).all()

        return res
