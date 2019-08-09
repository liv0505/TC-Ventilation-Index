from tcpi import pcmin, pcmin3_kflag, cape
import numpy as np, xarray as xr

def get_pi(fname_sl, fname_pl, ofile=True, reverse_p=True):
    '''
    Calculate Potential Intensity on EAR5 reanalysis data by calling pcmin.f90 fortran subroutine.
    Link:

    Input:
    1. fname_sl: ERA5 data on single levels of SST(K) and Sea Level Pressure(Pa).
    2. fname_pl: ERA5 data on pressure levels of Temperature(K) and Specific Humidity(kg kg**-1).
    3. ofile = whether or not save the result as .nc file.
    4. ofigure = whether or not show and save the figures.
    5. reverse_p:
    '''
    ds_1 = xr.open_dataset(fname_sl)
    ds_2 = xr.open_dataset(fname_pl)

    # variables needed: sst, slp, plevel(p levels), temp(3D temperature), qq(3D specific humidity)
    sst = ds_1['sst'] # xarray.DataArray'sst': (time, latitude, longitude), units: K
    slp = ds_1['sp'] # xarray.DataArray'sp': (time, latitude, longitude), units: Pa
    plevel = ds_2.level # xarray.DataArray'level': (level), units: mb
    temp = ds_2['t'] # xarray.DataArray't': (time, level, latitude, longitude), units: K
    qq = ds_2['q'] # xarray.DataArray'q': (time, level, latitude, longitude), units: kg kg**-1

    if reverse_p:
        # In pcmin.f90, the arrays MUST be arranged with increasing index corresponding to decreasing pressure.
        plevel = plevel.isel(level=slice(-1,None,-1))
        temp = temp.isel(level=slice(-1, None, -1))
        qq = qq.isel(level=slice(-1, None, -1))

    nt, nlat, nlon, nlevel = ds_2.time.size, ds_2.latitude.size, ds_2.longitude.size, ds_2.level.size

    # vpi: potential intensity
    vpi = np.zeros((nt,nlat,nlon))
    for i in range(0,nt):
        pmin, vmax, ifl = pcmin3_kflag(sst.isel(time=i).values,
                                   slp.isel(time=i).values,
                                   plevel.values,
                                   temp.isel(time=i).values,
                                   qq.isel(time=i).values,
                                   nlat, nlon, nlevel)
        vpi[i, :, :] = vmax
    # wrap into an xarray.DataArray
    vpi = xr.DataArray(vpi,
                   dims = ('time','latitude','longitude'),
                   coords=(ds_2.time, ds_2.latitude.values, ds_2.longitude.values),
                   attrs=dict(long_name='Potential Intensity', units='m/s')
                   )
    # wrap into an xarray.open_dataset
    ds = xr.Dataset(dict(vpi = vpi),
                    attrs={'vpi':'The surface wind speed upper limit for hurricanes'})

    if ofile is None:
        return ds
    else: # save ds to ofile
        nc_dtype = {'dtype': 'float32'}
        encoding = dict(vpi=nc_dtype)
        ds.to_netcdf(ofile, encoding=encoding, unlimited_dims='time')


def main():
    fname_1 = '/Users/serene.meng/TC/Ventilation_index/SST_SLP_monthly_06_to_11_2018.nc'
    fname_2 = '/Users/serene.meng/TC/Ventilation_index/T_SH_monthly_06_to_11_2018.nc'
    outfile = '/Users/serene.meng/TC/Ventilation_index/PI_monthly_06_to_11_2018.nc'
    get_pi(fname_1, fname_2, ofile=outfile, reverse_p=True)



if __name__ == '__main__':
    main()
