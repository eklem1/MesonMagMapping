import numpy as np
import matplotlib.pyplot as plt
import uproot as up
from mpl_toolkits.mplot3d import Axes3D
from stl import mesh
from mpl_toolkits import mplot3d
import scipy.stats as stats

'''
A function to graph the 3D position, in a 3D scatter plot as well as a view
on the planes: XY, XZ, YZ.

Lets you pass in a return the figure and axes objects so that more than
one set of values can be graph in one figure.
'''
def pltShape(x, y, z, startPlot=True, endPlot=True, label="", figVals=None, ls="None"):
    
    if startPlot: #create the figure and axes
        fig = plt.figure(figsize=(15,10))
        ax0 = fig.add_subplot(2,3,1)
        ax1 = fig.add_subplot(2,3,2, projection='3d')
        ax2 = fig.add_subplot(2,3,4)
        ax3 = fig.add_subplot(2,3,5)
        ax4 = fig.add_subplot(2,3,6)
        #controls camera angle of 3D plot
        ax1.view_init(elev=8., azim=45)
        ax1.set_xlim3d(-5, 7)
        ax1.set_ylim3d(-2, 0)
        ax1.set_zlim3d(-0.6, 0.5)
    else:
        #unpack the array that holds all the fig axes
        fig, ax0, ax1, ax2, ax3, ax4 = figVals
    
    #the 3D plot
    ax1.scatter(x, y, z, linestyle=ls)
    
    #empty plot to hold labels
    ax0.plot(0, label=label)
    
    #the 2D plots
    ax2.scatter(x, y, linestyle=ls)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax3.scatter(x, z, linestyle=ls)
    ax3.set_xlabel('x')
    ax3.set_ylabel('z')
    ax4.scatter(y, z, linestyle=ls)
    ax4.set_xlabel('y')
    ax4.set_ylabel('z')
    if endPlot:
        ax0.legend()
        plt.show()
    else:
        #if it's not the end of the graph, return the figure objects
        return [fig, ax0, ax1, ax2, ax3, ax4]
    
'''
A function to graph the 3D position, in a 3D scatter plot.
'''
def plot3D(x, y, z, startPlot=True, endPlot=True, label="", figVals=None, ls="None", size=(8,8)):
    if startPlot:
        fig = plt.figure(figsize=size)
        ax1 = fig.add_subplot(1,1,1, projection='3d')
        ax1.set_xlim3d(-5, 7)
        ax1.set_ylim3d(-2, 0)
        ax1.set_zlim3d(-0.6, 0.5)
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('z')
        
    else:
        #unpack the array that holds all the fig axes
        fig, ax1 = figVals
    
    #the 3D plot
    ax1.plot3D(x, y, z, linestyle=ls, label=label, marker='o')
    
    if endPlot:
        ax1.legend()
        plt.show()
    else:
        #if it's not the end of the graph, return the figure objects
        return [fig, ax1]
    
    
    
    
    
    
'''
Import and plot a stl file
''' 
def graphSTL(stlFile, axes, edgecolor="black", facecolor=None, linewidth=0.1, a=0.1):
    item_mesh = mesh.Mesh.from_file(stlFile, mode=None)
    #the mode=None suppresses the strange error I keep getting from these STLs
    item = mplot3d.art3d.Line3DCollection(item_mesh.vectors, linewidths=linewidth, alpha=a)
    item.set_edgecolor(edgecolor)
    item.set_facecolor(facecolor)
    axes.add_collection3d(item)