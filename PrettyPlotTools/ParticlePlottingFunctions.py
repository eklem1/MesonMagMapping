import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from stl import mesh
from mpl_toolkits import mplot3d
import scipy.stats as stats
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns

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
def plot3D(x, y, z, startPlot=True, endPlot=True, label="", figVals=None, ls="None", size=(8,8), c=None):
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
    if isinstance(c, type(None)):
        ax1.plot3D(x, y, z, linestyle=ls, label=label, marker='o')
    else:
        ax1.plot3D(x, y, z, linestyle=ls, label=label, marker='o', color=c)
    
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
    
    
    
'''
Plots all the data in 3D, with each component of the field plotted on a different graph
with a different colorbar.
Data should be a pandas df
'''
def PlotComponents(data, Compare=False, fsize=(20,6), lims=None, title=None, Sample=None, elev_set=None, azim_set=None):
    
    fig = plt.figure(figsize=fsize)
    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    fig.suptitle(title)     
    
    if lims is not None:
        Xvmin, Xvmax = lims[0]
        Yvmin, Yvmax = lims[1]
        Zvmin, Zvmax = lims[2]
    else:
        Xvmin, Xvmax = [None,None]
        Yvmin, Yvmax = [None,None]
        Zvmin, Zvmax = [None,None]

    axes = [ax1, ax2, ax3]
    
    if Sample is not None:
        data = data.sample(Sample)
        s_set=plt.rcParams['lines.markersize'] ** 2
    else:
        s_set=.5
    
    if Compare:
        Q_19 = ax1.scatter(data['x'], data['y'], data['z'],c=data['dB_x'], s=s_set, 
                           alpha=1, cmap=cm.PiYG, vmin=Xvmin, vmax=Xvmax)
        cbar_19 = fig.colorbar(Q_19, label='$dB_x (\mu T)$', ax=ax1, pad=0.1)
        ax1.set_title("$dB_x$")

        Q_22 = ax2.scatter(data['x'], data['y'], data['z'],c=data['dB_y'], s=s_set, 
                           alpha=1, cmap=cm.PRGn, vmin=Yvmin, vmax=Yvmax)
        cbar_22 = fig.colorbar(Q_22, label='$dB_y (\mu T)$', ax=ax2, pad=0.1)
        ax2.set_title("$dB_y$")

        Q_19 = ax3.scatter(data['x'], data['y'], data['z'],c=data['dB_z'], s=s_set,
                           alpha=1, cmap=cm.PuOr, vmin=Zvmin, vmax=Zvmax)
        cbar_19 = fig.colorbar(Q_19, label='$dB_z (\mu T)$', ax=ax3, pad=0.1)
        ax3.set_title("$dB_z$")

    else:

        Q_19 = ax1.scatter(data['x'], data['y'], data['z'],c=data['B_x'], s=s_set, 
                           alpha=1, cmap=cm.PiYG)
        
        cbar_19 = fig.colorbar(Q_19, label='$B_x (\mu T)$', ax=ax1, pad=0.1)
        ax1.set_title("$B_x$")

        Q_22 = ax2.scatter(data['x'], data['y'], data['z'],c=data['B_y'], s=s_set,
                           alpha=1, cmap=cm.PRGn)
        cbar_22 = fig.colorbar(Q_22, label='$B_y (\mu T)$', ax=ax2, pad=0.1)
        ax2.set_title("$B_y$")

        Q_19 = ax3.scatter(data['x'], data['y'], data['z'],c=data['B_z'], s=s_set,
                           alpha=1, cmap=cm.PuOr)
        cbar_19 = fig.colorbar(Q_19, label='$B_z (\mu T)$', ax=ax3, pad=0.1)
        ax3.set_title("$B_z$")
        
    for a in axes:
        a.view_init(elev=elev_set, azim=azim_set)
        a.set_xlabel('x [cm]', labelpad=8)
        a.set_ylabel('y [cm]', labelpad=12)
        a.set_zlabel('z [cm]', labelpad=8)
        
    fig.tight_layout(pad=1)#,rect=[0, 0, 1, 0.99])# plt.colorbar(sc, ax=ax4)
    return
        
''''
Plots a slice of the data in 3D, with each component of the field plotted on a 
different graph with a different colorbar.
Which ever entry of slicer=[x,y,z] is what the slice will be done on. The value must be exact for now
'''
def PlotComponentsSlice(data, slicer=[None, None, None], Compare=False, fsize=(14,5), lims=None, title=None, elev_set=30., azim_set=None):
    
    # ### Producing the plots
    # plt.rcParams['font.size'] = '12'
    fig = plt.figure(facecolor='white', figsize=fsize)

    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132, projection='3d')
    ax3 = fig.add_subplot(133, projection='3d')
    
    if lims is not None:
        Xvmin, Xvmax = lims[0]
        Yvmin, Yvmax = lims[1]
        Zvmin, Zvmax = lims[2]
    else:
        Xvmin, Xvmax = [None,None]
        Yvmin, Yvmax = [None,None]
        Zvmin, Zvmax = [None,None]

    for axi in [ax1, ax2, ax3]:
        axi.view_init(elev=elev_set, azim=azim_set) # you may need to adjsut it for better data visibility   

        axi.set_xticklabels(axi.get_xticks(),  rotation=40,
                        verticalalignment='baseline',
                        horizontalalignment='center')
        axi.tick_params(pad=13) 
        axi.set_yticklabels(axi.get_yticks(),  rotation=-25,
                        verticalalignment='baseline',
                        horizontalalignment='center')    

        axi.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        axi.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        
        if slicer[0] is not None:
            axi.set_xlabel('$\mathsf{z}$ (cm)', rotation=7, labelpad=10)
            axi.set_ylabel('$\mathsf{y}$ (cm)',  labelpad=10)
        elif slicer[1] is not None:
            axi.set_xlabel('$\mathsf{x}$ (cm)', rotation=7, labelpad=10)
            axi.set_ylabel('$\mathsf{z}$ (cm)',  labelpad=10)
        elif slicer[2] is not None:
            axi.set_xlabel('$\mathsf{x}$ (cm)', rotation=7, labelpad=10)
            axi.set_ylabel('$\mathsf{y}$ (cm)',  labelpad=22)
            
    di = 1 #cm
    if slicer[0] is not None:
        cols = np.array(['z', 'y'])
        # mask = data['x'].isin(slicer)
        mask = data['x'].between(slicer[0]-di, slicer[0]+di)
        actualValue = data['x'][mask]
        title_slice = f'x = {actualValue.iloc[0]:.1f}'
        checkSlice = len(actualValue.unique())
    elif slicer[1] is not None:
        cols = np.array(['x', 'z'])
        # mask = data['y'].isin(slicer)
        mask = data['y'].between(slicer[1]-di, slicer[1]+di)
        actualValue = data['y'][mask]
        title_slice = f'y = {actualValue.iloc[0]:.1f}'
        checkSlice = len(actualValue.unique())
        
    elif slicer[2] is not None:
        cols = np.array(['x', 'y'])
        # mask = data['z'].isin(slicer)
        # search = slicer[2] + 2
        # print(-search,search)
        mask = data['z'].between(slicer[2]-di, slicer[2]+di)
        actualValue = data['z'][mask]
        title_slice = f'z = {actualValue.iloc[0]:.1f}'
        checkSlice = len(actualValue.unique())
        
    if checkSlice != 1 :
        print("Warning, either no data was found for that slice value, or multiple layers of points were saved")
            
    col_Name = np.array(['a', 'b'])
    
    if Compare:
        cols = np.append(cols, ['dB_x', 'dB_y', 'dB_z'])
        col_Name = np.append(col_Name, ['dB_x', 'dB_y', 'dB_z'])
    else:
        cols = np.append(cols, ['B_x', 'B_y', 'B_z'])
        col_Name = np.append(col_Name, ['B_x', 'B_y', 'B_z'])
        
    plot_data = pd.DataFrame(data=data[cols]).loc[mask]
    plot_data.columns = col_Name

    if Compare:
        
        Q_19 = ax1.scatter(plot_data['a'], plot_data['b'], plot_data['dB_x'],c=plot_data['dB_x'], s=1,
                           alpha=1, cmap=cm.PiYG, vmin=Xvmin, vmax=Xvmax)
        # cbar_19 = fig.colorbar(Q_19, label='$dB_x (\mu T)$', ax=ax1, pad=0.1)
        ax1.set_title("$dB_x$")

        Q_22 = ax2.scatter(plot_data['a'], plot_data['b'], plot_data['dB_y'],c=plot_data['dB_y'], s=1, 
                           alpha=1, cmap=cm.PRGn, vmin=Yvmin, vmax=Yvmax)
        # cbar_22 = fig.colorbar(Q_22, label='$dB_y (\mu T)$', ax=ax2, pad=0.1)
        ax2.set_title("$dB_y$")

        Q_19 = ax3.scatter(plot_data['a'], plot_data['b'], plot_data['dB_z'],c=plot_data['dB_z'], s=1, 
                           alpha=1, cmap=cm.PuOr, vmin=Zvmin, vmax=Zvmax)
        # cbar_19 = fig.colorbar(Q_19, label='$dB_z (\mu T)$', ax=ax3, pad=0.1)
        ax3.set_title("$dB_z$")

    else:
         #  'Perceptually Uniform Sequential',
             # ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        Q_19 = ax1.scatter(plot_data['a'], plot_data['b'], plot_data['B_x'],c=plot_data['B_x'], s=1, 
                           alpha=1, cmap=cm.viridis)
        
        # cbar_19 = fig.colorbar(Q_19, label='$B_x (\mu T)$', ax=ax1, pad=0.1)
        ax1.set_title("$B_x$")

        Q_22 = ax2.scatter(plot_data['a'], plot_data['b'], plot_data['B_y'],c=plot_data['B_y'], s=1, 
                           alpha=1, cmap=cm.inferno)
        # cbar_22 = fig.colorbar(Q_22, label='$B_y (\mu T)$', ax=ax2, pad=0.1)
        ax2.set_title("$B_y$")

        Q_19 = ax3.scatter(plot_data['a'], plot_data['b'], plot_data['B_z'],c=plot_data['B_z'], s=1, 
                           alpha=1, cmap=cm.cividis)
        # cbar_19 = fig.colorbar(Q_19, label='$B_z (\mu T)$', ax=ax3, pad=0.1)
        ax3.set_title("$B_z$")
    
    ax1.set_zlabel('$\mathsf{B_x\,(\mu T)}$', rotation=180, labelpad=22)
    ax2.set_zlabel('$\mathsf{B_y\,(\mu T)}$', rotation=180, labelpad=22)
    ax3.set_zlabel('$\mathsf{B_z\,(\mu T)}$', rotation=180, labelpad=28)

    fig.suptitle(f'{title}, slice at {title_slice} cm')
    fig.tight_layout(pad=3,rect=[0, 0, 1, 0.99])# plt.colorbar(sc, ax=ax4)

    
    ''''
Plots a slice of the data in 2D as a heat map, with each component of the field plotted on a 
different graph with a different colorbar.
Which ever entry of slicer=[x,y,z] is what the slice will be done on. The value must be exact for now.
'''
def PlotComponentsSliceHeat(data, slicer=[None, None, None], Compare=False, fsize=(20,6), lims=None, title=None):
    
    # ### Producing the plots
    # plt.rcParams['font.size'] = '12'
    fig = plt.figure(facecolor='white', figsize=fsize)

    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    
    if lims is not None:
        Xvmin, Xvmax = lims[0]
        Yvmin, Yvmax = lims[1]
        Zvmin, Zvmax = lims[2]
    else:
        Xvmin, Xvmax = [None,None]
        Yvmin, Yvmax = [None,None]
        Zvmin, Zvmax = [None,None]

      
    di = 1 #cm
    if slicer[0] is not None:
        cols = np.array(['z', 'y'])
        mask = data['x'].between(slicer[0]-di, slicer[0]+di)
        actualValue = data['x'][mask]
        title_slice = f'x = {actualValue.iloc[0]:.1f}'
        checkSlice = len(actualValue.unique())
    elif slicer[1] is not None:
        cols = np.array(['x', 'z'])
        mask = data['y'].between(slicer[1]-di, slicer[1]+di)
        actualValue = data['y'][mask]
        title_slice = f'y = {actualValue.iloc[0]:.1f}'
        checkSlice = len(actualValue.unique())
    elif slicer[2] is not None:
        cols = np.array(['x', 'y'])
        mask = data['z'].between(slicer[2]-di, slicer[2]+di)
        actualValue = data['z'][mask]
        title_slice = f'z = {actualValue.iloc[0]:.1f}'
        checkSlice = len(actualValue.unique())
        
    col_Name = np.array(['a', 'b'])
    
    if Compare:
        cols = np.append(cols, ['dB_x', 'dB_y', 'dB_z'])
        col_Name = np.append(col_Name, ['dB_x', 'dB_y', 'dB_z'])
    else:
        cols = np.append(cols, ['B_x', 'B_y', 'B_z'])
        col_Name = np.append(col_Name, ['B_x', 'B_y', 'B_z'])
        
    plot_data = pd.DataFrame(data=data[cols]).loc[mask]
      
    plot_data.columns = col_Name

    if Compare:
               
        df_B_x = plot_data.pivot_table( index='b', columns='a', values='dB_x')
        # q = sns.heatmap(df_B_x, ax=ax1, xticklabels=10, yticklabels=10, cmap=cm.PiYG, vmin=Xvmin, vmax=Xvmax)
        q = sns.heatmap(df_B_x, ax=ax1, xticklabels=10, yticklabels=10, cmap=cm.RdPu_r, vmin=Xvmin, vmax=Xvmax)
        
        
        df_B_y = plot_data.pivot_table( index='b', columns='a', values='dB_y')
        # q = sns.heatmap(df_B_y, ax=ax2, xticklabels=10, yticklabels=10, cmap=cm.PRGn, vmin=Yvmin, vmax=Yvmax)
        q = sns.heatmap(df_B_y, ax=ax2, xticklabels=10, yticklabels=10, cmap=cm.PuBuGn, vmin=Yvmin, vmax=Yvmax)
        
        
        df_B_z = plot_data.pivot_table( index='b', columns='a', values='dB_z')
        # q = sns.heatmap(df_B_z, ax=ax3, xticklabels=10, yticklabels=10, cmap=cm.PuOr, vmin=Zvmin, vmax=Zvmax)
        q = sns.heatmap(df_B_z, ax=ax3, xticklabels=10, yticklabels=10, cmap=cm.Purples, vmin=Zvmin, vmax=Zvmax)
        
        
        ax1.set_title('$\mathsf{dB_x\, [\mu T]}$') 
        ax2.set_title('$\mathsf{dB_y\, [\mu T]}$')
        ax3.set_title('$\mathsf{dB_z\, [\mu T]}$')

    else:
        df_B_x = plot_data.pivot_table( index='b', columns='a', values='B_x')
        q = sns.heatmap(df_B_x, ax=ax1, xticklabels=10, yticklabels=10, cmap=cm.viridis, linewidths=0, square=True)
        
        df_B_y = plot_data.pivot_table( index='b', columns='a', values='B_y')
        q = sns.heatmap(df_B_y, ax=ax2, xticklabels=10, yticklabels=10, cmap=cm.inferno, linewidths=0, square=True)
        
        df_B_z = plot_data.pivot_table( index='b', columns='a', values='B_z')
        q = sns.heatmap(df_B_z, ax=ax3, xticklabels=10, yticklabels=10, cmap=cm.cividis, linewidths=0, square=True)
        
        ax1.set_title('$\mathsf{B_x\, [\mu T]}$') 
        ax2.set_title('$\mathsf{B_y\, [\mu T]}$')
        ax3.set_title('$\mathsf{B_z\, [\mu T]}$')

    for axi in [ax1, ax2, ax3]:

        # format text labels
        fmt = '{:0.1f}'
        xticklabels = []
        for item in axi.get_xticklabels():
            item.set_text(fmt.format(float(item.get_text())))
            xticklabels += [item]
        yticklabels = []
        for item in axi.get_yticklabels():
            item.set_text(fmt.format(float(item.get_text())))
            yticklabels += [item]

        # axi.set_xticklabels(xticklabels)
        axi.set_yticklabels(yticklabels)
        axi.set_xlabel(f"{cols[0]} [cm]")
        axi.set_ylabel(f"{cols[1]} [cm]")
        axi.set_xticklabels(xticklabels,  rotation=0)
                # verticalalignment='baseline',
                # horizontalalignment='right')
    
    
    fig.suptitle(f'{title}, slice at {title_slice} cm')
    fig.tight_layout(pad=1,rect=[0, 0, 1, 0.99])# plt.colorbar(sc, ax=ax4)
