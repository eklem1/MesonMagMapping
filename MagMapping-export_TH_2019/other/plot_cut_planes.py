# coding: utf-8

################################################################################################################
# HOW TO USE 
# This code exports a 2D cut of a 3D map for each of the (Bx, By, Bz, and total magnitude) component
# 
# If you want to change the cut conditions, edit around line 100.
#
#  x_all: all the unique x included in the df_all, the data frame including all measured data  
# idx_ucut: defines the index of x_all by which the x_cut is chosenm
# z_cut_min, z_cut_max: define the range of z to select the subset of df_all to be plotted 
# You may need to play around with the parameters in lines 148-168 to optimiza the visibility of the plots.
#
# code modified by Mark McCrea 2020/02/14
################################################################################################################

# ### Preamble
import pandas as pd

pd.set_option('display.max_columns', None)   #prints all columns in head() describe() etc

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

import scipy
import scipy.interpolate as interp

# ### Import data
df1 = pd.read_csv('./Data-Meson_hall_maps/20200201_1026_Feb01_map_avg.csv')
df2 = pd.read_csv('./Data-Meson_hall_maps/20200201_1356_Feb01_map_02_avg.csv')
df3 = pd.read_csv('./Data-Meson_hall_maps/20200202_1119_Feb02_map01_avg.csv')

df_all = df1.append(df2)
df_all = df_all.append(df3)

print(df_all.columns)#display all column headers

#offsets from measurement coordinates system center to center of MSR to be added
#Note: update axn axis limits when updating the center points
df_all['x'] = df_all.u
df_all['y'] = df_all.v 
df_all['z'] = df_all.w
# -1.25cm accounts for the position of the sensing center of the probe and the marker on the probe. 
# + 188.1cm: from z=0 of the measurement to the floor, -275cm: from the floor to the planned center of MSR
# df_all['z'] = df_all.v -1.25 ## previous version
df_all['B_x'] = df_all['B_u']
df_all['B_y'] = df_all['B_v']
df_all['B_z'] = df_all['B_w'] 
df_all['B_Mag'] = np.power(np.power(df_all['B_z'],2)+np.power(df_all['B_y'],2)+np.power(df_all['B_x'],2),0.5) ## previous version, but it was found that the label on the porbe was mistaken 


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

B_min = 100*np.min([np.min(df_all.B_x),np.min(df_all.B_y),np.min(df_all.B_z)])
B_max = 100*np.max([np.max(df_all.B_x),np.max(df_all.B_y),np.max(df_all.B_z)])
print('B_min = ', B_min, '  B_max =' , B_max)

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
#print("unique z values:")
#print(np.sort(z_all))
print("unique x values:")
print(x_all)
# print len(y_all)

# ### Make a cut with x=const., select the range of z, interpolate the subset of data

# The original data is B_i(x,y,z) (i={x,y,z}), each of the three components is a three-dimensional function
# In the following, a cut is obtained for x=c (const.), B_i(y,z|x=c)

idx_ucut = 9 # set the index of x to make a cut, can be 0 to 9
x_cut=x_all[idx_ucut]
z_cut_min = 50.0
z_cut_max = 350.0

df_all_sub = df_all[(df_all.x==x_cut) & (df_all.z <= z_cut_max) & (df_all.z >= z_cut_min)] # select the subset of the data frame

z_min, z_max= np.min(df_all_sub.z), np.max(df_all_sub.z)
y_min, y_max= np.min(df_all_sub.y), np.max(df_all_sub.y)
x_min, x_max= np.min(df_all_sub.x), np.max(df_all_sub.x)

# ### Producing the plots

fig2 = plt.figure(facecolor='white', figsize=(14,14))

ax4 = fig2.add_subplot(221, projection='3d')
ax5 = fig2.add_subplot(222, projection='3d')
ax6 = fig2.add_subplot(223, projection='3d')
ax7 = fig2.add_subplot(224, projection='3d')

for axi in [ax4, ax5, ax6, ax7]:
    #chose an initial axis rotation here from the common choices:
    axi.view_init(elev=50., azim=125) # you may need to adjsut it for better data visibility
    #axi.view_init(elev=90., azim=180) #top down view
    #axi.view_init(elev=00., azim=270) #view B_ vertical, z horizontal
    
    axi.set_xlim3d(z_min,z_max) # this is for a purpose to produce plots with z=0 : floor
    axi.set_ylim3d(y_min,y_max)    
    #axi.set_ylim3d(B_min,B_max) 

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
    
#draws line between points of same y values
for yi in y_all:
    ax4.plot(df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].z,df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].y, df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].B_x*100, '-', c='black', lw=.5)    
    ax5.plot(df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].z,df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].y, df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].B_y*100, '-', c='black', lw=.5)
    ax6.plot(df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].z,df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].y, df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].B_z*100, '-', c='black', lw=.5)
    ax7.plot(df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].z,df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].y, df_all_sub.sort_values('z')[df_all_sub.sort_values('z').y==yi].B_Mag*100, '-', c='black', lw=.5)
#draws line between points of same z values
for zi in z_all:
    ax4.plot(df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].z,df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].y, df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].B_x*100, '-', c='black', lw=.5)
    ax5.plot(df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].z,df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].y, df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].B_y*100, '-', c='black', lw=.5)
    ax6.plot(df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].z,df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].y, df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].B_z*100, '-', c='black', lw=.5)
    ax7.plot(df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].z,df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].y, df_all_sub.sort_values('y')[df_all_sub.sort_values('y').z==zi].B_Mag*100, '-', c='black', lw=.5)

# use either color based on B_ or color based on y depdending on plotting preferences, only one ca be used at a time.
#color based on B_
sc4 = ax4.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_x*100,c=df_all_sub.B_x*100, marker='s', cmap=cm.plasma)
sc5 = ax5.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_y*100,c=df_all_sub.B_y*100, marker='s', cmap=cm.plasma)
sc6 = ax6.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_z*100,c=df_all_sub.B_z*100, marker='s', cmap=cm.plasma)
sc7 = ax7.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_Mag*100,c=df_all_sub.B_Mag*100, marker='s', cmap=cm.plasma)

#color based on y
# set axi.view_init(elev=00., azim=270) on lines approximately 123-125  goes well with this option.
#sc4 = ax4.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_x*100,c=df_all_sub.y, marker='s', cmap=cm.plasma)
#sc5 = ax5.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_y*100,c=df_all_sub.y, marker='s', cmap=cm.plasma)
#sc6 = ax6.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_z*100,c=df_all_sub.y, marker='s', cmap=cm.plasma)
#sc7 = ax7.scatter(df_all_sub.z, df_all_sub.y, df_all_sub.B_Mag*100,c=df_all_sub.y, marker='s', cmap=cm.plasma)

ax4.set_title('$\mathsf{B_x}$') 
ax4.set_zlabel('$\mathsf{B_x\,(\mu T)}$', rotation=180, labelpad=10)

ax5.set_zlabel('$\mathsf{B_y\,(\mu T)}$', rotation=180, labelpad=10)
ax5.set_title('$\mathsf{B_y}$')

ax6.set_zlabel('$\mathsf{B_z\,(\mu T)}$', rotation=180, labelpad=10)
ax6.set_title('$\mathsf{B_z}$')

ax7.set_zlabel('$\mathsf{B_Mag\,(\mu T)}$', rotation=180, labelpad=10)
ax7.set_title('$\mathsf{B_{Mag}}$')

fig2.suptitle('$\mathsf{x=%.2f\,cm}$'%(x_cut))

fig2.tight_layout(pad=4,rect=[0, 0, 1, 0.99])# plt.colorbar(sc, ax=ax4)

fname = 'plots_MSR_centerNew/4cut_x_%.2f_z_[%.2f, %.2f].png' %(x_cut, z_cut_min, z_cut_max)
fig2.savefig(fname)
print('saved out:',fname)