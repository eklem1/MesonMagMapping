# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to make a 3d vector plot of the b-field
Original Created on Tue Sep 25 09:24:46 2019
@author: fpiermaier
modified by Mark McCrea 2020_02_14
"""

import pandas as pd
import numpy as np
import matplotlib

from matplotlib import pyplot as plt
matplotlib.use('QT5Agg')
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import mpl_toolkits.mplot3d.art3d as art3d


from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as patches

import scipy.interpolate as interp


# %%
#---IMPORT DATA---#
#Jan29-Feb2 data sets
df1 = pd.read_csv('Data-Meson_hall_maps/20200201_1026_Feb01_map_avg.csv')
df2 = pd.read_csv('Data-Meson_hall_maps/20200201_1356_Feb01_map_02_avg.csv')
df3 = pd.read_csv('Data-Meson_hall_maps/20200202_1119_Feb02_map01_avg.csv')

dfn_all = df1.append(df2)
dfn_all = dfn_all.append(df3)

#offsets from measurement coordinates system center to center of MSR (to be added)
#Note: update axn axis limits when updating the center points
dfn_all['x'] = dfn_all.u
dfn_all['y'] = dfn_all.v
dfn_all['z'] = dfn_all.w
dfn_all['B_x'] = dfn_all['B_u']*100
dfn_all['B_y'] = dfn_all['B_v']*100
dfn_all['B_z'] = dfn_all['B_w']*100

dfn_floor = dfn_all[dfn_all.z==dfn_all['z'].min()]

xn_all = dfn_all.x.unique()
yn_all = dfn_all.y.unique()
zn_all = dfn_all.z.unique()
zn_max = np.max(dfn_all.z)
zn_min = np.min(dfn_all.z)

# %%
#---QUIVER PLOT---#

# new
fign = plt.figure()
axn = fign.add_subplot(111, projection='3d')
# Color by length of vector
cn = np.sqrt(dfn_all['B_x']**2+dfn_all['B_y']**2+dfn_all['B_z']**2)
# Flatten and normalize
cn = (cn.ravel() - cn.min()) / np.ptp(cn)
# Repeat for each body line and two head lines
cn = np.concatenate((cn, np.repeat(cn, 2)))
# Colormap
cn = plt.cm.plasma(cn)
qn = axn.quiver(dfn_all['x'], dfn_all['y'], dfn_all['z'], dfn_all['B_x'], dfn_all['B_y'], dfn_all['B_z'], colors=cn, length=0.2)
axn.set_xlabel('X axis')
axn.set_ylabel('Y axis')
axn.set_zlabel('Z axis')
axn.set_xlim(-200, 200)
axn.set_ylim(-360, 200)
axn.set_zlim(000, 350)
fign.tight_layout(pad=3,rect=[0, 0, 1, 0.99])
plt.show()

# new floor
fln = plt.figure()
axfn = fln.add_subplot(111, projection='3d')
# Color by length of vector
cfn = np.sqrt(dfn_floor['B_x']**2+dfn_floor['B_y']**2+dfn_floor['B_z']**2)
# Flatten and normalize
cfn = (cfn.ravel() - cfn.min()) / np.ptp(cfn)
# Repeat for each body line and two head lines
cfn = np.concatenate((cfn, np.repeat(cfn, 2)))
# Colormap
cfn = plt.cm.plasma(cfn)
qfn = axfn.quiver(dfn_floor['x'], dfn_floor['y'], dfn_floor['z'], dfn_floor['B_x'], 
                dfn_floor['B_y'], dfn_floor['B_z'], colors=cfn, cmap = cm.plasma, length=0.1)
axfn.set_xlabel('X axis (cm)')
axfn.set_ylabel('Y axis (cm)')
axfn.set_zlabel('Z axis (cm)')
axfn.set_xlim(-320, 200)
axfn.set_ylim(-350, 200)
axfn.set_zlim(-200, -140)
fln.tight_layout(pad=3,rect=[0, 0, 1, 0.99])
plt.show()
