from src.circuit.Gellman import *

from utils.cost_functions import phi_cost, theta_cost, theta_corrector


# Pay attention : inputs to classes are always in radians
class Custom_Unitary:

    def __init__(self, matrix, dimension):
        self.d = dimension
        self.matrix = matrix

    def cost(self):
        return np.NAN


class R:
    @staticmethod
    def regulate_theta(angle):
        return theta_corrector(angle)

    @staticmethod
    def levels_setter(la, lb, dimension):
        if la == lb:
            raise Exception
        if la < 0:
            la = dimension + la
        if lb < 0:
            lb = dimension + lb
        if la < lb:
            return la, lb
        else:
            return lb, la

    def __init__(self, theta, phi, o_lev_a, o_lev_b, dimension):
        self.original_lev_a = o_lev_a
        self.original_lev_b = o_lev_b
        self.lev_a, self.lev_b = self.levels_setter(o_lev_a, o_lev_b, dimension)

        self.theta = self.regulate_theta(theta)
        self.phi = phi

        self.dimension = dimension

        Identity = np.identity(dimension, dtype='complex')

        Identity[self.lev_a, self.lev_a] = np.cos(theta / 2) * Identity[self.lev_a, self.lev_a]
        Identity[self.lev_b, self.lev_b] = np.cos(theta / 2) * Identity[self.lev_b, self.lev_b]

        cosine_matrix = Identity

        self.matrix = (cosine_matrix - 1j * np.sin(theta / 2) *
                       (np.sin(phi) * GellMann(self.lev_a, self.lev_b, 'a', dimension).matrix +
                        np.cos(phi) * GellMann(self.lev_a, self.lev_b, 's', dimension).matrix))

        self.shape = self.matrix.shape

    @property
    def dag(self):
        return self.matrix.conj().T.copy()

    @property
    def cost(self):
        return theta_cost(self.theta)

    def __str__(self):
        return str(f"R Theta {self.theta} phi {self.phi} lev a {self.original_lev_b} lev b {self.original_lev_b}")

class Rz:

    @staticmethod
    def regulate_theta(angle):
        return theta_corrector(angle)

    @staticmethod
    def levels_setter(lev, dimension):
        if lev < 0:
            return dimension + lev
        else:
            return lev

    def __init__(self, theta, o_lev, dimension):
        self.theta = self.regulate_theta(theta)
        self.lev = self.levels_setter(o_lev, dimension)

        self.dimension = dimension

        Identity = np.identity(dimension, dtype='complex')

        Identity[self.lev, self.lev] = np.exp(-1j * theta) * Identity[self.lev, self.lev]
        self.matrix = Identity

        self.shape = self.matrix.shape

    def __str__(self):
        return str(f"R Theta {self.theta}  lev a {self.lev}")

    @property
    def dag(self):
        return self.matrix.conj().T.copy()

    @property
    def cost(self):
        return phi_cost(self.theta)
