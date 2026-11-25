import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



## TEST 1 ##
# data = pd.read_csv("C:/Users/rongu/Downloads/AlSi10Mg 1.csv")
# csa = 35.9951 ## cross-sectional area in mm^2
# l0 = 3.39 ## starting length between the two lines in mm

## TEST 2 ##
# data = pd.read_csv("C:/Users/rongu/Downloads/AlSi10Mg 2.csv")
# csa = 35.8092 ## cross-sectional area in mm^2
# l0 = 9.27 ## starting length between the two lines in mm

## TEST 3 ##
# data = pd.read_csv("C:/Users/rongu/Downloads/AlSi10Mg 3.csv")
# csa = 36.039  ## cross-sectional area in mm^2
# l0 = 10.54 ## starting length between the two lines in mm


## TEST 4 ##
# data = pd.read_csv("C:/Users/rongu/Downloads/AlSi10Mg 0.001inps.csv")
# csa = 35.9951  ## cross-sectional area in mm^2
# l0 = 23.53 ## starting length between the two lines in mm


## TEST 5 ##
data = pd.read_csv("C:/Users/rongu/Downloads/AlSi10Mg 0.001inps 1000lbs clamp force.csv")
csa = 35.2787 ## cross-sectional area in mm^2
l0 = 26.97 ## starting length between the two lines in mm


t = np.array(data.RunningTime) ## seconds
d = np.array(data.AxialDisplacement) ## mm
f = np.array(data.AxialForce) ## Newtons
s = np.array(data.AxialStrain) ## %


stress = f/csa
strain = l0*s/(l0*100)

plt.plot(strain,stress)
plt.title('Test 5')
plt.xlabel("Strain")
plt.ylabel("Stress (MPa)")


