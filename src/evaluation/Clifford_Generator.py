from random import randint, shuffle

import numpy as np
from numpy import loadtxt
from numpy import savetxt

from src.evaluation.Pauli import H
from src.evaluation.Pauli import S
from src.utils.r_utils import matmul


class Clifford_Generator:

    def __init__(self, dimension, log2power=0, saving_path="/"):
        self.dimension = dimension
        self.power = log2power
        self.saving_path = saving_path
        self.database = []
        self.stringsdb = []

    def numerical_comparison(self, matrix):
        for elem in self.database:
            if (elem.size == matrix.size):
                if ((abs(matrix - elem) < 1e-12).all()):
                    return True

        return False

    def random_string_gen(self, limit):
        zero_count = randint(0, limit)
        one_count = (limit) - zero_count

        string = [0] * zero_count + [1] * one_count
        shuffle(string)
        shuffle(string)
        shuffle(string)
        shuffle(string)

        return string

    def strings_gen_random(self):
        for i in range(1, self.power):
            for j in range(1000000):
                sequ = self.random_string_gen(i)
                if (not (sequ in self.stringsdb)):
                    self.stringsdb.append(sequ)

    def genbin(self, n, l, bs=[]):
        if (n - 1):
            self.genbin(n - 1, l, bs + [0])
            self.genbin(n - 1, l, bs + [1])
        else:
            l.append(bs)

    def strings_gen_fixed(self):
        for i in range(2, self.power + 2):
            self.genbin(i, self.stringsdb)

    def generate(self):
        if (not self.power):
            return

        self.strings_gen_fixed()
        Hm = H(self.dimension)
        Sm = S(self.dimension)

        for s in self.stringsdb:
            matrix = np.identity(self.dimension, dtype='complex')
            for bit in s:
                if (bit):
                    matrix = matmul(Hm.matrix, matrix)
                else:
                    matrix = matmul(Sm.matrix, matrix)

            if (not self.numerical_comparison(matrix)):
                self.database.append(matrix)
                self.save_to_csv(matrix, s)

        return self.database

    def save_to_csv(self, matrix, name):
        name = " ".join(str(x) for x in name)
        savetxt(self.saving_path + "dim" + str(self.dimension) + "/" + str(name) + ".csv", matrix, fmt='%.12e',
                delimiter=',')

    @staticmethod
    def load_from_csv(path):
        data = loadtxt(path, delimiter=',', dtype=complex,
                       converters={0: lambda s: complex(s.decode().replace('+-', '-'))})
        return data

    @staticmethod
    def generate_all_3_5_7(path):

        C3 = Clifford_Generator(3, 9, path)  # log2(500)=9
        C3.generate()
        print("ok3")
        C5 = Clifford_Generator(5, 12, path)  # log2(4000) = circa 12
        C5.generate()
        print("ok5")
        C7 = Clifford_Generator(7, 13, path)  # 2^14= 16384
        C7.generate()
        print("ok7")
