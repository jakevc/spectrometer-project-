#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 11:24:52 2017

@author: JakeVanCampen
"""

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

def PolyReg(X,Y,order):
    coef,cov=np.polyfit(X,Y,order,cov=True)
    N=float(len(X))
    df=N-len(coef)
    stdErrors=np.sqrt(np.diagonal(cov)*(df-2)/df)
    p=np.poly1d(coef)
    yfit=p(X)
    res=Y-yfit
    sy=np.sqrt( np.sum(res**2) / df )
    return {'coef':coef,'errors':stdErrors,'n':N,'sy':sy,'res':res,'poly':p}

def FormatSciUsingError(x,e,WithError=False,ExtraDigit=0):
    if abs(x)>=e:
        NonZeroErrorX=np.floor(np.log10(abs(e)))
        NonZeroX=np.floor(np.log10(abs(x)))
        formatCodeX="{0:."+str(int(NonZeroX-NonZeroErrorX+ExtraDigit))+"E}"
        formatCodeE="{0:."+str(ExtraDigit)+"E}"
    else:
        formatCodeX="{0:."+str(ExtraDigit)+"E}"
        formatCodeE="{0:."+str(ExtraDigit)+"E}"
    if WithError==True:
        return formatCodeX.format(x)+" (+/- "+formatCodeE.format(e)+")"
    else:
        return formatCodeX.format(x) 
    
def AnnotateFit(fit,axisHandle,annotationText='Eq',color='black',Arrow=False,xArrow=0,yArrow=0,xText=0.1,yText=0.9):
    c=fit['coef']
    e=fit['errors']
    t=len(c)
    if annotationText=='Eq':
        annotationText="y = "
        for order in range(t):
            exponent=t-order-1
            if exponent>=2:
                annotationText=annotationText+FormatSciUsingError(c[order],e[order])+"x$^{}$".format(exponent)+" + "
            elif exponent==1:
                annotationText=annotationText+FormatSciUsingError(c[order],e[order])+"x + "
            else:
                annotationText=annotationText+FormatSciUsingError(c[order],e[order])
        annotationText=annotationText+", sy={0:.1E}".format(fit['sy'])
    if (Arrow==True):
        if (xArrow==0):
            xSpan=axisHandle.get_xlim()
            xArrow=np.mean(xSpan)
        if (yArrow==0):    
            yArrow=fit['poly'](xArrow)
        annotationObject=axisHandle.annotate(annotationText, 
                xy=(xArrow, yArrow), xycoords='data',
                xytext=(xText, yText),  textcoords='axes fraction',
                arrowprops={'color': color, 'width':1, 'headwidth':5},
                bbox={'boxstyle':'round', 'edgecolor':color,'facecolor':'0.8'}
                )
    else:
        xSpan=axisHandle.get_xlim()
        xArrow=np.mean(xSpan)
        ySpan=axisHandle.get_ylim()
        yArrow=np.mean(ySpan)
        annotationObject=axisHandle.annotate(annotationText, 
                xy=(xArrow, yArrow), xycoords='data',
                xytext=(xText, yText),  textcoords='axes fraction',
                ha="left", va="center",
                bbox={'boxstyle':'round', 'edgecolor':color,'facecolor':'0.8'}
                )
    annotationObject.draggable()


#root = tkinter.Tk()
#root.withdraw()
#file_path = tkinter.filedialog.askopenfilename()


#read data into pandas dataframe from selected file (CSV)
data1=pd.read_csv('LEDData.csv',names=['wavelength','absorptivity','blue','bluegreen','green','orange','white','yellow','red'],engine='python',skiprows=[0])
print(data1.head())


#plot wavelength vs absorptivity

wl = np.array(data1['wavelength'])

absX,absY = savsmooth(wl, 'absorptivity')


fig, ax1 = plt.subplots()
wl = np.array(data1['wavelength'])

ax1.plot(absX,absY, color='orange')
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


# loop over some concentrations to calculate the attenuated
# emissionof the blue LED at a range of concentrations from
# 0 to 10ppm in 1ppm increments


concList=np.arange(0,11,1)
monoAbs=np.zeros(len(concList))
polyAbs=np.zeros(len(concList))
P0= np.trapz(blueY)
path=1
concIndex=0
for conc in concList:
    sampleAbsorbance=absY*conc*path
    transmittance=10**-(sampleAbsorbance)
    attenuatedSource=blueY*transmittance
    P= np.trapz(attenuatedSource)
    ax2.plot(blueX,attenuatedSource,':b')
    monoAbs[concIndex]=np.max(sampleAbsorbance)
    polyAbs[concIndex]=-np.log10(P/P0)
    concIndex=concIndex+1 

# use the PolyReg function to fit the polychromatic absorbance to a second order  
fit2=PolyReg(concList[concList<=3],polyAbs[concList<=3],2)
fit1=PolyReg(concList,polyAbs,2)

# plot the data points (polyAbs), and the fit of the polychromatic,
# and the monochromatic absorbaces
plt.figure(2) 
ax1 = plt.subplot()
ax1.plot(concList, polyAbs, 'ob')
ax1.plot(concList, fit1['poly'](concList),'b')
ax1.plot(concList, monoAbs, 'k')

# annotate the polychromatic light fit
AnnotateFit(fit2,ax1,color='blue')

# label figure
ax1.set_ylabel('Absorbance')
ax1.set_xlabel('Concentration')
ax1.set_title('Calibration')



