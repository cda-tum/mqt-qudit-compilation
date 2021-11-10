import numpy as np

from binq.src.utils.r_utils import matmul


class Verifier:

    def __init__(self, sequence, target, original_map, final_map, dimension):
        self.decomposition = sequence
        self.target = target.matrix.copy()
        self.dimension = dimension
        self.permutation_matrix = self.get_perm_matrix(original_map, final_map)
        #self.permutation_matrix = self.per_mat()
        self.target = matmul(self.permutation_matrix , self.target)

    def per_mat(self):
        perm = np.identity(self.dimension, dtype='complex')
        for gate in self.decomposition:
            if(gate.theta == np.pi or gate.theta == -np.pi  ):
                perm = matmul(perm, gate.matrix)

        return perm

    def get_perm_matrix(self, original, final):
        max_col = len(original)
        max_row = len(final)
        perm = np.zeros((self.dimension,self.dimension))

        for i in range(max_row):
            for j in range(max_col):
                if(original[j]==final[i]):
                    perm[i,j] = 1

        return perm

    def verify(self):
        product = np.identity(self.dimension , dtype='complex') #starts with Identity

        for rotation in reversed(self.decomposition):
            product = matmul(rotation.matrix.conj().T.copy(), product)

        diff = self.target- product
        res = not np.any(diff > 1.0e-3)

        return res


