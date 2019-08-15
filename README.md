
# TC-Ventilation-Index
Calculate TC Ventilation Index using python.

**TC Ventilation Index** was proposed by Tang and Emanuel in [this 2012 paper.](https://journals.ametsoc.org/doi/abs/10.1175/BAMS-D-11-00165.1)<br>

From the expression of the ventilation index, we need to calculate **three parts**:<br>
>**Vertical Wind Shear**<br>
  The bulk environmental vertical wind shear between 850 and 200 hPa.<br>
>**Entropy Deficit**<br>
  The (nondimensional) entropy deficit, expression is Equation(2) in [Tang and Emanuel(2012b).](https://journals.ametsoc.org/doi/abs/10.1175/BAMS-D-11-00165.1)<br>
>**Potential Intensity**<br>
  The potential intensity of a TC is a theoretical upper bound on the maximum wind speed considering the local thermodynamic profile and gradient wind balance.<br>
The potential intensity is calculated by Equation(3) from [Bister and Emanuel (2002)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2001JD000776) under pseudoadia-batic assumptions.<br>


Here, I calculate the three parts separately and save them as three .nc files, then put them together to get the ventilation index.
