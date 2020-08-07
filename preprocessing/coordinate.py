import numpy as np
from netCDF4 import Dataset
import pdb

def latlon_slice(lats, lons, lat_bnds, lon_bnds):
    lat_inds = np.where((lats > lat_bnds[0]) & (lats < lat_bnds[1]))
    lon_inds = np.where((lons > lon_bnds[0]) & (lons < lon_bnds[1]))

    latli = lat_inds[0][0]
    latui = lat_inds[0][-1] + 1
    lonli = lon_inds[0][0]
    lonui = lon_inds[0][-1] + 1

    return latli,latui,lonli,lonui

def format_lon(data, lon):
    data_fm = np.zeros_like(data)
    lon_fm  = np.zeros_like(lon)
    
    shape = data_fm.shape

    idxsmall = np.where(lon<0)
    idxlarge = np.where(lon>=0)

    if(len(shape) == 2):
        data_fm[:,idxsmall] = data[:,idxlarge].copy()
        data_fm[:,idxlarge] = data[:,idxsmall].copy()
    if(len(shape) == 3):
        data_fm[:,:,idxsmall] = data[:,:,idxlarge].copy()
        data_fm[:,:,idxlarge] = data[:,:,idxsmall].copy()

    lon_fm[idxsmall] = lon[idxlarge].copy()
    lon_fm[idxlarge] = lon[idxsmall].copy() + 360

    return data_fm, lon_fm

def get_timeseries_files(flist,varn,lat_bnds,lon_bnds):
    ntime = len(flist)
    
    timeseries = np.empty(shape=(0))

    for f in flist:
        print("Processing "+str(f))
        fid = Dataset(f)
        varns_name = fid.variables.keys()
        if 'nlat' in varns_name:
            lat = fid.variables['nlat'][:]
        if 'latitude' in varns_name:
            lat = fid.variables['latitude'][:]
        if 'nlon' in varns_name:
            lon_tmp = fid.variables['nlon'][:]
        if 'longitude' in varns_name:
            lon_tmp = fid.variables['longitude'][:]

        data_tmp = fid.variables[varn][:]
        shape = data_tmp.shape
        if(len(shape) == 2):
            if(shape[0] > shape[1]):
                data_tmp = np.swapaxes(data_tmp,0,1)

        if(lon_tmp[0] < 0):
            data,lon=format_lon(data_tmp, lon_tmp)
        else:
            data = data_tmp
            lon  = lon_tmp

        latli,latui,lonli,lonui=latlon_slice(lat, lon, lat_bnds, lon_bnds)
        if(len(shape) == 2):
            data_reg = data[latli:latui,lonli:lonui]
            data_mean = np.mean(data_reg)
        if(len(shape) == 3):
            data_reg = data[:,latli:latui,lonli:lonui]
            data_mean = np.mean(data_reg,axis=(1,2))
        
        timeseries = np.append(timeseries,data_mean)

    return timeseries



