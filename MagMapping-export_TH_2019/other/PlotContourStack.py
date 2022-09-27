# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 09:16:53 2020

This python code plots a stack of contour plots going up the z-axis for all of the x and y planes.  
It requires regular nxn array of values.

Input:
It takes in a series of csv files of the format:
    start_t end_t u v w B_x B_y B_z
    where (x,y,z) are the nominal probe position, and B(x,y,z) are the probe output in volts that needs to be converted to mangetic field.

Output:
    4 plots of the B_x, B_y, B_z, and magnitude of the B-field in png format

@author: Mark McCrea
"""

import pandas as pd

pd.set_option('display.max_columns', None)   #prints all columns in head() describe() etc

import numpy as np;
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot;
from matplotlib import cm;
from mpl_toolkits.mplot3d import Axes3D;
pyplot.interactive(True);

#pyplot.gcf().subplots_adjust(right=0.5)

# ### Import data
df1 = pd.read_csv('Data-Meson_hall_maps/20200201_1026_Feb01_map_avg.csv')
df2 = pd.read_csv('Data-Meson_hall_maps/20200201_1356_Feb01_map_02_avg.csv')
#df3 = pd.read_csv('Data-Meson_hall_maps/20200202_1119_Feb02_map01_avg.csv')

df_all = df1.append(df2)
#df_all = df_all.append(df3)

print(df_all.columns)#display all column headers

# axis offsets
# the coordinates given (uvw) should be to the center of the z-axis probe in cm
# y-axis is ( , ,) offset from that
# x- axis is ( , , ) offset from that
# the center of the MSR is located at (-64.5, -74.3 ,275)cm
# The offsets used here are to place the center of the coordinate system at the center of the MSR
x_offset = 0#-64.5
y_offset = 0#-74.3
z_offset = 0# 275
df_all['x'] = df_all.u - x_offset
df_all['y'] = df_all.v - y_offset
df_all['z'] = df_all.w - z_offset

volt_to_microT = 100
df_all['B_x'] = volt_to_microT * df_all['B_u']  
df_all['B_y'] = volt_to_microT * df_all['B_v']
df_all['B_z'] = volt_to_microT * df_all['B_w'] 
df_all['B_Mag'] = np.power(np.power(df_all['B_z'],2)+np.power(df_all['B_y'],2)+np.power(df_all['B_x'],2),0.5) ## previous version, but it was found that the label on the porbe was mistaken 

df_all.to_csv('Data-Meson_hall_maps/CombinedFieldMaps.csv')

B_min = np.min([np.min(df_all.B_x),np.min(df_all.B_y),np.min(df_all.B_z)])
B_max = np.max([np.max(df_all.B_x),np.max(df_all.B_y),np.max(df_all.B_z)])
print('B_min = ', B_min, '  B_max =' , B_max)

z_all = df_all.z.unique()
z_nom = [30, 60, 100, 140, 180, 220, 260, 300, 340]#values for z slicing based on mounting base height
y_all = df_all.y.unique()
x_all = df_all.x.unique()


# Creat mesh for plotting color squares on
X = np.sort(x_all);
Y = np.sort(y_all);
X, Y = np.meshgrid(X, Y);
Z = np.zeros_like(X);# Create flat surface.

#choose z slice to plot at
idx_cut = 4 # set the index of x to make a cut, can be 0 to 9

fig2 = pyplot.figure(facecolor='white', figsize=(7.25,10))

axx = fig2.add_subplot(221, projection='3d')
axy = fig2.add_subplot(222, projection='3d')
axz = fig2.add_subplot(223, projection='3d')
axm = fig2.add_subplot(224, projection='3d')
axList = [axx , axy,  axz , axm]

plotting = ['B_x', 'B_y', 'B_z', 'B_Mag']
for i in range(len(axList)):
    axList[i].set_title(plotting[i])
    axList[i].set_xlabel('x (cm)')
    axList[i].set_ylabel('y (cm)')
    axList[i].set_zlabel('z (cm)')

#list of color maps
maps_x=[]
maps_y=[]
maps_z=[]
maps_m=[]
mapsList = [maps_x, maps_y, maps_z, maps_m]

for i in range(len(z_nom)):
    map_x = pd.DataFrame()
    map_y = pd.DataFrame()
    map_z = pd.DataFrame()
    map_m = pd.DataFrame()
    map = [map_x, map_y, map_z, map_m]
    z_cut=z_nom[i] + z_offset
    print('z_cut=',z_cut)
    for val in np.sort(x_all): 
        print('val=',val)
        df_heat_sub = df_all[(df_all.z<z_cut+10.0) & (df_all.z>z_cut-2) & (df_all.x==val) ]
        df_heat_sub = df_heat_sub[['x', 'y','z','B_x','B_y','B_z', 'B_Mag']]
#        print(df_heat_sub)
#        print(map)
        for jj in range(len(map)):
            map[jj][val] = df_heat_sub[plotting[jj]].to_numpy()
#        map_y[val] = df_heat_sub[plotting[1]].to_numpy()
#        map_z[val] = df_heat_sub[plotting[2]].to_numpy()
#        map_m[val] = df_heat_sub[plotting[3]].to_numpy()
    print('map(post loop):')
#    print('map_x = ',map_x)
#    print('map_y = ',map_y)
#    print('map_z = ',map_z)
#    print('map_m = ',map_m)
    maps_x.append(map_x)
    maps_y.append(map_y)
    maps_z.append(map_z)
    maps_m.append(map_m)
    print('mapsList[',0,']:')
    print(mapsList[0])
    
## Plot
#print(maps_x)
#print(maps_y)
#print(maps_z)
#print(maps_m)
#print(axList)

#plot a 2x2 grid of the heat map plots
for i in range(len(maps_x)):
#    A = mapsList[j][i].to_numpy()
    A = maps_x[i].to_numpy()
    B = maps_y[i].to_numpy()
    C = maps_z[i].to_numpy()
    D = maps_m[i].to_numpy()
    #A -= np.min(A); A /= np.max(A);
    A -= B_min; A /= B_max;
    B -= B_min; B /= B_max;
    C -= B_min; C /= B_max;
    D -= B_min; D /= B_max; 
    axList[0].plot_surface(X, Y, Z+z_nom[i], rstride=1, cstride=1, facecolors = cm.plasma(A));
    axList[1].plot_surface(X, Y, Z+z_nom[i], rstride=1, cstride=1, facecolors = cm.plasma(B));
    axList[2].plot_surface(X, Y, Z+z_nom[i], rstride=1, cstride=1, facecolors = cm.plasma(C));
    axList[3].plot_surface(X, Y, Z+z_nom[i], rstride=1, cstride=1, facecolors = cm.plasma(D));


#creating color bar
N = 14 #number of divisions in the color bar
cmap = pyplot.get_cmap('plasma',N)
norm = matplotlib.colors.Normalize(vmin=B_min,vmax=B_max) #sets min and max of color bar
sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
#add color bar to last plot
pyplot.colorbar(sm, ticks=np.linspace(B_min,B_max,N), 
             boundaries=np.arange(B_min,B_max,1))

fname = 'plots_MSR_center/ContStack.png'
fig2.savefig(fname)


#startingf single plot outputs
fnameX = 'plots_MSR_centerNew/ContStack-B_X.png'
fnameY = 'plots_MSR_centerNew/ContStack-B_Y.png'
fnameZ = 'plots_MSR_centerNew/ContStack-B_Z.png'
fnameM = 'plots_MSR_centerNew/ContStack-B_Mag.png'
fnameList = [fnameX , fnameY , fnameZ , fnameM]

height = 10
width = 7.25
figX = pyplot.figure(facecolor='white', figsize=(width,height))
axX = figX.add_subplot(111, projection='3d')
figY = pyplot.figure(facecolor='white', figsize=(width,height))
axY = figY.add_subplot(111, projection='3d')
figZ = pyplot.figure(facecolor='white', figsize=(width,height))
axZ = figZ.add_subplot(111, projection='3d')
figM = pyplot.figure(facecolor='white', figsize=(width,height))
axM = figM.add_subplot(111, projection='3d')
figList = [figX, figY, figZ, figM]
axn = [axX, axY, axZ, axM]
#create plots and set titles

for i in range(len(axn)):
    axn[i].set_title(plotting[i])
    axn[i].set_xlabel('x (cm)')
    axn[i].set_ylabel('y (cm)')
    axn[i].set_zlabel('z (cm)')

for i in range(len(maps_x)):
    A = maps_x[i].to_numpy()
    B = maps_y[i].to_numpy()
    C = maps_z[i].to_numpy()
    D = maps_m[i].to_numpy()
    #remonarlization doesn't seem to be needed if it was dne in the previous section for uncertain reasons.
    #A -= np.min(A); A /= np.max(A);
#    A -= B_min; A /= B_max;
#    B -= B_min; B /= B_max;
#    C -= B_min; C /= B_max;
#    D -= B_min; D /= B_max; 
    axn[0].plot_surface(X, Y, Z+z_nom[i], rstride=1, cstride=1, facecolors = cm.plasma(A));
    axn[1].plot_surface(X, Y, Z+z_nom[i], rstride=1, cstride=1, facecolors = cm.plasma(B));
    axn[2].plot_surface(X, Y, Z+z_nom[i], rstride=1, cstride=1, facecolors = cm.plasma(C));
    axn[3].plot_surface(X, Y, Z+z_nom[i], rstride=1, cstride=1, facecolors = cm.plasma(D));


#pyplot.colorbar(sm, ticks=np.linspace(B_min,B_max,N), 
#             boundaries=np.arange(B_min,B_max,1))

for fig in figList:
    fig.colorbar(sm, ticks=np.linspace(B_min,B_max,N), boundaries=np.arange(B_min,B_max,1))


for i in range(len(figList)):
    figList[i].savefig(fnameList[i])