# Let's calculate Potential Intensity!

## File descriptions:
**1.pcmin.f90** is a collection of five subroutines written in FORTRAN 90.
* The first four subroutines (pcmin3, pcmin3_kflag, pcmin2 and pcmin) could all be used to calculate the potential intensity (the maxium wind speed and the minimum central pressure) of a tropical cyclone. The detailed description of PI could be found [here](https://emanuel.mit.edu/limits-hurricane-intensity). 
* The fifth subroutine is CAPE, which would be called by all other subroutines in this f90 file.

**2.PI.py** is the core python script that reads `*.atmos.nc` like nc file(here I use EAR5 reanalysis data), extracts necessary variables, calculates PI and saves the results (potential intensity (m/s)) to a new `.nc` file. Detailed description could be found in this code.

**3.get_figure.py** is a python script that plot chosen variables from \*.atmos.nc like nc file, and save the figures.

## Quick Start:
Before start, you should put your data files, pcmin.f90, PI.py, get_figure.py in the same folder.<br>
**Step 1. Compile FORTRAN 90 file:**<br>
Enter the following code into your terminal:<br>
>`f2py -c pcmin.f90 -m tcpi`<br>

And you will get a `tcpi*.so file`, (e.g. `tcpi.cpython-37m-darwin.so`), which could be called in python.<br>

**Step 2. Run PI.py:**<br>
First, modify the filenames in PI.py, i.e. `fname_1`, `fname_2` and `outfile` in main().<br>
Enter the following code into your terminal:<br>
>`python /...(rootpath).../PI.py`<br>

And wait...Hopefully you will get a new `.nc` file soon includes potential intensity in wind speed form!! Yeah~<br>
My sample result is `PI_monthly_06_to_11_2018.nc`<br>

**Step 3. Plot your result:**<br>
You may wanna plot your results as well.<br>
First, modify the filename in get_figure.py, i.e.`fname` in main().<br>
Enter the following code into your terminal:<br>
>`python /...(rootpath).../get_figure.py`<br>

That's it. Good Luck!



        
        
