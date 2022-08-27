#Emma Klemets
#Aug 2022

#############################################################
# HOW TO USE 
# This code imports the mapping data as a pandas data frame, 
# rotates and shifts the data before interpolating for a given
# range and setting the edges of the region outside where data
# was taken to ?
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

# from matplotlib.ticker import LinearLocator, FormatStrFormatter
# from matplotlib.ticker import FormatStrFormatter

import scipy
import scipy.interpolate as interp
import CoordTransfFunctions as ctf


### Import data

# I am pretty sure this data is in [cm] and [0.1 mT = 1e-4 T = 1 G]
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

# df_all.to_csv('data_csv/rawdata_all.csv')
# df_plat0 = df_all[df_all.z>0]
# df_plat0.to_csv('data_csv/rawdata_all_z_above_platform.csv')

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

### Re orientation
# All the work is done in the functions in CoordTransfFunctions.py

df_BField_data_fixed, off_sets, rotation, off_setwithRotation, data_total = ctf.FixOffset(df_all_sub, plot=False, alpha=.5)

print("Transformed data")
ctf.Limits(df_BField_data_fixed)

### Interpolation

# copied from plot_simple_cut_horizontal.py for interpolation

x_min, x_max= np.min(df_BField_data_fixed.x), np.max(df_BField_data_fixed.x)
z_min, z_max= np.min(df_BField_data_fixed.z), np.max(df_BField_data_fixed.z)
y_min, y_max= np.min(df_BField_data_fixed.y), np.max(df_BField_data_fixed.y)

NL = 50 # this defines the number of points for interpolation,  default is 50

x_dense, z_dense, y_dense = np.meshgrid(np.linspace(x_min, x_max, NL), np.linspace(z_min, z_max, NL), np.linspace(y_min,y_max, NL))

Bx_rbf = interp.Rbf(df_BField_data_fixed.x, df_BField_data_fixed.z, df_BField_data_fixed.y, df_BField_data_fixed.B_x, function='cubic', smooth=0)  # default smooth=0 for interpolation
Bx_dense = Bx_rbf(x_dense, z_dense, y_dense)  # not really a function, but a callable class instance

Bz_rbf = interp.Rbf(df_BField_data_fixed.x, df_BField_data_fixed.z, df_BField_data_fixed.y, df_BField_data_fixed.B_z, function='cubic', smooth=0)  # default smooth=0 for interpolation
Bz_dense = Bz_rbf(x_dense, z_dense, y_dense)  # not really a function, but a callable class instance

By_rbf = interp.Rbf(df_BField_data_fixed.x, df_BField_data_fixed.z, df_BField_data_fixed.y, df_BField_data_fixed.B_y, function='cubic', smooth=0)  # default smooth=0 for interpolation
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

#plotting to check

# fig = plt.figure(figsize=(11, 5))
# ax1 = fig.add_subplot(1, 2, 1, projection='3d')

# ctf.plotMapping(ax1, data_interp, title="PENTrack origin, \ninterpolated to rectilinear grid", view=4, txtSize='x-small')
# B1 = np.sqrt(data_interp[2]['B_x']**2 + data_interp[2]['B_y']**2 + data_interp[2]['B_z']**2 )*100 #muT
# Q = ax1.scatter(data_interp[2]['x'], data_interp[2]['y'], data_interp[2]['z'],c=B1, s=1, alpha=1, cmap=cm.plasma)

# cbar = fig.colorbar(Q, label='$\mathsf{|B|\,(\mu T)}$')
# plt.subplots_adjust(wspace=0.0)
# plt.show()

### Data removal
def Remove_Data(x, y, corners):
    """
    'Removes' data outside of the original range before interpolation
    """
    lines = []
    for i in range(len(corners[:4])):
        xs = [corners[i,0], corners[(i+1)%4,0]]
        ys = [corners[i,1], corners[(i+1)%4,1]]
        a,b = np.polyfit(xs, ys, 1)
#         print(a,b)        
        lines.append(a*x+b)

    # plt.plot(x, lines[0], label="1")
    # plt.plot(x, lines[1], label="2")
    # plt.plot(x, lines[2], label="3")
    # plt.plot(x, lines[3], label="4")

    # plt.legend()
    # plt.show()
        
    side1 = y >= lines[0]
    side2 = y <= lines[1]
    side3 = y <= lines[2]
    side4 = y >= lines[3]
    
    goodpoints = side1 & side2 & side3 & side4
    
    return goodpoints

CutCorners = True

if CutCorners:
    # [center_PEN, corners_PEN, data_PEN, MSR_center_PEN, O_PEN]
    corners = data_interp[1]
    PointsInside = Remove_Data(data_interp[2]['x'], data_interp[2]['y'], corners.T)

    #now what to do with the sketchy points outside this region?
    #could just set to 0 for now, might need to change later
    data_interp[2]["Inside Mapped Region"] = PointsInside

    #set values outside this range to 0
    data_interp[2].loc[~data_interp[2]["Inside Mapped Region"], ['B_x', 'B_y', 'B_z']] = 0, 0, 0
    data_interp[2] = data_interp[2].drop("Inside Mapped Region", axis=1)

    # display(data_interp[2])


# plotting to check

fig = plt.figure(figsize=(11, 5))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')

ctf.plotMapping(ax1, data_interp, title="PENTrack origin, \ninterpolated to rectilinear grid, with sliced corners", view=4, txtSize='x-small')
B1 = np.sqrt(data_interp[2]['B_x']**2 + data_interp[2]['B_y']**2 + data_interp[2]['B_z']**2 )*100 #muT
Q = ax1.scatter(data_interp[2]['x'], data_interp[2]['y'], data_interp[2]['z'],c=B1, s=1, alpha=1, cmap=cm.plasma)

cbar = fig.colorbar(Q, label='$\mathsf{|B|\,(\mu T)}$')
plt.subplots_adjust(wspace=0.0)
plt.show()


### Save to txt file for PENTrack

BField_data_fixed = data_interp[2].to_numpy()
BField_Names = data_interp[2].columns

comment = "This data is interpolated from Takashi's summer 2019 data. The data has been shifted and rotated to,"+\
    " to match the origin and axes used in PENTrack STL files, as well as interpolated to a rectilinear grid in this " +\
    "rotated frame."

file = 'original data'

headerText = f'File: {file}\n' + f'Date created: {date.today().strftime("%d/%m/%Y")}\n'\
    + 'Units: [cm], [G = 1e-4 T]\n' +f'Offset from original data used: {off_sets} cm\n + \nRotation about z axis: '\
    + f'{rotation} degrees\n' + f'Resulting total origin shift: {off_setwithRotation} cm\n'\
    + f'Comments: {comment}\n' + '\t'.join(BField_Names)

file_save = f"map_referencedPENTrack_interp{NL}"
if CutCorners:
    file_save = file_save + "_cutCorners"
    comment = comment + " The corners of this grid outside the original data edges have also been set to 0."

print(f"Saving file: ./data_export/{file_save}.txt")

np.savetxt(f'./data_export/{file_save}.txt', BField_data_fixed,  delimiter='\t', newline='\n', header=headerText)
