#Emma Klemets
#Aug 2022

#############################################################
# CoordTransfFunctions.py
#############################################################

### imports

import pandas as pd
import numpy as np
# get_ipython().magic(u'matplotlib notebook')
from IPython.display import display
import matplotlib
# matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib import cm
# from datetime import date
import sys
import os
sys.path.insert(1, '../PrettyPlotTools/')
import ParticlePlottingFunctions as ppf

def Limits(data):
    print(f"x: [{min(data['x'])}, {max(data['x'])}], y: [{min(data['y'])}, {max(data['y'])}], z: [{min(data['z'])}, {max(data['z'])}]")
    print(f"Bx: [{min(data['B_x'])}, {max(data['B_x'])}], By: [{min(data['B_y'])}, {max(data['B_y'])}], Bz: [{min(data['B_z'])}, {max(data['B_z'])}]")


def MakeCube(axes, center=np.array([0,0,0]), sideLengths = np.array([3.5, 3.5, 3.5]) , c='black', angle=0):
    """
    Makes a cube to represent the MSR, with control over the center of the MSR, the sidelengths, 
    the angle it is rotated by.
    """
    halfs_minus = [center[0]-sideLengths[0]/2, center[1]-sideLengths[1]/2, center[2]-sideLengths[2]/2]
    halfs_plus = [center[0]+sideLengths[0]/2, center[1]+sideLengths[1]/2, center[2]+sideLengths[2]/2]

    n = 20
    x_edge0 = np.linspace(halfs_minus[0], halfs_plus[0], n)
    y_edge0 = np.linspace(halfs_minus[1], halfs_plus[1], n)
    z_edge0 = np.linspace(halfs_minus[2], halfs_plus[2], n)
    
    x_min = halfs_minus[0]*np.ones(len(x_edge0))
    y_min = halfs_minus[1]*np.ones(len(x_edge0))
    z_min = halfs_minus[2]*np.ones(len(x_edge0))
    
    x_plus = halfs_plus[0]*np.ones(len(x_edge0))
    y_plus = halfs_plus[1]*np.ones(len(x_edge0))
    z_plus = halfs_plus[2]*np.ones(len(x_edge0))
    
    x_edge1, y_edge1 = rotate(np.array([x_edge0, y_min]).T, origin=center[:2], degrees=angle).T
    x_edge2, y_edge2 = rotate(np.array([x_min, y_edge0]).T, origin=center[:2], degrees=angle).T
    x_edge3, y_edge3 = rotate(np.array([x_min, y_min]).T, origin=center[:2], degrees=angle).T
    
    x_edge4, y_edge4 = rotate(np.array([x_edge0, y_plus]).T, origin=center[:2], degrees=angle).T
    x_edge5, y_edge5 = rotate(np.array([x_plus, y_edge0]).T, origin=center[:2], degrees=angle).T
    x_edge6, y_edge6 = rotate(np.array([x_plus, y_plus]).T, origin=center[:2], degrees=angle).T
    
    x_edge7, y_edge7 = rotate(np.array([x_edge0, y_min]).T, origin=center[:2], degrees=angle).T
    x_edge8, y_edge8 = rotate(np.array([x_min, y_edge0]).T, origin=center[:2], degrees=angle).T
    x_edge9, y_edge9 = rotate(np.array([x_min, y_plus]).T, origin=center[:2], degrees=angle).T
    
    x_edge10, y_edge10 = rotate(np.array([x_edge0, y_plus]).T, origin=center[:2], degrees=angle).T
    x_edge11, y_edge11 = rotate(np.array([x_plus, y_edge0]).T, origin=center[:2], degrees=angle).T
    x_edge12, y_edge12 = rotate(np.array([x_plus, y_min]).T, origin=center[:2], degrees=angle).T
    
    axes.scatter(center[0], center[1], center[2], color='purple', marker='*', s=45, label="MSR center")

    axes.plot(x_edge1, y_edge1, z_min, c=c)
    axes.plot(x_edge2, y_edge2, z_min, c=c)
    axes.plot(x_edge3, y_edge3, z_edge0, c=c)

    axes.plot(x_edge4, y_edge4, z_plus, c=c)
    axes.plot(x_edge5, y_edge5, z_plus, c=c)
    axes.plot(x_edge6, y_edge6, z_edge0, c=c)

    axes.plot(x_edge7, y_edge7, z_plus, c=c)
    axes.plot(x_edge8, y_edge8, z_plus, c=c)
    axes.plot(x_edge9, y_edge9, z_edge0, c=c)

    axes.plot(x_edge10, y_edge10, z_min, c=c)
    axes.plot(x_edge11, y_edge11, z_min, c=c)
    axes.plot(x_edge12, y_edge12, z_edge0, c=c)

    return axes

def getCorners(data):
    """
    Returns the coordinates of the 8 corners of the mapped area.
    The input data should be before any rotations as this assumes that the data is rectangular wrt to
    the coordinates currently.
    """
    x_dense_MSRframe = data['x']
    y_dense_MSRframe = data['y']
    z_dense_MSRframe = data['z']
    
    top_balc_M11 = [max(x_dense_MSRframe), max(y_dense_MSRframe), max(z_dense_MSRframe)]
    top_balc_cycl = [min(x_dense_MSRframe), max(y_dense_MSRframe), max(z_dense_MSRframe)]
    top_cycl_UCN = [min(x_dense_MSRframe), min(y_dense_MSRframe), max(z_dense_MSRframe)]
    top_M11_UCN = [max(x_dense_MSRframe), min(y_dense_MSRframe), max(z_dense_MSRframe)]

    bottom_balc_M11 = [max(x_dense_MSRframe), max(y_dense_MSRframe), min(z_dense_MSRframe)]
    bottom_balc_cycl = [min(x_dense_MSRframe), max(y_dense_MSRframe), min(z_dense_MSRframe)]
    bottom_cycl_UCN = [min(x_dense_MSRframe), min(y_dense_MSRframe), min(z_dense_MSRframe)]
    bottom_M11_UCN = [max(x_dense_MSRframe), min(y_dense_MSRframe), min(z_dense_MSRframe)]

    corners_MSRframe = np.array([top_balc_M11, top_balc_cycl, top_cycl_UCN, top_M11_UCN, bottom_balc_M11, 
               bottom_balc_cycl, bottom_cycl_UCN, bottom_M11_UCN]).T #cm
    
    #     print(f"Max dimension in x: {np.abs(top_balc_cycl[0]-top_balc_M11[0])} , y:", 
    #       f"{(top_balc_cycl[1]-top_cycl_UCN[1])}, z: {(top_balc_M11[2]-bottom_balc_M11[2])} cm")
    
    return corners_MSRframe

def plotMapping(ax, data, title, units="cm", view=0, angle=0, STLs=False, legend=True, txtSize='medium'):
    if len(data) == 5:
        center, corners, dataXB, MSR_center, Or = data
    else:
        print("Bad data passed")
        return

    ax.set_title(title, pad=-10)
    
    ax.scatter(center[0], center[1], center[2], color='orange', marker='*', s=45, label="Field mapped center")
    ax.scatter(corners[0,:4], corners[1,:4], corners[2,:4], color='blue', s=45, label="Field mapped corners top")
    ax.scatter(corners[0,4:], corners[1,4:], corners[2,4:], color='green', s=45, label="Field mapped corners bottom")

    ax.scatter(Or[0], Or[1], Or[2], color='red', marker='*', s=45, label="PENTrack STL center")
    
    if "cm" in units:
        MakeCube(ax, MSR_center, np.array([3.5,3.5,3.5])*100, angle=angle)
    elif "m" in units:
        MakeCube(ax, MSR_center, np.array([3.5,3.5,3.5]), angle=angle)
        
        if STLs:
            # #loads all the file I have in this folder as STLs
            STLpath = '../PrettyPlotTools/STLsToGraph'
            stl_array = os.listdir(STLpath)

            for STLfile in stl_array:
                ppf.graphSTL(STLpath+'/'+STLfile, ax, a=0.05)

    if view == 0:
        ax.view_init(elev=90., azim=-90)  #top view
    elif view == 1:
        ax.view_init(elev=0., azim=-90) #front view

    ax.set_xlabel(f'x [{units}]')
    ax.set_ylabel(f'y [{units}]')
    ax.set_zlabel(f'z [{units}]')
    if legend:
        ax.legend(loc='center left', bbox_to_anchor=(-.4, 0.3), fontsize=txtSize)

    return

def rotate(p, origin=(0, 0), degrees=0):
    #2D rotation
    #https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T-o.T) + o.T).T)


def rotate3D(p, origin=(0, 0, 0), degrees=0):
    #3D rotation
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle), 0],
                  [np.sin(angle),  np.cos(angle), 0],
                  [0, 0, 1]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    A = np.squeeze((R @ (p.T-o.T) + o.T).T)
    return A


def refToPENTrack(data_T, center_T):
    """    
    Makes the center of SCM be (0,0,0), and x parallel to the guide going into the SCM,
    y perpendicular to this.
    Input:
        data_T - data output from Takashi's file data_export.py, imported as a df.
        center_T - the center of this data (0,0,0)
    Returns:
        center, corners, data_transf, MSR_center
        all in cm
    """

    #First try at centering, using the corner marked as F1 on the floor
    # x_off = 161.2 - 126 # cm
    # y_off = 187 + 464.05 # cm
    # z_off = + 16.3 # cm

    #Using the center of the MSR that Tony marked for me
    x_off = 51.7 - 22.3# cm #deltaX of C_MSR to C_T - deltaX of C_MSR to C_SMC
    y_off = + 648.9 # cm #as the MSR center is already aligned with C_T, this is just the distance from the C_MSR to the C_SCM
    z_off = + 16.3 # cm #vertical center of the MSR has changed in designs by this much, based off prev. distance to concrete floor
    
    center = np.array([center_T[0]+x_off, center_T[1]+y_off, center_T[2]+z_off])
    MSR_center = np.array([-22.3, 643.8,0])
    
    data_transf = data_T.copy()

    data_transf['x'] += x_off
    data_transf['y'] += y_off
    data_transf['z'] += z_off
    
    corners = getCorners(data_transf)
    
    return center, corners, data_transf, MSR_center #C_SMC = (0,0,0)


def rotateBData(df_data, origin, angle):
    data_pos = rotate3D(df_data[['x', 'y', 'z']].values, origin=origin, degrees=angle)
    
    #gotta check this part makes sense
    data_B = rotate3D(df_data[['B_x', 'B_y', 'B_z']].values, origin=origin, degrees=angle)
    # print(f"Rotation of {angle} degrees")
    
    df_data_rot = pd.DataFrame(data_pos, columns=['x', 'y', 'z'])
    df_data_rot[['B_x', 'B_y', 'B_z']] = data_B
    
    return df_data_rot


def refToMSR(data_T, center_T):
    """    
    Makes the center of the MSR be (0,0,0), and x parallel to the guide going into the MSR,
    y perpendicular to this.
    Input:
        data_T - data output from Takashi's file data_export.py, imported as a df.
        center_T - the center of this data (0,0,0)
    Returns:
        center, corners, data_transf, MSR_center
        all in cm
    """

    #Using the center of the MSR that Tony marked for me
    x_off = 51.7 # cm #deltaX of C_MSR to C_T

    y_off = + 0 # cm #as the MSR center is already aligned with C_T

    z_off = + 16.3 # cm #vertical center of the MSR has changed in designs by this much, based off prev. distance to concrete floor
    
    center = np.array([center_T[0]+x_off, center_T[1]+y_off, center_T[2]+z_off])

    MSR_center = np.array([0,0,0])
    
    data_transf = data_T.copy()

    data_transf['x'] += x_off
    data_transf['y'] += y_off
    data_transf['z'] += z_off
    
    corners = getCorners(data_transf)
    
    return center, corners, data_transf, MSR_center

def FixOffset(df_BField_data, plot=False, alpha=.01, PEN_origin=True):
   
    center_T = np.array([0, 0, 0]) #our intial origin
    data_T = df_BField_data[["x", "y", "z", "B_x", "B_y", "B_z"]] #original data

    #there might be another rotation to do here, as the grid used to take this data is
    #not exactly straight with the sides of the MSR - meh, it's pretty close to straight

    if PEN_origin: #use the SCM as the origin with the axes aligned to the pre SCM guides

        #getting the correct shift to use in PENtrack, but not the coordinate rotation
        center_PEN_notRot, corners_PEN_notRot, data_PEN_notRot, MSR_center_PEN_notRot = refToPENTrack(data_T, center_T)

        off_sets = center_PEN_notRot #how much the old origin has shifted
        O_PEN_notRot =  np.array([0, 0, 0]) #the new origin to rotate about

        data1 = [center_PEN_notRot, corners_PEN_notRot, data_PEN_notRot, MSR_center_PEN_notRot, O_PEN_notRot]
        
        rotationAngle = -20 - 90 #20 degree switch from Y, plus swapping the x and y coords
        
        #apply the rotation to both the position and the B field components
        data_PEN = rotateBData(data_PEN_notRot.copy(), O_PEN_notRot, rotationAngle)
        center_PEN = rotate3D(center_PEN_notRot.T, origin=O_PEN_notRot, degrees=rotationAngle).T
        corners_PEN = rotate3D(corners_PEN_notRot.T, origin=O_PEN_notRot, degrees=rotationAngle).T
        MSR_center_PEN = rotate3D(MSR_center_PEN_notRot.T, origin=O_PEN_notRot, degrees=rotationAngle).T
        O_PEN = O_PEN_notRot

        data_return = [center_PEN, corners_PEN, data_PEN, MSR_center_PEN, O_PEN]

        data_PEN_m = data_PEN.copy()
        data_PEN_m[['x', 'y', 'z']] = data_PEN_m[['x', 'y', 'z']]/100

        # print(off_sets, MSR_center_PEN)
        data2 = [center_PEN/100, corners_PEN/100, data_PEN_m, MSR_center_PEN/100, O_PEN/100]

        data = data_PEN
        centerShift = center_PEN


        if plot:
            fig = plt.figure(figsize=(11, 5))
            ax1 = fig.add_subplot(1, 2, 1, projection='3d')
            ax2 = fig.add_subplot(1, 2, 2, projection='3d')

            plotMapping(ax1, data1, title="PENTrack origin, pre rotation", view=4)
            B1 = np.sqrt(data1[2]['B_x']**2 + data1[2]['B_y']**2 + data1[2]['B_z']**2 )*100 #muT
            Q = ax1.scatter(data1[2]['x'], data1[2]['y'], data1[2]['z'],c=B1, s=1, alpha=alpha, cmap=cm.plasma)

            plotMapping(ax2, data2, title="PENTrack frame", view=4, angle=rotationAngle, units="m", STLs=False, legend=False)

            B2 = np.sqrt(data2[2]['B_x']**2 + data2[2]['B_y']**2 + data2[2]['B_z']**2 )*100 #muT
            Q = ax2.scatter(data2[2]['x'], data2[2]['y'], data2[2]['z'],c=B2, s=1, alpha=alpha, cmap=cm.plasma)

            # [left, bottom, width, height] 
            cax = fig.add_axes([ax2.get_position().x1+0.04, ax2.get_position().y0, 0.02, ax1.get_position().y1-ax1.get_position().y0])

            cbar = fig.colorbar(Q, label='$\mathsf{|B|\,(\mu T)}$', cax=cax)
            plt.subplots_adjust(wspace=0.0)
            plt.show() 

    else: #here we just want the origin to be the center of the MSR, as they the axes are already aligned with F_T

        #getting the correct shift to use in PENtrack
        centerShift_MSR, corners_MSR, data_MSR, MSR_center_origin = refToMSR(data_T, center_T)

        off_sets = centerShift_MSR #how much the old origin has shifted
        O_PEN_notRot =  np.array([0, 0, 0]) #the new origin to rotate about

        data_return = [centerShift_MSR, corners_MSR, data_MSR, MSR_center_origin, MSR_center_origin]
        
        rotationAngle = 0

        data_MSR_m = data_MSR.copy()
        data_MSR_m[['x', 'y', 'z']] = data_MSR_m[['x', 'y', 'z']]/100 #convert to m

        # print(off_sets, MSR_center_PEN)
        data2 = [centerShift_MSR/100, corners_MSR/100, data_MSR_m, MSR_center_origin/100, MSR_center_origin/100]

        data = data_MSR
        centerShift = centerShift_MSR

        if plot:
            fig = plt.figure(figsize=(11, 5))
            ax1 = fig.add_subplot(1, 2, 1, projection='3d')

            plotMapping(ax1, data2, title="MSR origin", view=4, units="m", STLs=False, legend=True)
            B1 = np.sqrt(data2[2]['B_x']**2 + data2[2]['B_y']**2 + data2[2]['B_z']**2 )*100 #muT

            Q = ax1.scatter(data2[2]['x'], data2[2]['y'], data2[2]['z'], c=B1, s=1, alpha=alpha, cmap=cm.plasma)

            # [left, bottom, width, height] 
            cax = fig.add_axes([ax1.get_position().x1+0.04, ax1.get_position().y0, 0.02, ax1.get_position().y1-ax1.get_position().y0])

            cbar = fig.colorbar(Q, label='$\mathsf{|B|\,(\mu T)}$', cax=cax)
            plt.subplots_adjust(wspace=0.0)
            plt.show() 
        
    return data, off_sets, rotationAngle, centerShift, data_return
    
