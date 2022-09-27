# coding: utf-8

################################################################################################################
# HOW TO USE 
# This code exports a 2D cut of a 3D map for each of the (Bx, By, Bz) component
# The origin is chosen such that z=0 corresponds to the planned center of MSL-MSR, 2.75m from the floor (See line 48)
# If you want to change the cut conditions, edit around line 100.
#  x_all: all the unique x included in the df_all, the data frame including all measured data  
# idx_ucut: defines the index of x_all by which the x_cut is chosenm
# z_cut_min, z_cut_max: define the range of z to select the subset of df_all to be plotted 
# You may need to play around with the parameters in lines 148-168 to optimiza the visibility of the plots.
#
# CAUTION
# If there is too few data points, interpolation from line 121 will return an error saying 
# "ValueError: zero-size array to reduction operation maximum which has no identity"
################################################################################################################

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
df_all['z'] = df_all.v -1.25 +188.1 -275 
# -1.25cm accounts for the position of the sensing center of the probe and the marker on the probe. 
# + 188.1cm: from z=0 of the measurement to the floor, -275cm: from the floor to the planned center of MSR
# df_all['z'] = df_all.v -1.25 ## previous version
df_all['B_x'] = -df_all['B_u']
df_all['B_y'] = -df_all['B_w']
df_all['B_z'] = -df_all['B_v'] 
# df_all['B_z'] = df_all['B_v'] ## previous version, but it was found that the label on the porbe was mistaken 



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

# The original data is B_i(x,y,z) (i={x,y,z}), each of the three components is a three-dimensional function
# In the following, a cut is obtained for x=c (const.), B_i(y,z|x=c)

idx_ucut = 3 # set the index of x to make a cut, can be 0 to 9
x_cut=x_all[idx_ucut]
z_cut_min = -180
z_cut_max = 250

df_all_sub = df_all[(df_all.x==x_cut) & (df_all.z <= z_cut_max) & (df_all.z >= z_cut_min)] # select the subset of the data frame
# print df_all_sub.index.size

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



# ### Producing the plots


fig2 = plt.figure(facecolor='white', figsize=(14,5))

ax4 = fig2.add_subplot(131, projection='3d')
ax5 = fig2.add_subplot(132, projection='3d')
ax6 = fig2.add_subplot(133, projection='3d')


# ax4.tick_params(axis='x', rotation=-15, labelsize=10)
# ax4.tick_params(axis='y', rotation=-25, labelsize=10)
# ax4.tick_params(axis='y', rotation=-30, labelsize=11)
# ax4.set_ylim3d(np.min(df1_sub.z)-15,np.max(df1_sub.z)+5)



for axi in [ax4, ax5, ax6]:
    axi.view_init(elev=50., azim=125) # you may need to adjsut it for better data visibility
    
    axi.set_xlim3d(z_min,z_max) # this is for a purpose to produce plots with z=0 : floor
    axi.set_ylim3d(y_min,y_max)    

    axi.set_xticklabels(ax4.get_xticks(),  rotation=50,
                    verticalalignment='baseline',
                    horizontalalignment='right')
    axi.set_yticklabels(ax4.get_yticks(),  rotation=-25,
                    verticalalignment='baseline',
                    horizontalalignment='left')    

    axi.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    axi.yaxis.set_major_formatter(FormatStrFormatter('%d'))
                                  
    axi.set_xlabel('$\mathsf{z}$ (cm)', rotation=7, labelpad=10)
    axi.set_ylabel('$\mathsf{y}$ (cm)',  labelpad=15)

ax6.set_zlim(-90,-275) # invert the z-axis direction for B_z, just for visualization purpose
    
for yi in y_all:
    ax4.plot(df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].z,df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].y, df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].B_x*100, '-', c='black', lw=.5)    
    ax5.plot(df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].z,df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].y, df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].B_y*100, '-', c='black', lw=.5)
    ax6.plot(df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].z,df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].y, df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].B_z*100, '-', c='black', lw=.5)
for zi in z_all:
    ax4.plot(df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].z,df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].y, df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].B_x*100, '-', c='black', lw=.5)
    ax5.plot(df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].z,df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].y, df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].B_y*100, '-', c='black', lw=.5)
    ax6.plot(df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].z,df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].y, df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].B_z*100, '-', c='black', lw=.5)
    

sc4_int = ax4.scatter(z_dense, y_dense, Bx_dense*100, c=np.concatenate(Bx_dense)*100, marker='.', lw=.1, cmap=cm.plasma)
sc5_int = ax5.scatter(z_dense, y_dense, By_dense*100, c=np.concatenate(By_dense)*100, marker='.', lw=.1, cmap=cm.plasma)
sc6_int = ax6.scatter(z_dense, y_dense, Bz_dense*100, c=np.concatenate(Bz_dense)*100, marker='.', lw=.1, cmap=cm.plasma)

sc4 = ax4.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_x*100,c=df_all_sub.B_x*100, marker='s', cmap=cm.plasma)
sc5 = ax5.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_y*100,c=df_all_sub.B_y*100, marker='s', cmap=cm.plasma)
sc6 = ax6.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_z*100,c=df_all_sub.B_z*100, marker='s', cmap=cm.plasma)

ax4.set_title('$\mathsf{B_x}$') 
ax4.set_zlabel('$\mathsf{B_x\,(\mu T)}$', rotation=180, labelpad=10)

ax6.set_zlabel('$\mathsf{B_z\,(\mu T)}$', rotation=180, labelpad=10)
ax6.set_title('$\mathsf{B_z}$')

ax5.set_zlabel('$\mathsf{B_y\,(\mu T)}$', rotation=180, labelpad=10)
ax5.set_title('$\mathsf{B_y}$')

fig2.suptitle('$\mathsf{x=%.2f\,cm}$'%(x_cut))

fig2.tight_layout(pad=3,rect=[0, 0, 1, 0.99])# plt.colorbar(sc, ax=ax4)

fname = 'plots_MSR_center/cut2_x_%.2f_z_[%.2f, %.2f].png' %(x_cut, z_cut_min, z_cut_max)
fig2.savefig(fname)


