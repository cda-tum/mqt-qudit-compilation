import numpy as np

from binq.src.utils.r_utils import matmul


class Verifier:

    def __init__(self, sequence, target, dimension):
        self.decomposition = sequence
        self.target = target
        self.dimension = dimension

    def verify(self):
        product = np.identity(self.dimension , dtype='complex') #starts with Identity

        for rotation in reversed(self.decomposition):
            product = matmul(product, rotation.dag)

        diff = self.target.matrix - product
        res = not np.any(diff > 1.0e-4)

        return res


