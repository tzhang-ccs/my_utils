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
import matplotlib.path as mpath

def plot_2d_contourf_PlateCarree(fig, ax, data, lat, lon, lat_rgns, lon_rgns, name, units, colorbar_range, cmap = cmo.balance, alpha=1.0):
    xticks = np.arange(lon_rgns[0], lon_rgns[1]+1, 30)
    yticks = np.arange(lat_rgns[0], lat_rgns[1]+1, 30)

    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)
    ax.set_extent([lon_rgns[0],lon_rgns[1]+1,lat_rgns[0],lat_rgns[1]+1], ccrs.PlateCarree())

    #pwd_dir = os.path.dirname(__file__)
    #file_color_range=open(pwd_dir+"/colorbar_range.json")
    #color_range = json.load(file_color_range)
    #v = color_range[cb]

    #cmap = cmo.balance
    ax.coastlines();

    #cmap = "RdBu_r"
    mm = ax.contourf(lon_cyc,\
            lat,\
            data_cyc,\
            colorbar_range,\
            extend='both',\
            corner_mask=False,\
            transform=ccrs.PlateCarree(),\
            alpha = alpha,\
            cmap=cmap)

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    fh = 18
    #cbar = fig.colorbar(mm, fraction=0.018, ax=ax)
    ##cbar.set_label(units, labelpad=-40, y=1.05, rotation=0)
    #cbar.ax.set_title(units,fontsize=fh)
    #cbar.ax.tick_params(labelsize=fh)

    ax.set_title(name, fontsize=fh)
    ax.tick_params(labelsize=13)

    return fig, ax

def plot_2d_contourf(fig, ax, data, lat, lon, name, units, colorbar_range, cmap='RdBu_r', alpha=1.0):
    ax.coastlines()
    mm = ax.contourf(lon,lat,data,colorbar_range,extend='both',transform=ccrs.PlateCarree(), alpha = alpha, cmap=cmap)
    fh = 18
    cbar = fig.colorbar(mm, fraction=0.018, ax=ax)
    cbar.ax.set_title(units,fontsize=fh)
    ax.set_title(name, fontsize=fh)

    return ax

def plot_2d_contourf_PolarStereo(fig, ax, data, lat, lon, name, units, colorbar_range, cmap='RdBu_r', alpha=1.0, polar='S'):
    ax.coastlines()
    #ax.gridlines()

    #theta = np.linspace(0, 2*np.pi, 100)
    #center, radius = [0.5, 0.5], 0.5
    #verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    #circle = mpath.Path(verts * radius + center)
    #ax.set_boundary(circle, transform=ax.transAxes)

    data_cyc, lon_cyc = add_cyclic_point(data, coord=lon)
    mm = ax.contourf(lon_cyc,lat,data_cyc,colorbar_range,extend='both',transform=ccrs.PlateCarree(), alpha = alpha, cmap=cmap)
    ax.gridlines(color='lightgrey', linestyle='-', draw_labels=True)
    if polar == 'S':
        ax.set_extent([-180, 180, -90, -60], ccrs.PlateCarree())
    elif polar == 'N':
        ax.set_extent([-180, 180, 30, 90], ccrs.PlateCarree())

    ax.gridlines(color='lightgrey', linestyle='-', draw_labels=True)
    fh = 18
    cbar = fig.colorbar(mm, fraction=0.018, ax=ax)
    cbar.ax.set_title(units,fontsize=fh)
    ax.set_title(name, fontsize=fh)

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

    ax.coastlines()
    ax.scatter(lonsig, latsig, s=1,color='gray')
    xticks = np.arange(lon_rgns[0], lon_rgns[1], 30)
    yticks = np.arange(lat_rgns[0], lat_rgns[1], 30)

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)


def plot_scatter(ax, lat_rgns, lon_rgns, slat, slon, title):
    sflon = slon - 180.0

    ax.coastlines()
    ax.scatter(sflon, slat, s=1,color='gray')
    xticks = np.arange(lon_rgns[0], lon_rgns[1], 30)
    yticks = np.arange(lat_rgns[0], lat_rgns[1], 30)
    ax.set_extent([lon_rgns[0],lon_rgns[1]+1,lat_rgns[0],lat_rgns[1]+1], ccrs.PlateCarree())

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    fh = 18
    ax.set_title(title, fontsize=fh)

    return ax


def plot_scatter_map(ax,data,lat,lon,lat_rgns,lon_rgns,siglev):
    ax.coastlines()
    ax.contourf(lon, lat, data, 3, colors='none',linewidth=0, hatches=['', '..'], transform=ccrs.PlateCarree())

if __name__ == '__main__':
    data_dir="/gscr3/tzhang/cause_doubleitcz/cesm/BC5_f19g16_cosp/atm/"
    flf  = Dataset(data_dir+'BC5_f19g16_cosp.cam.h0.0003-07.nc')
   
    plot_2d_contour(flf, "TS", "TEMP")
    #plt.show()
