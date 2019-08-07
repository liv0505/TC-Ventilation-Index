from tcpi import pcmin, pcmin2, pcmin3, pcmin3_kflag, cape
import numpy as np, xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, savefig
import matplotlib.colors
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


fname_1 = '/Users/serene.meng/TC/Ventilation_index/PI/SST_SLP_monthly_06_to_11_2018.nc'
fname_2 = '/Users/serene.meng/TC/Ventilation_index/PI/T_SH_monthly_06_to_11_2018.nc'
ds_1 = xr.open_dataset(fname_1)
ds_2 = xr.open_dataset(fname_2)
sst = ds_1['sst']
slp = ds_1['sp']
plevel = ds_2.level
temp = ds_2['t']
qq = ds_2['q']

plevel = plevel.isel(level=slice(-1,None,-1))    
temp = temp.isel(level=slice(-1, None, -1))
qq = qq.isel(level=slice(-1, None, -1))

nt, nlat, nlon, nlevel = ds_2.time.size, ds_2.latitude.size, ds_2.longitude.size, ds_2.level.size

vpi = np.zeros((nt,nlat,nlon))

for i in range(0,nt):
    pmin, vmax, ifl = pcmin3_kflag(sst.isel(time=i).values,
                                   slp.isel(time=i).values,
                                   plevel.values,
                                   temp.isel(time=i).values,
                                   qq.isel(time=i).values,
                                   nlat, nlon, nlevel)
    vpi[i, :, :] = vmax
    
vpi = xr.DataArray(vpi,
                   dims = ('time','latitude','longitude'),
                   coords=(ds_2.time, ds_2.latitude.values, ds_2.longitude.values),
                   attrs=dict(long_name='Potential Intensity', units='m/s')
                   )

norm = matplotlib.colors.Normalize(vmin = 0, vmax = 130)


fig = plt.figure(figsize = (12,4.9), dpi = 300)

ax = plt.axes(projection = ccrs.PlateCarree(central_longitude = 180))

contour = vpi[0].plot(ax = ax, transform = ccrs.PlateCarree(), 
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

plt.show()
fig.savefig('/Users/serene.meng/TC/Ventilation_index/PI/PI_old/PI_06_2018.png', figsize = (12,4.9), dpi = 300)
