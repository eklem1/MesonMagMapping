# coding: utf-8

#############################################################
# HOW TO USE 
# This code imports the mapping data as a pandas data frame, 
# and then export the data in a range set by the user. 
# Edit around line 100 to change the cut conditions 
#############################################################

# ### Preamble

import pandas as pd
import numpy as np
# get_ipython().magic(u'matplotlib notebook')
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.ticker import FormatStrFormatter

import numpy as np
import scipy
import scipy.interpolate as interp


# ### Import data

df1 = pd.read_csv('Mapping_0809_RUN1.csv')
df2 = pd.read_csv('Mapping_0809_RUN2.csv')
df3 = pd.read_csv('Mapping_0809_RUN3.csv')
df4 = pd.read_csv('Mapping_0809_RUN4.csv')

df_all0 = df1.append(df2)
df_all1  = df_all0.append(df3)
df_all  = df_all1.append(df4)

df_all['x'] = - df_all.u + 10.25
df_all['y'] = -df_all.w
df_all['z'] = df_all.v -1.25 +188.1 -275 #-> sets z = 0 to the center of the MSR 
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


# v_floors = df_all1.v.unique()
v_all = df_all.v.unique()
w_all = df_all.w.unique()
u_all = df_all.u.unique()
# print len(v_all)
# print len(u_all)

# print len(w_all)
# z_floors = df_all.z.unique()

z_all = df_all.z.unique()
y_all = df_all.y.unique()
x_all = df_all.x.unique()
# print len(z_all)
# print len(x_all)
# print len(y_all)


# ### Make a cut with x=const., select the range of z, interpolate the subset of data

x_cut_min = np.min(x_all)
x_cut_max = np.max(x_all)
y_cut_min = np.min(y_all)
y_cut_max = np.max(y_all)
z_cut_min = np.min(z_all)
z_cut_max = np.max(z_all)

# x_cut_min = np.min(x_all)
# x_cut_max = np.max(x_all)
# y_cut_min = np.min(y_all)
# y_cut_max = np.max(y_all)
# z_cut_min = -200
# z_cut_max = 400

df_all_sub = df_all[(df_all.x <= x_cut_max) & (df_all.x >= x_cut_min)
                    & (df_all.y <= y_cut_max) & (df_all.y >= y_cut_min)
                    & (df_all.z <= z_cut_max) & (df_all.z >= z_cut_min)] # select the subset of the data frame

print(df_all_sub.index.size)
df_all_sub.index.name = 'index'

# """
#copied from plot_simple_cut_horizontal.py for interpolation, but this is only made for interpolation on a plane
# can I just exend this to 3D and then save the resulting data in a form I can use in PENTrack (once the relative
#positioning is fixed?)

z_min, z_max= np.min(df_all_sub.z), np.max(df_all_sub.z)
y_min, y_max= np.min(df_all_sub.y), np.max(df_all_sub.y)
NL = 50 # this defines the number of points for interpolation,  default is 50

z_dense, y_dense = np.meshgrid(np.linspace(z_min, z_max, NL), np.linspace(y_min,y_max, NL))

# Bx_rbf = interp.Rbf(df_all_sub.z, df_all_sub.y, df_all_sub.B_u, function='cubic', smooth=0)  # default smooth=0 for interpolation
Bx_rbf = interp.Rbf(df_all_sub.z, df_all_sub.y, df_all_sub.B_x, function='cubic', smooth=0)  # default smooth=0 for interpolation
Bx_dense = Bx_rbf(z_dense, y_dense)  # not really a function, but a callable class instance

Bz_rbf = interp.Rbf(df_all_sub.z, df_all_sub.y, df_all_sub.B_z, function='cubic', smooth=0)  # default smooth=0 for interpolation
Bz_dense = Bz_rbf(z_dense, y_dense)  # not really a function, but a callable class instance

By_rbf = interp.Rbf(df_all_sub.z, df_all_sub.y, df_all_sub.B_y, function='cubic', smooth=0)  # default smooth=0 for interpolation
By_dense = By_rbf(z_dense, y_dense)  # not really a function, but a callable class instance
# """


df_all_sub[['x','y','z','B_x','B_y','B_z']].to_csv('data_export/map_export1_[%.1f,%.1f]_[%.1f,%.1f]_[%.1f,%.1f].csv' %(x_cut_min, x_cut_max, y_cut_min, y_cut_max, z_cut_min, z_cut_max))
