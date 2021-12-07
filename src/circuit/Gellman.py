import numpy as np


class GellMann:
    # TODO WE CAN BUILD TEST CASES FOR THIS, BUT I SWEATED ALREADY TOO MUCH ON THIS.
    # TODO BE CAREFUL IF YOU MAKE ANY CHANGES AND TEST IT CAREFULLY

    def __init__(self, lev_a, lev_b, type_m, d):
        """Definition taken from https://mathworld.wolfram.com/GeneralizedGell-MannMatrix.html"""

        self.lev_a = lev_a
        self.lev_b = lev_b
        self.type_m = type_m
        self.d = d

        self.matrix = np.zeros((d, d), dtype=complex)

        if type_m == "s":

            self.matrix[lev_a, lev_b] = 1
            self.matrix[lev_b, lev_a] = 1

        elif type_m == "a":
            self.matrix[lev_a, lev_b] -= 1j
            self.matrix[lev_b, lev_a] += 1j

        else:
            # lev_a is l in this case

            E = np.zeros((d, d))

            for j_ind in range(0, lev_b):
                E[j_ind, j_ind] += 1

            E[lev_b, lev_b] -= lev_b

            coeff = np.sqrt(2 / (lev_b * (lev_b + 1)))

            E = coeff * E

            self.matrix = E

    def m(self):
        return self.matrix
