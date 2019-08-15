import xarray as xr, numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


fname_vws = '/Users/serene.meng/TC/Ventilation_index/WindShear/VWS_monthly_06_to_11_2018.nc'
fname_ed = '/Users/serene.meng/TC/Ventilation_index/EntropyDeficit/ED_monthly_06_to_11_2018.nc'
fname_pi = '/Users/serene.meng/TC/Ventilation_index/PI_monthly_06_to_11_2018.nc'
ds_vws = xr.open_dataset(fname_vws)
ds_ed = xr.open_dataset(fname_ed)
ds_pi = xr.open_dataset(fname_pi)

da_vws = ds_vws.Vshear
da_ed = ds_ed.chi_m
da_pi = ds_pi.vpi

vi = da_vws*da_ed/da_pi
vip = vi.where(vi!=-np.inf,np.nan)
nt = vip.time.size


for i in range(0,nt):
    da = vip[i]
    fig = plt.figure(figsize = (12,4.9), dpi = 200)
    ax = plt.axes(projection = ccrs.PlateCarree(central_longitude = 180))
    pcm = da.plot(ax = ax, transform = ccrs.PlateCarree(),
                  norm=colors.LogNorm(vmin=0.001, vmax=1),
                  cmap='PuBu_r')
    fig.colorbar(pcm, extend='max')
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
    ofig = '/Users/serene.meng/TC/Ventilation_index//VI_' + str(da.time.values)[0:7] + '.png'
    plt.show()
    fig.savefig(ofig, figsize = (12,4.9), dpi = 200)
    plt.close('all')