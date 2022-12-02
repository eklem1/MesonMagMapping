#Emma Klemets
#Aug 2022

#############################################################
# HOW TO USE 
# This code imports the mapping data as a pandas data frame, 
# rotates and shifts the data before interpolating for a given
# range and setting the edges of the region outside where data
# was taken to 0
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
import CoordTransfFunctions as ctf


### Import data ###

#if True, cuts data range to compare with new data
CUT = True 

# This data is in [cm] and [0.1 mT = 1e-4 T = 1 G]
df1 = pd.read_csv('Mapping_0809_RUN1.csv')
df2 = pd.read_csv('Mapping_0809_RUN2.csv')
df3 = pd.read_csv('Mapping_0809_RUN3.csv')
df4 = pd.read_csv('Mapping_0809_RUN4.csv')

df_all0 = df1.append(df2)
df_all1  = df_all0.append(df3)
df_all  = df_all1.append(df4)

df_all['x'] = - df_all.u + 10.25
df_all['y'] = -df_all.w
df_all['z'] = df_all.v -1.25 + 188.1 -275 #-> sets z = 0 to the center of the MSR 
# -1.25cm accounts for the position of the sensing center of the probe and the marker on the probe. 
# + 188.1cm: from z=0 of the measurement to the floor, -275cm: from the floor to the planned center of MSR
# df_all['z'] = df_all.v -1.25 ## previous version

df_all['B_x'] = -df_all['B_u']
df_all['B_y'] = -df_all['B_w']
df_all['B_z'] = -df_all['B_v']  


u_max = np.max(df_all.u)
v_max = np.max(df_all.v)
w_max = np.max(df_all.w)
u_min = np.min(df_all.u)
v_min = np.min(df_all.v)
w_min = np.min(df_all.w)

x_max = np.max(df_all.x)
z_max = np.max(df_all.z)
y_max = np.max(df_all.y)
x_min = np.min(df_all.x)
z_min = np.min(df_all.z)
y_min = np.min(df_all.y)

v_all = df_all.v.unique()
w_all = df_all.w.unique()
u_all = df_all.u.unique()

z_all = df_all.z.unique()
y_all = df_all.y.unique()
x_all = df_all.x.unique()

# ### Make a cut with x=const., select the range of z, interpolate the subset of data - not doing this, just setting the 
# x cut to the min/max value

x_cut_min = np.min(x_all)
x_cut_max = np.max(x_all)
y_cut_min = np.min(y_all)
y_cut_max = np.max(y_all)
z_cut_min = np.min(z_all)
z_cut_max = np.max(z_all)


df_all_sub = df_all[(df_all.x <= x_cut_max) & (df_all.x >= x_cut_min)
                    & (df_all.y <= y_cut_max) & (df_all.y >= y_cut_min)
                    & (df_all.z <= z_cut_max) & (df_all.z >= z_cut_min)] # select the subset of the data frame

# print(df_all_sub.index.size)
df_all_sub.index.name = 'index'

df_all_sub = df_all_sub[['x','y','z','B_x','B_y','B_z']]

print("Original data")
ctf.Limits(df_all_sub)

### Re orientation ###
# All the work is done in the functions in CoordTransfFunctions.py


df_BField_data_fixed, off_sets, rotation, off_setwithRotation, data_total = ctf.FixOffset(df_all_sub, plot=False, alpha=.5, PEN_origin=False)


print("Transformed data")
#prints out the limits of the transformed data, in position and strength of the B field
ctf.Limits(df_BField_data_fixed)

#conversion to muT - if you want it
df_BField_data_fixed['B_x'] = df_BField_data_fixed['B_x'] * 100
df_BField_data_fixed['B_y'] = df_BField_data_fixed['B_y'] * 100
df_BField_data_fixed['B_z'] = df_BField_data_fixed['B_z'] * 100


### Shifting data ###
#this is where we will do a bunch of shifts of the data to comapare which one works the best
# [{x_shift},{y_shift}]

# x_shift_arr = np.linspace(-120, 120, 8) #cm
# y_shift_arr = np.linspace(-120, 120, 8) #cm

x_shift_arr = np.linspace(-40, 30, 5) #cm
y_shift_arr = np.linspace(-30, 40, 5) #cm

saveLimits = []

print(x_shift_arr, y_shift_arr)

for x_shift in x_shift_arr:
    for y_shift in y_shift_arr:

        df_data_shift_copy = df_BField_data_fixed.copy()

        df_data_shift_copy.x += x_shift
        df_data_shift_copy.y += y_shift

        ### Interpolation ###

        # copied from plot_simple_cut_horizontal.py for interpolation
        if CUT: #setting the limits of the interpolated data
            # x_min, x_max = -90.1, 123.60939 
            # y_min, y_max = -174.71133, -94.61279 
            # z_min, z_max = -150.75165, 9.257800000000003

            # print("2019 limits:")
            mins_19 = np.min(df_data_shift_copy, axis=0).values
            max_19 = np.max(df_data_shift_copy,axis=0).values

            print("2022 limits:")
            mins_22 = np.array([-118.9572  ,   -174.71133  ,  -150.75165  ,  -105.02902915, -108.11342154, -276.1794207 ])
            max_22 = np.array([ 123.60939  ,   -94.61279  ,     9.2578  ,      5.14 ,       -28.79225841, -160.99588885])

            whichMin = mins_19 > mins_22
            whichMax = max_19 < max_22

            minsAll = np.concatenate(( mins_19[whichMin], mins_22[~whichMin]))
            maxsAll = np.concatenate(( max_19[whichMax], max_22[~whichMax]))

            print(  f"x_min, x_max = {minsAll[0]}, {maxsAll[0]} \n" +
                f"y_min, y_max = {minsAll[1]}, {maxsAll[1]} \n"+
                f"z_min, z_max = {minsAll[2]}, {maxsAll[2]}")

            x_min, x_max = minsAll[0], maxsAll[0]
            y_min, y_max = minsAll[1], maxsAll[1]
            z_min, z_max = minsAll[2], maxsAll[2]

            saveLimits.append(minsAll)

            print("Cut data")
        else:
            x_min, x_max= np.min(df_data_shift_copy.x), np.max(df_data_shift_copy.x)
            z_min, z_max= np.min(df_data_shift_copy.z), np.max(df_data_shift_copy.z)
            y_min, y_max= np.min(df_data_shift_copy.y), np.max(df_data_shift_copy.y)

        NL = 50 # this defines the number of points for interpolation, default is 50

        x_dense, z_dense, y_dense = np.meshgrid(np.linspace(x_min, x_max, NL), np.linspace(z_min, z_max, NL), np.linspace(y_min,y_max, NL))

        Bx_rbf = interp.Rbf(df_data_shift_copy.x, df_data_shift_copy.z, df_data_shift_copy.y, df_data_shift_copy.B_x, function='cubic', smooth=0)  # default smooth=0 for interpolation
        Bx_dense = Bx_rbf(x_dense, z_dense, y_dense)  # not really a function, but a callable class instance

        Bz_rbf = interp.Rbf(df_data_shift_copy.x, df_data_shift_copy.z, df_data_shift_copy.y, df_data_shift_copy.B_z, function='cubic', smooth=0)  # default smooth=0 for interpolation
        Bz_dense = Bz_rbf(x_dense, z_dense, y_dense)  # not really a function, but a callable class instance

        By_rbf = interp.Rbf(df_data_shift_copy.x, df_data_shift_copy.z, df_data_shift_copy.y, df_data_shift_copy.B_y, function='cubic', smooth=0)  # default smooth=0 for interpolation
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

        data_interp = data_total.copy()
        data_interp[2] = df_all_intr

        # plotting to check

        # fig = plt.figure(figsize=(11, 5))
        # ax1 = fig.add_subplot(1, 2, 1, projection='3d')

        # ctf.plotMapping(ax1, data_interp, title="PENTrack origin, \ninterpolated to rectilinear grid, with sliced corners", view=4, txtSize='x-small')
        # B1 = np.sqrt(data_interp[2]['B_x']**2 + data_interp[2]['B_y']**2 + data_interp[2]['B_z']**2 )*100 #muT
        # Q = ax1.scatter(data_interp[2]['x'], data_interp[2]['y'], data_interp[2]['z'],c=B1, s=1, alpha=1, cmap=cm.plasma)

        # cbar = fig.colorbar(Q, label='$\mathsf{|B|\,(\mu T)}$')
        # plt.subplots_adjust(wspace=0.0)
        # plt.show()


        ### Save to txt file for PENTrack ###

        BField_data_fixed = data_interp[2].to_numpy()
        BField_Names = data_interp[2].columns

        comment = "This data is interpolated from Takashi's summer 2019 data. The data has been shifted"+\
            f" at the best idea so that the MSR is the origin, and by dx={x_shift}, dy={y_shift} cm to try to spot a mistake in the coords" +\
            " as well as interpolated and cut to match fall 2022 data for comparing."
                # , as well as interpolated and cut to match fall 2022 data for comparing."

                # 
        file = 'original data'

        headerText = f'File: {file}\n' + f'Date created: {date.today().strftime("%d/%m/%Y")}\n'\
            + 'Units: [cm], [1 muT = 1e-6 T]\n' +f'Offset from original data used: {off_sets} cm\n + \nRotation about z axis: '\
            + f'{rotation} degrees\n' + f'Resulting total origin shift: {off_setwithRotation} cm\n'\
            + f'Comments: {comment}\n' + '\t'.join(BField_Names)

        file_save = f"map_referencedMSR_shift[{x_shift},{y_shift}]"

        if CUT:
            file_save = file_save + "_CUT"

        file_save = file_save + f"_interp{NL}"

        print(f"Saving file: ./data_export/shifts/{file_save}.txt")

        np.savetxt(f'./data_export/shifts2/{file_save}.txt', BField_data_fixed,  delimiter='\t', newline='\n', header=headerText)


# print(saveLimits)


np.savetxt(f"./data_export/Limits_try1.csv", saveLimits, delimiter=',', newline='\n',
    header=f'Limits for x,y shifts of\nx:{x_shift_arr}, y:{y_shift_arr} cm', footer='', comments='# ')
