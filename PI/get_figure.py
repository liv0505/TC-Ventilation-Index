import numpy as np, xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, savefig
import matplotlib.colors
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def getfig(da, ofig):

    norm = matplotlib.colors.Normalize(vmin = 0, vmax = 130)
    fig = plt.figure(figsize = (12,4.9), dpi = 200)
    ax = plt.axes(projection = ccrs.PlateCarree(central_longitude = 180))
    contour = da.plot(ax = ax, transform = ccrs.PlateCarree(),
                   #cmap = 'Blues',
                   norm = norm,
                   linewidth = 0, antialiased = False)

    ax.set_global()
    gl = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels=True, alpha=0.5, linewidth = 0.1, color = 'gray')
    ax.coastlines(linewidth = 0.3)
    #ax.set_title('The variance of 3-10 day bandpass filtered 850hPa vorticity')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlocator = mticker.FixedLocator([-180,-135,-90, -45, 0, 45, 90, 135])
    gl.ylocator = mticker.FixedLocator([-90,-60,-30, 0, 30, 60, 90])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 10, 'color': 'gray'}
    gl.ylabel_style = {'size': 10,'color': 'gray'}

    #plt.show()
    fig.savefig(ofig, figsize = (12,4.9), dpi = 200)


def main():
    fname = '/Users/serene.meng/TC/Ventilation_index/PI_monthly_06_to_11_2018.nc'
    ds = xr.open_dataset(fname)

    nt = ds.time.size
    for i in range(0,nt):
        da = ds.isel(time = i)['vpi']
        ofig = '/Users/serene.meng/TC/Ventilation_index/PI/PI_' + str(da.time.values)[0:7] + '.png'
        getfig(da, ofig)

if __name__ == '__main__':
    main()
