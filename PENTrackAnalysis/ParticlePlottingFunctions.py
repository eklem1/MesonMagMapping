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
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax0.legend(by_label.values(), by_label.keys())
#         ax0.legend()
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
A function to graph the 3D positions of the UCNs, in a 3D scatter plot, with coloring of points
as a function of the geometry they are in, and also the option to label each point with
the timing [s].
'''
def plot3D_geoColor(x, y, z, geo, t=None, startPlot=True, endPlot=True, label="", \
                    figVals=None, ls="None", text_times=False, size=(8,8)):
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
        
    #get the label and matching color for the geometry type that each neutron is in
    point_features = np.transpose([getColor(g) for g in geo] )
    colors = point_features[0]
    geo_label = point_features[1]
    
    #for connections between points if wanted
    ax1.plot3D(x, y, z, linestyle=ls, marker='') 
    #for different colors of each point
    ax1.scatter(x, y, z, c=colors)
    
    #includes the labeling for each geometry color
    for i, c in enumerate(colors):
        ax1.plot3D(100, 100, 100, linestyle="", marker='o', c=c, label=geo_label[i])
    
    if text_times:
        for i in range(len(x)): #plot each point's time as text above
            ax1.text(x[i],y[i],z[i],  '%s' % (str(t[i])), size=15, zorder=1, color='k') 
    
    #if it's the end of the plot, call the legend and show it
    if endPlot:
        #removes repeated labels so this doesn't look silly
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax1.legend(by_label.values(), by_label.keys())

#         ax1.legend()
        plt.show()
        #could add option to save the graph too here
    else:
        #if it's not the end of the graph, return the figure objects
        return [fig, ax1]
'''
returns the coorsponding geometry label and set color for a particular PENTrack
geometry tag.
Default for unknown/not yet defined geometry parts is black.
'''
def getColor(geo1):
    color = 'black'
    label = None

    if geo1 == 183:
        #Long Y guide
        color = 'red'
        label = 'Y_guide'
    elif geo1 in [187, 188]:
        #guides into chambers
        color = 'red'
    elif (2 <= geo1 <= 33) | (37 <= geo1 <= 114):
        #He vapour and liquid volumes 
        color='blue'
        label = 'He'
    elif geo1 in [185, 186]:
        #in the chambers to do the rest of the experiment
        color = 'black'
        label = 'in cell'
    elif geo1 == 1:
        #the default volume geometry
        color = 'orange'
        label = '1'
        
    else: #to catch new geometry labels coming up
        print(geo1)
        
    return color, label

'''
Here we have the 3D UCN plotting, with a colorbar axis for a variable input of 
the user's choice.
'''
def plot3D_varColor(x, y, z, var, t=None, startPlot=True, endPlot=True, label="", \
                    figVals=None, ls="None", text_times=False, size=(8,8)):
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
           
    #for connections between points if wanted
    ax1.plot3D(x, y, z, linestyle=ls, marker='') 
    #for different colors of each point
    p = ax1.scatter(x, y, z, c=var, cmap=plt.cm.magma, alpha=0.7)
    
    if text_times:
        for i in range(len(x)): #plot each point's time as text above
            ax1.text(x[i],y[i],z[i],  '%s' % (str(t[i])), size=15, zorder=1, color='k') 
    
    #if it's the end of the plot, call the legend and show it
    if endPlot:
        #removes repeated labels so this doesn't look silly
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax1.legend(by_label.values(), by_label.keys())

        fig.colorbar(p, ax=ax1)
        plt.show()
        #could add option to save the graph too here
    else:
        #if it's not the end of the graph, return the figure objects
        return [fig, ax1, p]
    
    
    
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