from netCDF4 import Dataset, MFDataset, num2date
import matplotlib.pylab as plt
import numpy as np
from matplotlib import cm
import cartopy.crs as ccrs
from cmocean import cm as cmo
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import json
import sys
import os
from cartopy.util import add_cyclic_point
import pandas as pd
import matplotlib.colors as colors
import matplotlib.patches as patches


def plot_2d_contour_by_array(fig, ax, data, lat, lon, name, units, colorbar_range):
    xticks = np.arange(0, 360, 30)
    yticks = np.arange(-90, 90, 10)


    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)

    pwd_dir = os.path.dirname(__file__)
    file_color_range=open(pwd_dir+"/colorbar_range.json")
    color_range = json.load(file_color_range)
    v = color_range[cb]

    cmap = cmo.balance

    mm = ax.contourf(lon_cyc,\
            lat,\
            data_cyc,\
            colorbar_range,\
            extend='both',\
            transform=ccrs.PlateCarree(),\
            cmap=cmap)

    ax.coastlines();
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    cbar = fig.colorbar(mm, fraction=0.018, ax=ax)
    #cbar.set_label(units, labelpad=-40, y=1.05, rotation=0)
    cbar.ax.set_title(units,fontsize=10)

    ax.set_title(name)


def plot_2d_contour_by_array_region(fig, ax, data, lat, lon, lat_rgns, lon_rgns, name, units, colorbar_range):
    xticks = np.arange(lon_rgns[0], lon_rgns[1], 30)
    yticks = np.arange(lat_rgns[0], lat_rgns[1], 30)


    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)
    ax.set_extent([lon_rgns[0],lon_rgns[1],lat_rgns[0],lat_rgns[1]], ccrs.PlateCarree())

    #pwd_dir = os.path.dirname(__file__)
    #file_color_range=open(pwd_dir+"/colorbar_range.json")
    #color_range = json.load(file_color_range)
    #v = color_range[cb]

    cmap = cmo.balance

    mm = ax.contourf(lon_cyc,\
            lat,\
            data_cyc,\
            colorbar_range,\
            extend='both',\
            transform=ccrs.PlateCarree(),\
            cmap=cmap)

    ax.coastlines();
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    cbar = fig.colorbar(mm, fraction=0.018, ax=ax)
    #cbar.set_label(units, labelpad=-40, y=1.05, rotation=0)
    cbar.ax.set_title(units,fontsize=10)

    ax.set_title(name)

def plot_2d_contour(fid, name, cb):

    lat  = fid.variables['lat'][:]
    lon  = fid.variables['lon'][:]
    data = fid.variables[name][0,:,:]
    units= fid.variables[name].units

    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)

    pwd_dir = os.path.dirname(__file__)
    file_color_range=open(pwd_dir+"/colorbar_range.json")
    color_range = json.load(file_color_range)
    v = color_range[cb]

    plt.figure(figsize=(13,6.2))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    
    mm = plt.contourf(lon_cyc,\
            lat,\
            data_cyc,\
            v,\
            extend='both',\
            transform=ccrs.PlateCarree(),\
            #cmap=cmo.dense)
            cmap=cmo.balance)

    ax.coastlines();
    ax.set_xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360], crs=ccrs.PlateCarree())
    ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    cbar = plt.colorbar(mm, shrink=.85)
    ###cbar.set_label(units, labelpad=-40, y=1.05, rotation=0)
    cbar.ax.set_title(units,fontsize=10)

    plt.title(name)
    plt.show()
    return ax

def plot_rectangle(ax, lat_bnds, lon_bnds, ecolor='r'):
    rect  = patches.Rectangle((lon_bnds[0]-180,lat_bnds[0]),lon_bnds[1]-lon_bnds[0],lat_bnds[1]-lat_bnds[0],linewidth=3,edgecolor=ecolor,facecolor='none')
    ax.add_patch(rect)

def plot_corrsig(ax, data, lat, lon, siglev):
    """ plot correlation signification

    Parameters
    ----------
    ax: axes
    data: double
    lat: double
    lon: double
    siglev: double
    
    """
    idx_2d = np.where(data < siglev)
    latsig = lat[idx_2d[0]]
    lonsig = lon[idx_2d[1]] - 180.0

    ax.scatter(lonsig, latsig, s=1,color='gray')


def plot_corrsig_only(ax, data, lat, lon, lat_rgns, lon_rgns, sigleg):
    """ plot correlation with lat and lon

    Parameters
    ----------
    ax:
    data:
    lat:
    lon:
    lat_rgns:
    lon_rgns:
    sigleg:
    """
    idx_2d = np.where(data < sigleg)
    latsig = lat[idx_2d[0]]
    lonsig = lon[idx_2d[1]] - 180.0

    ax.scatter(lonsig, latsig, s=1,color='gray')
    xticks = np.arange(lon_rgns[0], lon_rgns[1], 30)
    yticks = np.arange(lat_rgns[0], lat_rgns[1], 10)

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

def get_colorbar_range(var, name, adj=0):
    pwd_dir = os.path.dirname(__file__)
    file_color_step=open(pwd_dir+"/colorbar_step.json")
    color_step = json.load(file_color_step)
    step = color_step[name]

    a_min = int(np.min(var))
    a_max = int(np.max(var))

    c_range = np.arange(a_min, a_max+adj*step, step)
    return c_range

def plot_scatter():
    """plot_scatter"""
    s1 = 150
    a1 = 0.6
    fh = 18
    palette = plt.get_cmap('Set2')
    
    for i,icol in zip(range(len(tmp1.columns)),tmp1.columns):
        #plt.scatter(range(4),tmp1.loc[:,icol],s=s1,alpha=a1,label=icol, color=palette(i))
        plt.scatter(range(4),tmp1.loc[:,icol],s=s1,alpha=a1,label=icol)
        
    plt.tick_params(labelsize=fh) 
    plt.legend(fontsize=fh,bbox_to_anchor=(1.04,0),loc='lower left')

def plot_scatter_map(ax,data,lat,lon,lat_rgns,lon_rgns,siglev):
    ax.coastlines()
    ax.contourf(lon, lat, data, 3, colors='none',linewidth=0, hatches=['', '..'], transform=ccrs.PlateCarree())

if __name__ == '__main__':
    data_dir="/gscr3/tzhang/cause_doubleitcz/cesm/BC5_f19g16_cosp/atm/"
    flf  = Dataset(data_dir+'BC5_f19g16_cosp.cam.h0.0003-07.nc')
   
    plot_2d_contour(flf, "TS", "TEMP")
    #plt.show()
