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

def plot_2d_contour_by_array(fig, ax, data, lat, lon, name, units, cb, save_name=None):
    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)

    #data_cyc = data
    #lon_cyc = lon

    #fig = plt.figure(figsize=(13,6.2))
    #ax = sub_ax.axes(projection=ccrs.PlateCarree(central_longitude=180))
    
    pwd_dir = os.path.dirname(__file__)
    file_color_range=open(pwd_dir+"/colorbar_range.json")
    color_range = json.load(file_color_range)
    v = color_range[cb]

    mm = ax.contourf(lon_cyc,\
            lat,\
            data_cyc,\
            v,\
            extend='both',\
            transform=ccrs.PlateCarree(),\
            cmap=cmo.balance)



    ax.coastlines();
    if str(ax.projection).split(' ')[0].split('.')[2] != 'Robinson':
        ax.set_xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360], crs=ccrs.PlateCarree())
        ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
        lon_formatter = LongitudeFormatter(zero_direction_label=False)
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)

    #cbar = fig.colorbar(mm, shrink=.85, ax=ax)
    cbar = fig.colorbar(mm, fraction=0.02, ax=ax)
    #cbar.set_label(units, labelpad=-40, y=1.05, rotation=0)
    cbar.ax.set_title(units,fontsize=10)

    ax.set_title(name)

    if save_name is not None:
        plt.savefig(save_name)

def plot_2d_contour_by_array_region(fig, ax, data, lat, lon, lat_rgns, lon_rgns, name, units, cb):
    xticks = np.arange(lon_rgns[0], lon_rgns[1], 30)
    yticks = np.arange(lat_rgns[0], lat_rgns[1], 10)


    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)
    ax.set_extent([lon_rgns[0],lon_rgns[1],lat_rgns[0],lat_rgns[1]], ccrs.PlateCarree())

    pwd_dir = os.path.dirname(__file__)
    file_color_range=open(pwd_dir+"/colorbar_range.json")
    color_range = json.load(file_color_range)
    v = color_range[cb]

    mm = ax.contourf(lon_cyc,\
            lat,\
            data_cyc,\
            v,\
            extend='both',\
            transform=ccrs.PlateCarree(),\
            cmap=cmo.balance)

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


if __name__ == '__main__':
    data_dir="/gscr3/tzhang/cause_doubleitcz/cesm/BC5_f19g16_cosp/atm/"
    flf  = Dataset(data_dir+'BC5_f19g16_cosp.cam.h0.0003-07.nc')
   
    plot_2d_contour(flf, "TS", "TEMP")
    #plt.show()
