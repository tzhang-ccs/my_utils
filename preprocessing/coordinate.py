import numpy as np

def latlon_slice(lats, lons, lat_bnds, lon_bnds):
    lat_inds = np.where((lats > lat_bnds[0]) & (lats < lat_bnds[1]))
    lon_inds = np.where((lons > lon_bnds[0]) & (lons < lon_bnds[1]))

    latli = lat_inds[0][0]
    latui = lat_inds[0][-1] + 1
    lonli = lon_inds[0][0]
    lonui = lon_inds[0][-1] + 1

    return latli,latui,lonli,lonui
