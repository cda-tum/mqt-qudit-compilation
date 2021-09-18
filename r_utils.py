
import numpy as np
from placement import distance_nodes




### not used anymore
from scipy import sparse
def phases_matrix(dim):
    diags = [[1 for x in range(dim)], [-1 for x in range(dim-1)]]
    
    ret = sparse.diags(diags, [0, -1]).toarray()
    
    return np.delete(ret, -1, axis=1)

####################

########################               UTILS

def matmul(f,s):
    dim = f.shape[1]
    rows_s = s.shape[0]
    if(dim!=rows_s):
        raise Exception('not matching dims')


    mat = [[] for x in range(dim)]
    
    for i in (range(dim)):
        for j in range(dim):
            mat[i].append(f[i,:].dot(s[:,j]))

    return np.array(mat)



def eurlerComplex(phi,A=1):
    return A * ( np.cos(phi) + np.sin(phi)*1j )
   

    
###########################################################
    
def cost_calculator(gate, placement, non_zeros):
    source = gate.lev_a
    target = gate.lev_b
    dist = distance_nodes(placement, source, target)
    
    return ( gate.cost * dist * non_zeros)

##########################################

def theta_corrector(angle):

    theta_in_units_of_pi = np.mod( (angle / np.pi), 2)
    if(theta_in_units_of_pi < 0.2):
        theta_in_units_of_pi +=  2.0

    return (theta_in_units_of_pi * np.pi)


