# Let's calculate wind shear between 200hPa and 850hPa

Calculating wind shear is quite easy though...but it worth looking at when you are interested in TC formation. Here we go!<br>

## Formula:<br>
Vshear = ( (u200-u850)\*\*2 + (v200-v850)\*\*2 )\*\*(1/2)
## Data:<br>
I use EAR5 reanalysis monthly averaged u,v data from Jun to Nov, 2018. You could get access to it [here](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels-monthly-means?tab=overview).
