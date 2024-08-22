import numpy as np
import xarray as xr


def find_level_loop(A,P,levels,nlev,nsigma,sh2,t):
 
    for ilev in range(nlev):  # loop through pressure levels
        #print('Interpolating to targeted level =',levels[ilev])
        lev = levels[ilev]  # get value for the level
        Pabv = np.ones(sh2, dtype=np.float32)
        Aabv = -1 * Pabv  # Array on sigma level Above
        Abel = -1 * Pabv  # Array on sigma level Below
        Pbel = -1 * Pabv  # Pressure on sigma level Below
        Pabv = -1 * Pabv  # Pressure on sigma level Above
        Peq = np.ma.masked_equal(Pabv,-1)  # Area where Pressure == levels
        for i in range(1, nsigma):  # loop from second sigma level to last one
            a = np.ma.greater_equal(
                P[i],
                lev)  # Where is the pressure greater than lev
            b = np.ma.less_equal(
                P[i - 1],
                lev)  # Where is the pressure less than lev
            # Now looks if the pressure level is in between the 2 sigma levels
            # If yes, sets Pabv, Pbel and Aabv, Abel
            a = np.ma.logical_and(a, b)
            Pabv = xr.where(a, P[i], Pabv)  # Pressure on sigma level Above
            Aabv = xr.where(a, A[i], Aabv)  # Array on sigma level Above
            Pbel = xr.where(a, P[i - 1], Pbel)  # Pressure on sigma level Below
            Abel = xr.where(a, A[i - 1], Abel)  # Array on sigma level Below
            Peq = np.ma.where(np.ma.equal(P[i], lev), A[i], Peq)
 
        val = np.ma.masked_where(
            np.ma.equal(Pbel, -1), np.ones(Pbel.shape) * lev) # set to missing value if no data below lev if there is
 
        tl = np.log(val / Pbel) / np.log(Pabv / Pbel) * (Aabv - Abel) + Abel  # Interpolation
 
        if ((Peq.mask is None) or (Peq.mask is np.ma.nomask)):
            tl = Peq
        else:
            tl = xr.where(1 - Peq.mask, Peq, tl)
 
        t[ilev] = tl.astype(np.float32)
 
    return t

def logLinearInterpolation(A, P, levels=[100000, 92500, 85000, 70000, 60000, 50000, 40000,
                      30000, 25000, 20000, 15000, 10000, 7000, 5000,3000, 2000, 1000], axis='z'):
    """
    Converted from cdutil.logLinearRegression by Yi Qin (yi.qin@pnnl.gov).
    Description: Log-linear interpolation to convert a field from sigma levels to pressure levels.
    Values below surface are masked.
 
    :param A: array on sigma levels
    :param P: pressure field from TOP (level 0) to BOTTOM (last level)
    :param levels: pressure levels to interplate to (same units as P), default levels are:
            [100000, 92500, 85000, 70000, 60000, 50000, 40000, 30000, 25000, 20000, 15000, 10000, 7000, 5000,
            3000, 2000, 1000]

    :type levels: list
    :param axis: axis over which to do the linear interpolation
    :type axis: str
    .. note::
        P and levels must have same units
    :returns: array on pressure levels (levels)
    :Example:
        .. doctest:: vertical_logLinearInterpolation
            >>> A=logLinearInterpolation(A,P) # interpolate A using pressure field P over the default levels
    """
 
    try:
        nlev = len(levels)  # Number of pressure levels
    except BaseException:
        nlev = 1  # if only one level len(levels) would breaks
        levels = [levels, ]

    order = list(A.coords)
    lev_idx = [idim for idim,dim in enumerate(order) if 'lev' in dim]
    lev_nm = order[lev_idx[0]]
 
    # The input pressure field needs to be TOP to BOTTOM
    if P[0,-1,0,0] < P[0,0,0,0]:
        print('Reverse pressure field into TOP to BOTTOM as logLinearRegression required')
        P = P[:,::-1,:]
        A = A[:,::-1,:]

    else:
        print('Top level=',P[0,-1,0,0].values, 'Bottom level=',P[0,0,0,0].values)
 
    A = A.transpose(lev_nm,...)
    P = P.transpose(lev_nm,...)

    sh = list(P.shape)
    nsigma = sh[0]  # number of sigma levels
    sh[0] = nlev
    t = np.ma.zeros(sh, dtype=np.float32)
    sh2 = P[0].shape
    prev = -1
    t = find_level_loop(A.to_masked_array(),P.to_masked_array(),levels,nlev,nsigma,sh2,t)
    ax = A.coords
    lvl = levels

    try:
        lvl.units = P.units
    except BaseException:
        pass
    try:
        t.units = P.units
    except BaseException:
        pass
    coords = {'lev':lvl,'time':A.coords['time'], 'lat':A.coords['lat'], 'lon':A.coords['lon'],}
    t = xr.DataArray(t, coords=coords).transpose('time',lev_nm,'lat','lon')
    return t
 
