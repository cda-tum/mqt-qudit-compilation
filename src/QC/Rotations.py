
from Gellman import *


import numpy as np

from bin.src.utils.costs_utils import theta_corrector

####################### ROTATION MATRICES
class custom_Unitary:
    
    def __init__(self, matrix, dimension):
        
        self.d=dimension
        self.matrix = matrix
        
    def cost(self):
        return np.NAN
        

class R:
    
    def __init__(self, theta, phi, lev_a, lev_b, dimension):


        self.theta = theta_corrector(theta)
        self.phi = phi
        self.lev_a = lev_a
        self.lev_b = lev_b
        self.dimension = dimension

        Identity = np.identity(dimension, dtype='complex')
        
        Identity[lev_a,lev_a] = np.cos(theta/2)*Identity[lev_a,lev_a]
        Identity[lev_b,lev_b] = np.cos(theta/2)*Identity[lev_b,lev_b]

        cosine_matrix = Identity
        
        
        
        self.matrix =  (cosine_matrix -1j*np.sin(theta/2)* 
                        ( np.sin(phi)*GellMann(lev_a,lev_b,'s',dimension).matrix - 
                          np.cos(phi)*GellMann(lev_a,lev_b,'a',dimension).matrix ) )
        
        """control if the matrix is actually correct because different from the slides of Martin, 
            but works as in example"""
        self.shape = self.matrix.shape

    @property
    def dag(self):
        return self.matrix.conj().T

    @property
    def cost(self):
        theta_on_units = self.theta/np.pi

        E = ( 4*theta_on_units + 1*abs(np.mod(theta_on_units+0.25, 0.5) - 0.25) )*10.0e-04
        return E

    def __str__(self):
        return str(self.matrix)



class Rz:
    
    def __init__(self,theta,lev, dimension):
        
        self.theta = theta_corrector(theta) # TODO DISCUSS IF THIS SHOULD GO THROUGH THE CORRECTOR
        self.lev = lev
        
        self.dimension = dimension
        
        Identity = np.identity(dimension,dtype='complex')
        
        Identity[lev,lev]= np.exp(-1j*theta)*Identity[lev,lev]
        self.matrix = Identity

        self.shape = self.matrix.shape

    def __str__(self):
        return str(self.matrix)

    @property
    def dag(self):
        return self.matrix.conj().T

    @property
    def cost(self):
        theta_on_units = self.theta / np.pi

        E = theta_on_units * 10.0e-04
        return E


class PI_PULSE(R):

    def __init__(self, lev_a, lev_b, additional_bookmark, dimension):
        super(PI_PULSE, self).__init__(np.pi, 0, lev_a, lev_b, dimension)

        self.bookmark = additional_bookmark