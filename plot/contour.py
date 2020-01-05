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

def plot_2d_contour_box(data, lat, lon, name):
    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)

    plt.figure(figsize=(13,6.2))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    mm = ax.pcolormesh(lon_cyc,\
                   lat,\
                   data_cyc,\
                   vmin=np.min(data_cyc),\
                   vmax=np.max(data_cyc),\
                   transform=ccrs.PlateCarree(),\
                   cmap=cmo.balance )
    ax.coastlines();
    plt.colorbar(mm)
    plt.title(name)
    plt.show()

def plot_2d_contour_by_array(data, lat, lon, name, units, cb, save_name):
    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)

    #data_cyc = data
    #lon_cyc = lon

    fig = plt.figure(figsize=(13,6.2))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    
    pwd_dir = os.path.dirname(__file__)
    file_color_range=open(pwd_dir+"/colorbar_range.json")
    color_range = json.load(file_color_range)
    v = color_range[cb]

    mm = plt.contourf(lon_cyc,\
            lat,\
            data_cyc,\
            v,\
            extend='both',\
            transform=ccrs.PlateCarree(),\
            cmap=cmo.balance)

    ax.coastlines();
    ax.set_xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360], crs=ccrs.PlateCarree())
    ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    cbar = plt.colorbar(mm, shrink=.85)
    #cbar.set_label(units, labelpad=-40, y=1.05, rotation=0)
    cbar.ax.set_title(units,fontsize=10)

    plt.title(name)

    if save_name is not None:
        plt.savefig(save_name)
    return fig,ax

def plot_2d_contour_by_array_region(data, lat, lon, name, units, cb):
    lat_min = np.min(lat)
    lat_max = np.max(lat)
    lon_min = np.min(lon)
    lon_max = np.max(lon)

    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)
    plt.figure(figsize=(13,6.2))
    ax = plt.subplot(projection=ccrs.PlateCarree(180))
    ax.set_extent([122.5, 295, -60, 60], ccrs.PlateCarree())
    #ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
    #ax.set_extent([122.5,-180, -60, 60], crs=ccrs.PlateCarree())
    print(lon_min, lon_max)

    pwd_dir = os.path.dirname(__file__)
    file_color_range=open(pwd_dir+"/colorbar_range.json")
    color_range = json.load(file_color_range)
    v = color_range[cb]

    mm = plt.contourf(lon_cyc,\
            lat,\
            data_cyc,\
            v,\
            extend='both',\
            transform=ccrs.PlateCarree(),\
            cmap=cmo.balance)

    ax.coastlines();
    ax.set_xticks([120, 150, 180, 210, 240, 270, 300], crs=ccrs.PlateCarree())
    ax.set_yticks([-60, -30, 0, 30, 60], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    cbar = plt.colorbar(mm, shrink=.85)
    #cbar.set_label(units, labelpad=-40, y=1.05, rotation=0)
    cbar.ax.set_title(units,fontsize=10)

    plt.title(name)
    return ax,mm


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


if __name__ == '__main__':
    data_dir="/gscr3/tzhang/cause_doubleitcz/cesm/BC5_f19g16_cosp/atm/"
    flf  = Dataset(data_dir+'BC5_f19g16_cosp.cam.h0.0003-07.nc')
   
    plot_2d_contour(flf, "TS", "TEMP")
    #plt.show()
