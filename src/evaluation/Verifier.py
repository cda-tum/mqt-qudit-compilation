import numpy as np

from binq.src.utils.r_utils import matmul


class Verifier:

    def __init__(self, sequence, target, original_map, final_map, dimension):
        self.decomposition = sequence
        self.target = target
        self.dimension = dimension
        self.permutation_matrix = self.get_perm_matrix(original_map, final_map, dimension)
        self.target.matrix = matmul(target.matrix, self.permutation_matrix )

    def get_perm_matrix(self, original, final, dimension):
        max_col = len(original)
        max_row = len(final)
        perm = np.zeros((self.dimension,self.dimension))

        for i in range(max_row):
            for j in range(max_col):
                if(original[j]==final[i]):
                    perm[i,j] =  1

        return perm

    def verify(self):
        product = np.identity(self.dimension , dtype='complex') #starts with Identity

        for rotation in reversed(self.decomposition):
            product = matmul(product, rotation.dag)

        diff = self.target.matrix - product
        res = not np.any(diff > 1.0e-4)

        return res


