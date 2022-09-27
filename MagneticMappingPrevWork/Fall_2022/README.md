### Sept23_data
Data files for Mapping on top of the base with the cyclotron on, done on the afternoon of Sept 23, 2022. Files marked with \*RUN#.csv hold the grid of fluxgate data. The other file with the coorisponding colar contain fluxgate data from three static fluxgates montitoring the nearby area as we took data.

| File                        |                 | info                                                                                                                 | units                  |   |   |   |   |   |
|-----------------------------|-----------------|----------------------------------------------------------------------------------------------------------------------|------------------------|---|---|---|---|---|
| Grid of fluxgate  data file |                 |                                                                                                                      |                        |   |   |   |   |   |
|                             |    **datetime** | Date and time of data                                                                                                | format='%Y%m%d_%H%M%S' |   |   |   |   |   |
|                             | **utime_start** | Start of point data taking                                                                                           |                        |   |   |   |   |   |
|                             |   **utime_end** | End of point data taking                                                                                             |                        |   |   |   |   |   |
|                             |          **x0** | Position on grid with a hole on the board as the  origin (L) and the bottom of the pole for the  vertical origin     | $cm$                     |   |   |   |   |   |
|                             |          **dx** | Offset of position to the center of the fluxgate  and vertically to the top of the base                              | $cm$                     |   |   |   |   |   |
|                             |           **x** | Corrected position to actual position of the  fluxgate center and vertical position relative  to the top of the base | $cm$                     |   |   |   |   |   |
|                             |          **B1** | Magnetic field value  B1=Bx, B2=-Bz, B3=By                                                                           | $\mu T$                |   |   |   |   |   |
|                             |         **dB1** | Magnetic field gradient value                                                                                        | $\mu T/m$ ?             |   |   |   |   |   |
|                             |                 |                                                                                                                      |                        |   |   |   |   |   |
| static data  file           |                 |                                                                                                                      |                        |   |   |   |   |   |
|                             |    **Datetime** | Date and time of data                                                                                                | format='%Y%m%d_%H%M%S' |   |   |   |   |   |
|                             |   **UNIX_time** |                                                                                                                      |                        |   |   |   |   |   |
|                             |     **LV_time** |                                                                                                                      |                        |   |   |   |   |   |
|                             |        **FG1x** | Static fluxgate #1, 3 axis readings                                                                                  | $\muT$                 |   |   |   |   |   |
|                             |        **FG2x** | Static fluxgate #2, 3 axis readings                                                                                  | $\muT$                 |   |   |   |   |   |
|                             |        **FG3x** | Static fluxgate #3, 3 axis readings                                                                                  | $\muT$                 |   |   |   |   |   |


For offset explaination see (file on Plone)