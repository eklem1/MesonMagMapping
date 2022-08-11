# MagMapping-export_TH
This code is based on Takashi Higuchi's work done on data taken in summer 2019 mapping the magnetic field in a region near where the MSR was planned to be at the time. The orginal code can be found [here](https://github.com/takashihiguchi/tucan-magnetics-mapping-export_20200129).

The orginal measurements were taken on a grid in 40 cm intervals for 3 different levels, and code was written to then interpolate this data and shift the coordinates so that z=0 was the planned center of MSL-MSR. This is all done in [ data_export.py](https://github.com/eklem1/UCN_work/blob/master/MagneticMappingPrevWork/MagMapping-export_TH/data_export.py).

I would like to use this data as a starting point for my simulations of the adiabatic paramter in the UCN guiding tubes to use in the design of the guiding fields.

However, to use this data in a [PENTrack simulation](https://github.com/eklem1/Guides_nEDMsensitivity), a different coordinate system is needed, as well as the data file needs to be in a specified format. This is currently a work in progress in [PositionCalibration.ipynb](https://github.com/eklem1/UCN_work/blob/master/MagneticMappingPrevWork/MagMapping-export_TH/PositionCalibration.ipynb).

