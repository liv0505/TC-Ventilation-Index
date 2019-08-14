import numpy as np, xarray as xr


def get_endfc(fname_sl, fname_pl, ofile=True):
    '''
    Calculate Entropy deficit chi_m defined by Tang and Emanuel (2012b)
    Save the result in form of Xarray.Dataset to an nc file.

    Link: https://journals.ametsoc.org/doi/full/10.1175/BAMS-D-11-00165.1

    Input:
    1. fname_sl: ERA5 data on single levels of SST(K) and Sea Level Pressure(Pa).
    2. fname_pl: ERA5 data on pressure levels of Temperature(K), Specific Humidity(kg kg**-1) and relative humidity (%)
    3. ofile = whether or not save the result as .nc file.
    '''
    cp = 1005.7 # specific heat at constant pressure for dry air (J * kg^-1* k^-1)
    rd = 287.05 # gas constant for dry air (J * kg^-1 * k^-1)
    rv = 461.51 # gas constant for water vapor (J * kg^-1 * k^-1)
    lv = 2.555e6 # latent heat of vaporization (J * kg^-1)


    ds_1 = xr.open_dataset(fname_sl)
    ds_2 = xr.open_dataset(fname_pl)

    sst = ds_1['sst'] # k
    sstc = sst - 273.15 # °C
    slp = ds_1['sp'] # Pa

    rh = ds_2['r']
    q = ds_2['q']
    tk = ds_2['t'] # temperatures (k)
    tc = tk - 273.15 # temperatures (°C)

    #nt, nlat, nlon, nlevel = ds_2.time.size, ds_2.latitude.size, ds_2.longitude.size, ds_2.level.size

    # ------------------------------------
    # Saturation moist entropy at sea surface temperature
    e_surf_sat = 610.94*np.exp((17.625*sstc)/(243.04+sstc)) # saturated vapor pressure at SST (Pa)
    mr_surf_sat = 0.622*e_surf_sat/(slp-e_surf_sat) # saturated mixing ratio at SST
    s_surf_sat = cp*np.log(sst)-rd*np.log(slp-e_surf_sat)+lv*mr_surf_sat/sst # J * kg^-1* k^-1

    # ------------------------------------
    # Moist entropy for boundary layer (950 hPa)
    tk_bl = tk.isel(level=1) # temperature at 950hPa (k)
    tc_bl = tc.isel(level=1) # temperature at 950hPa (°C)
    p_bl = tc.level.values[1]*100.0 # 95000 Pa
    q_bl = q.isel(level=1)
    e_bl_sat = 610.94*np.exp((17.625*tc_bl)/(243.04+tc_bl)) # saturated vapor pressure for boundary layer (Pa)
    rh_bl = rh.isel(level=1)*0.01 # relative humidity for boundary layer
    e_bl = e_bl_sat*rh_bl # vapor pressure for boundary layer (Pa)
    mr_bl = 0.622*e_bl/(p_bl-e_bl) # mixing ratio for boundary layer
    #mr_bl = q_bl/(1-q_bl)
    s_bl = cp*np.log(tk_bl)-rd*np.log(p_bl-e_bl)+lv*mr_bl/tk_bl-rv*mr_bl*np.log(rh_bl) # J * kg^-1* k^-1

    # ------------------------------------
    # Saturation moist entropy at mid-level (600hPa) in the inner core of the TC
    tk_m = tk.isel(level=0) # temperature at mid-level (k)
    tc_m = tc.isel(level=0) # temperature at mid-level (°C)
    p_m = tc.level.values[0]*100 # 60000 Pa
    e_m_sat = 610.94*np.exp((17.625*tc_m)/(243.04+tc_m)) # saturated vapor pressure at mid-level (Pa)
    mr_m_sat = 0.622*e_m_sat/(p_m-e_m_sat) # saturated mixing ratio for boundary layer
    s_m_sat = cp*np.log(tk_m)-rd*np.log(p_m-e_m_sat)+lv*mr_m_sat/tk_m # J * kg^-1* k^-1

    # ------------------------------------
    # Moist entropy at mid-level (600hPa) in the environment
    q_m = q.isel(level=0)
    rh_m = rh.isel(level=0)*0.01 # relative humidity for mid-level
    e_m = e_m_sat*rh_m # vapor pressure for mid-level (Pa)
    mr_m = 0.622*e_m/(p_m-e_m) # mixing ratio for mid-level
    #mr_m = q_m/(1-q_m)
    s_m = cp*np.log(tk_m)-rd*np.log(p_m-e_m)+lv*mr_m/tk_m-rv*mr_m*np.log(rh_m) # J * kg^-1* k^-1

    # ------------------------------------
    # Entropy deficit
    chi_m = (s_m_sat-s_m)/(s_surf_sat-s_bl)

    # wrap into an xarray.DataArray
    chi_m = xr.DataArray(chi_m,
                   attrs=dict(long_name='Entropy Deficit', units='J * kg^-1* k^-1')
                   )
    # wrap into an xarray.Dataset
    ds = xr.Dataset(dict(chi_m = chi_m),
                    attrs={'chi_m':'Entropy Deficit'})

    if ofile is None:
        return ds
    else: # save ds to ofile
        nc_dtype = {'dtype': 'float32'}
        encoding = dict(chi_m = nc_dtype)
        ds.to_netcdf(ofile, encoding=encoding, unlimited_dims='time')


def main():
    fname_sl = '/Users/serene.meng/TC/Ventilation_index/EntropyDeficit/SST_SLP_monthly_06_to_11_2018.nc'
    fname_pl = '/Users/serene.meng/TC/Ventilation_index/EntropyDeficit/rh_q_T_6009509751000_monthly_06_to_11_2018.nc'
    outfile = '/Users/serene.meng/TC/Ventilation_index/EntropyDeficit/ED_monthly_06_to_11_2018.nc'
    get_endfc(fname_sl,fname_pl,ofile = outfile)


if __name__ == '__main__':
    main()
