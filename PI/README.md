# Let's calculate Potential Intensity!

## File descriptions:
1. **pcmin.f90** is a collection of five subroutines.<br>
- The first four subroutines (pcmin3, pcmin3_kflag, pcmin2 and pcmin) could all be used to calculate the potential intensity (the maxium wind speed and the minimum central pressure) of a tropical cyclone. The detailed description of PI could be found [here](https://emanuel.mit.edu/limits-hurricane-intensity). <br>
- The fifth subroutine is CAPE, which would be called by all other subroutines in this f90 file.<br>

2. **PI.py** is the core python script that reads \*.atmos.nc like nc file, extracts necessary variables, calculates PI and saves the results to a new nc file.<br>

3. **get_figure.py** is a python script that plot chosen variables from \*.atmos.nc like nc file, and save the figures.
