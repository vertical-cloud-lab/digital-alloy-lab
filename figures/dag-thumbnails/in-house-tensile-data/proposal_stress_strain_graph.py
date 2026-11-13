import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




data = pd.read_csv("C:/Users/rongu/Downloads/AlSi10Mg 0.001inps 1000lbs clamp force.csv")
csa = 35.2787 ## cross-sectional area in mm^2
l0 = 26.97 ## starting length between the two lines in mm


f = np.array(data.AxialForce) ## Newtons
s = np.array(data.AxialStrain) ## %


stress = f/csa
strain = l0*s/l0

plt.plot(strain,stress)
plt.xlabel("Strain (%)", fontsize = 15)
plt.ylabel("Stress (MPa)", rotation = 0, labelpad = 55, fontsize = 15)
plt.ylim(0)
plt.xticks([0,6], fontsize = 20)
plt.yticks([0,400],fontsize = 20)
