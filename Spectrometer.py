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
    
def AttenuatedEmit(colorX,colorY,color='blue'):
    ''' This function takes output from the savsmooth function for each LED color 
    as arguements, plots the attenuated emission for that color LED over a range of
    10 concentraitons, and returns the polyAbs, monoAbs, and concList'''
    
    concList=np.arange(0,11,1)
    monoAbs=np.zeros(len(concList))
    polyAbs=np.zeros(len(concList))
    P0= np.trapz(blueY)
    path=1
    concIndex=0
    for conc in concList:
        sampleAbsorbance=absY*conc*path
        transmittance=10**-(sampleAbsorbance)
        attenuatedSource=colorY*transmittance
        P= np.trapz(attenuatedSource)
        ax2.plot(colorX,attenuatedSource,color,ls=':')
        monoAbs[concIndex]=np.max(sampleAbsorbance)
        polyAbs[concIndex]=-np.log10(P/P0)
        concIndex=concIndex+1 
    return polyAbs,monoAbs, concList


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
ax1.plot(absX,absY, color='orange')
ax1.set_xlabel('wavelength (nm)')
ax1.set_ylabel('Absorbance', color='orange')
ax1.tick_params('y', colors='orange')

ax2 = ax1.twinx()
blueX, blueY = savsmooth(wl,'blue')
greenX, greenY = savsmooth(wl, 'green')
bgX, bgY = savsmooth(wl, 'bluegreen')
orangeX, orangeY = savsmooth(wl, 'orange')
whiteX, whiteY = savsmooth(wl, 'white') 
yellowX,yellowY = savsmooth(wl, 'yellow') 
redX, redY = savsmooth(wl, 'red')

ax2.plot(blueX,blueY, color='blue')
ax2.plot(greenX,greenY, color='green')
ax2.plot(bgX,bgY, color='c')
ax2.plot(orangeX,orangeY, color = 'orange')
ax2.plot(whiteX,whiteY, color = 'k')
ax2.plot(yellowX,yellowY, color = 'y')
ax2.plot(redX,redY, color = 'r')

ax2.set_ylabel('Intensity')

fig.tight_layout()
plt.show()


#Access Attenuated emission data for each color LED
polyAbs_blue, monoAbs_blue, concList_blue = AttenuatedEmit(blueX,blueY,':b')
polyAbs_green, monoAbs_green, concList_green = AttenuatedEmit(greenX, greenY, color = ':g')
polyAbs_bg, monoAbs_bg, concList_bg = AttenuatedEmit(bgX, bgY, color = ':c') 
polyAbs_orange, monoAbs_orange, concList_orange = AttenuatedEmit(orangeX, orangeY, color = 'orange')  
polyAbs_white, monoAbs_white, concList_white = AttenuatedEmit(whiteX, whiteY, color = ':k')  
polyAbs_yellow, monoAbs_yellow, concList_yellow = AttenuatedEmit(yellowX, yellowY, color = ':y')  
polyAbs_red, monoAbs_red, concList_red = AttenuatedEmit(redX, redY, color = ':r')  


# use the PolyReg function to fit the polychromatic absorbance to a second order  
fit2=PolyReg(concList_blue[concList_blue<=3],polyAbs_blue[concList_blue<=3],2)
fit1=PolyReg(concList_blue,polyAbs_blue,2)
fit3=PolyReg(concList_green,polyAbs_green,2)
fit4=PolyReg(concList_bg,polyAbs_bg,2)
fit5=PolyReg(concList_orange,polyAbs_orange,2)
fit6=PolyReg(concList_white,polyAbs_white,2)
fit7=PolyReg(concList_yellow,polyAbs_yellow,2)
fit8=PolyReg(concList_red,polyAbs_red,2)


# plot the data points (polyAbs), and the fit of the polychromatic,
# and the monochromatic absorbaces
plt.figure(2) 
ax1 = plt.subplot()
ax1.plot(concList_blue, polyAbs_blue, 'ob')
ax1.plot(concList_blue, fit1['poly'](concList_blue),'b')

ax1.plot(concList_green, polyAbs_green, 'og') 
ax1.plot(concList_green, fit3['poly'](concList_green),'g')

ax1.plot(concList_bg, polyAbs_bg, 'oc') 
ax1.plot(concList_bg, fit4['poly'](concList_bg),'c')

ax1.plot(concList_orange, polyAbs_orange,'orange',marker='o') 
ax1.plot(concList_orange, fit5['poly'](concList_orange),'orange')

ax1.plot(concList_white, polyAbs_white, 'ok') 
ax1.plot(concList_white, fit6['poly'](concList_white),'k')

ax1.plot(concList_yellow, polyAbs_yellow,'yellow',marker='o') 
ax1.plot(concList_yellow, fit7['poly'](concList_yellow),'yellow')

ax1.plot(concList_red, polyAbs_red, 'or') 
ax1.plot(concList_red, fit8['poly'](concList_red),'r')

ax1.plot(concList_blue, monoAbs_blue, 'k')

# annotate the polychromatic light fit
AnnotateFit(fit2,ax1,color='blue')
AnnotateFit(fit3,ax1,color ='green',xText=0.1, yText=0.8)
AnnotateFit(fit4,ax1,color ='c',xText=0.1, yText=0.7)
AnnotateFit(fit5,ax1,color ='orange',xText=0.1, yText=0.6)
AnnotateFit(fit6,ax1,color ='k',xText=0.1, yText=0.5)
AnnotateFit(fit7,ax1,color ='yellow',xText=0.1, yText=0.4)
AnnotateFit(fit8,ax1,color ='red',xText=0.1, yText=0.3)

# label figure
ax1.set_ylabel('Absorbance')
ax1.set_xlabel('Concentration')
ax1.set_title('Calibration')
plt.show()



