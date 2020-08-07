import numpy as np

def get_abnorm(x):
    xnorm = x.copy()
    for i in range(12):
        xm = np.mean(x[i::12, :, :], axis=0)
        xnorm[i,:,:] = x[i,:,:] - xm
    return xnorm
