from random import  randint, shuffle
import numpy as np
from numpy import allclose

from binq.src.evaluation.Pauli import S
from binq.src.evaluation.Pauli import H
from binq.src.utils.r_utils import matmul


class Clifford_Generator:

    def __init__(self, dimension, log2power):
        self.dimension = dimension
        self.power = log2power
        self.database = []
        self.stringsdb = []

    def numerical_comparison(self, matrix):
        return next(  (True for elem in self.database if elem.size == matrix.size and allclose(elem, matrix, rtol=1e-08, atol=1e-010)) , False)

    def random_string_gen(self, limit):
        zero_count = randint(0, limit)
        one_count = (limit) - zero_count

        string = [0] * zero_count + [1] * one_count
        shuffle(string)

        return string

    def strings_gen(self):
        for i in range(1, self.power):
            for j in range(10):
                sequ = self.random_string_gen(i)
                if( not( sequ in self.stringsdb )):
                    self.stringsdb.append(sequ)

    def generate(self):
        self.strings_gen()
        Hm = H(self.dimension)
        Sm = S(self.dimension)

        for s in self.stringsdb:
            matrix = np.identity(self.dimension)
            for bit in s:
                if(bit):
                    matrix = matmul(Hm.matrix, matrix)
                else:
                    matrix = matmul(Sm.matrix, matrix)

            if( not self.numerical_comparison(matrix)):
                self.database.append(matrix)

        return self.database