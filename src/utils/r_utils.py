import numpy as np


###         UTILS

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



def eurlerComplex(phi, A=1):
    return A * ( np.cos(phi) + np.sin(phi)*1j )

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ todo understand if to make it class method
def rotation_cost_calc(gate, placement):
    SP_PENALTY = 1  # TODO REFINE MEASUREMENT OF PENALTY FOR SP LEVELS

    source = gate.original_lev_a
    target = gate.original_lev_b
    gate_cost = gate.cost

    if(placement.is_Sp(source) or placement.is_Sp(target)):
        theta_on_units = gate.theta / np.pi
        gate_cost = gate_cost + ( SP_PENALTY*abs(np.mod(theta_on_units+0.25, 0.5) - 0.25) )*10.0e-04

    return gate_cost
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

