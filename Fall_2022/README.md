Data files for Mapping on top of the base with the cyclotron on, done from Sept 23 - 27th, 2022. Files marked with \*RUN#.csv hold the grid of fluxgate data. The other file with the corresponding color contain fluxgate data from three static fluxgates montitoring the nearby area as we took data. All distances are in $cm$, and magnetic field readings are in $\mu T$.
      
## Files
#### Data runs
20220923_153158_Red_RUN1.csv - data for red plywood placement  
20220923_153158_Red_RUN1_cor.csv - data for red plywood placement with corrected offsets for L' as origin  
20220923_170313_Green_RUN3.csv - data for green plywood placement  
20220923_170313_Green_RUN3_cor.csv - data for green plywood placement with corrected offsets for L as origin  
20220926_164800_RUN5.csv - data on the top of the stairs  
20220926_164800_RUN5_cor.csv - data on the top of the stairs with corrected offsets for Tony's mark on stair face as origin   

#### Static fluxgate background monitoring files
20220923_153207_Red.csv - for Red_RUN1  
20220923_165751_Green.csv - for Green_RUN3  
20220926_160856_platform_RUN5.csv - for RUN5  
20220926_144129_Green_RUN4 - for test run Green_RUN4  
20220923_172912_weekend.csv - left running over the weekend  
20220926_173701_after_mapping.csv - left running after Monday data taking  

#### Test runs
20220926_144410_Green_RUN4.csv - test data for green plywood placement  

## Data file formating

| File                        |                 | info                                                                                                                 | units                  |   
|-----------------------------|-----------------|----------------------------------------------------------------------------------------------------------------------|------------------------|
| Grid of fluxgate  data file |                 |                                                                                                                      |                        |   |   |   |   |   |
|                             |    **datetime** | Date and time of data                                                                                                | format='%Y%m%d_%H%M%S' |
|                             | **utime_start** | Start of point data taking                                                                                           |                        |
|                             |   **utime_end** | End of point data taking                                                                                             |                        |
|                             |          **x0** | Position on grid with a hole on the board as the  origin (L) and the bottom of the pole for the  vertical origin     | $cm$                     |
|                             |          **dx** | Offset of position to the center of the fluxgate  and vertically to the top of the base                              | $cm$                     |
|                             |           **x** | Corrected position to actual position of the  fluxgate center and vertical position relative  to the top of the base | $cm$                     |
|                             |          **B1** | Magnetic field value  B1=Bx, B2=-Bz, B3=By                                                                           | $\mu T$                |
|                             |         **dB1** | Magnetic field gradient value                                                                                        | $\mu T/m$ ?             |
|                             |                 |                                                                                                                      |                        |
| static data  file           |                 |                                                                                                                      |                        |
|                             |    **Datetime** | Date and time of data                                                                                                | format='%Y%m%d_%H%M%S' |
|                             |   **UNIX_time** |                                                                                                                      |                        |
|                             |     **LV_time** |                                                                                                                      |                        |
|                             |        **FG1x** | Static fluxgate #1, 3 axis readings                                                                                  | $\mu T$                 |
|                             |        **FG2x** | Static fluxgate #2, 3 axis readings                                                                                  | $\mu T$                 |
|                             |        **FG3x** | Static fluxgate #3, 3 axis readings                                                                                  | $\mu T$                 |

## Offsets
For offset explaination see (file on Plone)
 - the offset for y and z are incorrect in the original files, so new files were made, marked with \_cor in the file title with the corrected offsets.