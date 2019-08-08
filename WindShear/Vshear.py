import numpy as np, xarray as xr
from get_figure import getfig

def get_vshear(fname):
    ds = xr.open_dataset(fname)
    u, v = ds['u'], ds['v']
    Vshear = ( (u.interp(level=200) - u.interp(level=850))**2
        + (v.interp(level=200) - v.interp(level=850))**2 )**0.5
    
    Vshear.attrs['long_name'] = 'vertical wind shear between 200hPa and 850hPa'
    Vshear.attrs['units'] = 'm/s'
    
    return Vshear


def main():
    fname = '/Users/serene.meng/TC/Ventilation_index/WindShear/U_V_850_200_monthly_06_to_11_2018.nc'
    vs = get_vshear(fname)
    nt = vs.time.size
    
    for i in range(0,nt):
        da = vs[i]
        ofig = '/Users/serene.meng/TC/Ventilation_index/WindShear/VShear_' + str(da.time.values)[0:7] + '.png'
        getfig(da, ofig, 0, 60)

if __name__ == '__main__':
    main()

    


