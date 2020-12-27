import numpy as np
import MV2 as MV
from statsmodels.tsa.tsatools import detrend

def calc_anorm_stddata(data, data_cut):
    data_anorm = np.zeros_like(data)
    
    for i in range(12):
        data_climo = MV.average(data_cut[i::12,:,:], axis=0)
        data_anorm[i::12,:,:] = data[i::12,:,:] - data_climo
        
    return data_anorm

def calc_detrend(data):
    nlat = data.shape[1]
    nlon = data.shape[2]
    
    data_detrend = np.zeros_like(data)
    for i in range(nlat):
        for j in range(nlon):
            data_detrend[:,i,j] = detrend(data[:,i,j],order=2)
            
    return data_detrend


