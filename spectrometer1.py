
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter, tkinter.filedialog
from scipy.signal import savgol_filter


#smooth ydata and convert x-axis to evenly spcaed 1nm increments 
def savsmooth(xdata,ydata):
    yarray = np.array(data1[ydata])
    ysmooth=savgol_filter(yarray, 15, 2, deriv=0) 
    newX = np.arange(400,700,1)
    newY = np.zeros(newX.size)
    index=0 
    for wavelength in newX: 
        oldXBool = ((wl >= (wavelength - (1/2.0))) & (wl <= wavelength + (1/2.0)))
        newY[index]=np.average((ysmooth[oldXBool]))
        index=index+1
    
    return newX, newY
#root = tkinter.Tk()
#root.withdraw()
#file_path = tkinter.filedialog.askopenfilename()


#read data into pandas dataframe from selected file (CSV)


data1=pd.read_csv('LEDData.csv',names=['wavelength','absorptivity','blue','bluegreen','green','orange','white','yellow','red'],engine='python',skiprows=[0])
print(data1.head())


#plot wavelength vs absorptivity

wl = np.array(data1['wavelength'])

#make this a savsmooth function
oldY = np.array(data1['absorptivity']*5)

fig, ax1 = plt.subplots()
wl = np.array(data1['wavelength'])
oldY = np.array(data1['absorptivity'])

ax1.plot(wl,absmooth, color='orange')
ax1.set_xlabel('wavelength (nm)')
ax1.set_ylabel('Absorbance', color='orange')
ax1.tick_params('y', colors='orange')

ax2 = ax1.twinx()
blueX, blueY = savsmooth(wl,'blue')
ax2.plot(blueX,blueY, color='blue')
ax2.set_ylabel('Intensity', color='blue')
ax2.tick_params('y', colors='blue')

fig.tight_layout()
plt.show()

