
from src.circuit.Gellman import *


# TODO:                             DISCLAIMER!!!!!!

# TODO: WE CAN BUILD TEST CASES FOR THIS, BUT I SWEATED ALREADY TOO MUCH ON THIS.
# TODO: BE CAREFUL IF YOU MAKE ANY CHANGES AND TEST IT CAREFULLY
# TODO: -------------only the properties have been tested-------------

## Pay attention : inputs to classes are always in radians
## cost functions in this class take input radians but work on units of pi, the rest is taken care automatically

####################### ROTATION MATRICES
class custom_Unitary:
    
    def __init__(self, matrix, dimension):
        
        self.d=dimension
        self.matrix = matrix
        
    def cost(self):
        return np.NAN
        

class R:

    @staticmethod
    def theta_corrector(angle):
        theta_in_units_of_pi = np.mod(abs(angle / np.pi), 4)
        if(angle<0):
            theta_in_units_of_pi = theta_in_units_of_pi * -1
        if (abs(theta_in_units_of_pi) < 0.2):
            theta_in_units_of_pi += 4.0

        return (theta_in_units_of_pi * np.pi)

    @staticmethod
    def levels_setter(la, lb, dimension):
        if(la == lb ):
            raise Exception
        if(la<0):
            la = dimension+la
        if(lb<0):
            lb = dimension+lb

        if(la < lb):
            return la, lb
        else:
            return lb, la

    def __init__(self, theta, phi, o_lev_a, o_lev_b, dimension):

        self.original_lev_a = o_lev_a
        self.original_lev_b = o_lev_b
        self.lev_a, self.lev_b = self.levels_setter(o_lev_a, o_lev_b, dimension)

        self.theta = self.theta_corrector(theta)
        self.phi = phi

        self.dimension = dimension

        Identity = np.identity(dimension, dtype='complex')
        
        Identity[self.lev_a, self.lev_a] = np.cos(theta / 2) * Identity[self.lev_a, self.lev_a]
        Identity[self.lev_b, self.lev_b] = np.cos(theta / 2) * Identity[self.lev_b, self.lev_b]

        cosine_matrix = Identity
        
        
        
        self.matrix =  (cosine_matrix - 1j * np.sin(theta/2) *
                        (np.sin(phi) * GellMann(self.lev_a, self.lev_b, 'a', dimension).matrix +
                         np.cos(phi) * GellMann(self.lev_a, self.lev_b, 's', dimension).matrix))
        
        """control if the matrix is actually correct because different from the slides of Martin, 
            but works as in example"""
        self.shape = self.matrix.shape

    @property
    def dag(self):
        return self.matrix.conj().T.copy()

    @property
    def cost(self):
        theta_on_units = self.theta/np.pi
        
        E = ( 4*abs(theta_on_units) + 1*abs(np.mod(abs(theta_on_units)+0.25, 0.5) - 0.25) )*1e-04
        return E

    def __str__(self):
        return str("R "+"Theta "+str(self.theta)+"phi "+str(self.phi)+"O lev a "+self.original_lev_a+"O lev b "+self.original_lev_b)



class Rz:


    @staticmethod
    def theta_corrector(angle):
        theta_in_units_of_pi = np.mod(abs(angle / np.pi), 4)
        if(angle<0):
            theta_in_units_of_pi = theta_in_units_of_pi * -1
        if (abs(theta_in_units_of_pi) < 0.2):
            theta_in_units_of_pi += 4.0

        return (theta_in_units_of_pi * np.pi)

    @staticmethod
    def levels_setter(lev, dimension):
        if(lev<0):
            return dimension+lev
        else:
            return lev

    def __init__(self,theta, o_lev, dimension):
        
        self.theta = self.theta_corrector(theta) # TODO DISCUSS IF THIS SHOULD GO THROUGH THE CORRECTOR
        self.lev = self.levels_setter(o_lev, dimension)
        
        self.dimension = dimension
        
        Identity = np.identity(dimension, dtype='complex')
        
        Identity[self.lev, self.lev]= np.exp(-1j * theta) * Identity[self.lev, self.lev]
        self.matrix = Identity

        self.shape = self.matrix.shape

    def __str__(self):
        return str("R "+"Theta "+str(self.theta)+"O lev a "+self.lev)

    @property
    def dag(self):
        return self.matrix.conj().T.copy()

    @property
    def cost(self):
        theta_on_units = self.theta / np.pi

        E = abs(theta_on_units) * 1e-04
        return E


class PI_PULSE(R):

    def __init__(self, lev_a, lev_b, additional_bookmark, sequence_flag,  dimension):
        super(PI_PULSE, self).__init__(np.pi, 0, lev_a, lev_b, dimension)

        self.bookmark = additional_bookmark
        self.sequence_gate = sequence_flag


