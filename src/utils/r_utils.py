import numpy as np


############          UTILS

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
   

    

