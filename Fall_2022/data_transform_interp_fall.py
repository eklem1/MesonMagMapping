#Emma Klemets
#Sept 2022

#############################################################
# HOW TO USE 
# This code imports the mapping data as a pandas data frame, 
# 
# 
#############################################################

### imports

import pandas as pd
import numpy as np
# get_ipython().magic(u'matplotlib notebook')
from IPython.display import display
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib import cm
from datetime import date
import scipy
import scipy.interpolate as interp
import CoordTransfFunctions_fall as ctf

#if set to False, the origin will be the MSR, and no rotation transformation will be preformed
SET_FINAL_ORIGIN_PENTRACK = False #not currently doing anything
#if True, cuts data range to compare with new data
CUT_2019 = True 
CUT_guides = False #both cuts can't be true at the same time

MergeTOGETHER = True

shifted = False
shiftAmount = 0 #cm


### Import data ###

# This data is in [cm] and [1 muT = 1e-6 T]
dfRed = pd.read_csv('Sept23_data/20220923_153158_Red_RUN1_cor.csv')
dfRed['datetime'] = pd.to_datetime(dfRed['datetime'], format='%Y%m%d_%H%M%S')

dfGreen = pd.read_csv('Sept23_data/20220923_170313_Green_RUN3_cor.csv')
dfGreen['datetime'] = pd.to_datetime(dfGreen['datetime'], format='%Y%m%d_%H%M%S')

#matching up the correct axes of the fluxgate, as it was not placed in the 
#same orientation as the coordinate system
dfRed['B_x'] = dfRed['B1']
dfRed['B_y'] = dfRed['B3']
dfRed['B_z'] = -dfRed['B2']  
dfRed.index.name = 'index'

dfRed_sub = dfRed[['x','y','z','B_x','B_y','B_z']]
print("Original red data")
ctf.Limits(dfRed_sub)

dfGreen['B_x'] = dfGreen['B1']
dfGreen['B_y'] = dfGreen['B3']
dfGreen['B_z'] = -dfGreen['B2']  
dfGreen.index.name = 'index'

dfGreen_sub = dfGreen[['x','y','z','B_x','B_y','B_z']]
print("Original green data")
ctf.Limits(dfGreen_sub)

### Re orientation ###
# All the work is done in the functions in CoordTransfFunctions.py

df_BField_data_fixed_red, off_sets, rotation, off_setwithRotation, data_total = ctf.FixOffset(dfRed_sub, plot=False, alpha=.5, POSITION='red')
df_BField_data_fixed_green, off_sets, rotation, off_setwithRotation, data_total = ctf.FixOffset(dfGreen_sub, plot=False, alpha=.5, POSITION='green')

print("Transformed data")
#prints out the limits of the transformed data, in position and strength of the B field
ctf.Limits(df_BField_data_fixed_red)

### Add data together ### do here?
# Now the properly orientated data can be combined

df_BField_data_tryTogether = df_BField_data_fixed_red.append(df_BField_data_fixed_green) 

### Interpolation ###

# copied from plot_simple_cut_horizontal.py for interpolation



df_BField_data_fixed = pd.DataFrame()

if MergeTOGETHER: #interpolating the two sets together
    dataSets = [df_BField_data_tryTogether]
else: # for adding together after interpolation
    dataSets = [df_BField_data_fixed_red, df_BField_data_fixed_green]

for df_data in dataSets:

    # a rough idea of the area that the guides pass through
    guidesLims = np.array([[-31, 31], [-325, 0], [-34, 34]]) #cm

    #these match our best guess at matching up with the 2019 data
    # compare_2019_cut = np.array([[-90.1, 123.60939], [-174.71133, -94.61279 ], [-150.75165, 9.257800000000003]]) #cm
    compare_2019_cut = np.array([[-90.1, 123.60939], [-174.71133, -94.61279 ], [-150.75165, 9.257800000000003]]) #cm


    #setting the limits of the interpolated data, but still uses just the data's limits if those are smaller, 
    #so as not to extrapolate data
    if CUT_2019:
        # x_min = max(min(df_data.x), compare_2019_cut[0][0])
        # x_max = min(max(df_data.x), compare_2019_cut[0][1])
        # y_min = max(min(df_data.y), compare_2019_cut[1][0])
        # y_max = min(max(df_data.y), compare_2019_cut[1][1])
        # z_min = max(min(df_data.z), compare_2019_cut[2][0])
        # z_max = min(max(df_data.z), compare_2019_cut[2][1])
        x_min, x_max = compare_2019_cut[0]
        y_min, y_max = compare_2019_cut[1]
        z_min, z_max = compare_2019_cut[2]

        print("Cut data for comparing to 2019 data")

    elif CUT_guides:
        x_min = max(min(df_data.x), guidesLims[0][0])
        x_max = min(max(df_data.x), guidesLims[0][1])
        y_min = max(min(df_data.y), guidesLims[1][0])
        y_max = min(max(df_data.y), guidesLims[1][1])
        z_min = max(min(df_data.z), guidesLims[2][0])
        z_max = min(max(df_data.z), guidesLims[2][1])
        print("Cut data for guide area")
    else: #just use limits of the data
        x_min, x_max= np.min(df_data.x), np.max(df_data.x)
        z_min, z_max= np.min(df_data.z), np.max(df_data.z)
        y_min, y_max= np.min(df_data.y), np.max(df_data.y)

    NL = 50 # this defines the number of points for interpolation, default is 50

    x_dense, z_dense, y_dense = np.meshgrid(np.linspace(x_min, x_max, NL), np.linspace(z_min, z_max, NL), np.linspace(y_min,y_max, NL))

    #could make a version with arange instead which might make the shifting possible
    # di = 0.5
    # x_dense, z_dense, y_dense = np.meshgrid(np.arange(x_min, x_max, di), np.arange(z_min, z_max, di), np.arange(y_min,y_max, di))


    Bx_rbf = interp.Rbf(df_data.x, df_data.z, df_data.y, df_data.B_x, function='cubic', smooth=0)  # default smooth=0 for interpolation
    Bx_dense = Bx_rbf(x_dense, z_dense, y_dense)  # not really a function, but a callable class instance

    Bz_rbf = interp.Rbf(df_data.x, df_data.z, df_data.y, df_data.B_z, function='cubic', smooth=0)  # default smooth=0 for interpolation
    Bz_dense = Bz_rbf(x_dense, z_dense, y_dense)  # not really a function, but a callable class instance

    By_rbf = interp.Rbf(df_data.x, df_data.z, df_data.y, df_data.B_y, function='cubic', smooth=0)  # default smooth=0 for interpolation
    By_dense = By_rbf(x_dense, z_dense, y_dense)  # not really a function, but a callable class instance

    NT = np.product(y_dense.shape)

    data = {
        "x": np.reshape(x_dense,NT),
        # "x": np.ones(NT)*x_cut,
        "y": np.reshape(y_dense,NT),
        "z": np.reshape(z_dense,NT),
        "B_x": np.reshape(Bx_dense, NT),
        "B_y": np.reshape(By_dense, NT),
        "B_z": np.reshape(Bz_dense, NT),
    }

    df_all_intr = pd.DataFrame(data, columns=['x','y','z','B_x','B_y','B_z'])
    df_all_intr.index.name = 'index'

    # display(df_all_intr)

    print("Interpolated data")
    ctf.Limits(df_all_intr)

    # Add data together
    df_BField_data_fixed = df_BField_data_fixed.append(df_all_intr)


### Add data together ### or do here?
# Now the properly orientated data can be combined?

data_interp = data_total.copy()
data_interp[2] = df_BField_data_fixed


# plotting to check

fig = plt.figure(figsize=(11, 5))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')

ctf.plotMapping(ax1, data_interp, title="MSR origin, interpolated", view=4, txtSize='x-small')
B1 = np.sqrt(data_interp[2]['B_x']**2 + data_interp[2]['B_y']**2 + data_interp[2]['B_z']**2 )#muT
Q = ax1.scatter(data_interp[2]['x'], data_interp[2]['y'], data_interp[2]['z'],c=B1, s=1, alpha=1, cmap=cm.plasma)

cbar = fig.colorbar(Q, label='$\mathsf{|B|\,(\mu T)}$')
plt.subplots_adjust(wspace=0.0)
plt.show()


### Save to txt file for PENTrack ###

BField_data_fixed = data_interp[2].to_numpy()
BField_Names = data_interp[2].columns

comment = "This data is interpolated from Emma & Takashi's fall 2022 data. The data has been shifted"+\
        " so the MSR is the origin, as well as interpolated. It is also cut to match "

file = 'original data'

headerText = f'File: {file}\n' + f'Date created: {date.today().strftime("%d/%m/%Y")}\n'\
    + 'Units: [cm], [1e-6 T]\n' +f'Offset from original data used: {off_sets} cm\n + \nRotation about z axis: '\
    + f'{rotation} degrees\n' + f'Resulting total origin shift: {off_setwithRotation} cm\n'\
    + f'Comments: {comment}\n' + '\t'.join(BField_Names)

#putting together a nice name for the file
file_save = f"map_referencedMSR_fall2022"

if MergeTOGETHER: #interpolating the two sets together
    file_save = file_save + "_together"
else: # for adding together after interpolation
    file_save = file_save + "_seperate"

if CUT_2019:
    file_save = file_save + "_CUT2019"
if CUT_guides:
    file_save = file_save + "_CUTGuides"

if shifted: #this is data for testing if our transformations are off
    file_save = "shifted/"+ file_save + f"{shiftAmount}"


file_save = file_save + f"_interp{NL}"

print(f"Saving file: ./data_export/{file_save}.txt")

np.savetxt(f'./data_export/{file_save}.txt', BField_data_fixed,  delimiter='\t', newline='\n', header=headerText)
