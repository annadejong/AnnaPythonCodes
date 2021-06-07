#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 16:03:46 2021

@author: addejong
"""

import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import datetime as dt
import idlsave 
import matplotlib.cm as cm
import matplotlib.colors as mplc
import matplotlib as mpl
from matplotlib import lines
lines.lineStyles.keys()



gitm=idlsave.read('gitm_baselinecube_newion_smc.save')


glats=gitm.gitmdatacubelats
glons=gitm.gitmdatacubelons
galts=gitm.gitmdatacubealts
gdatatimes=gitm.gitmdatacubeUT
gjuldate=gitm.gitmdatacubejulian2000

#transpose to get in terms of times,lons,lats,alts
gtemp=np.transpose(gitm.gitmdatacubetemp)
gmlt=np.transpose(gitm.gitmdatacubemlt)
gmaglats=np.transpose(gitm.gitmdatacubemaglats)




#pick altitude
althigh=500.
altlow=200

#set geographics latitudes (must be large to get all MLTs)
latslow=40.
latshigh=90.

#set longitudes to get rid of wrapping elements 
lonlow=0.
lonhigh=360.

gtimelow=-1042.5
gtimeshigh=-1042.25

#set up new terms with out extra "stuff"

#new_temp=gtemp[0:72,2:110,132:182,43]

new_times=gjuldate[(gjuldate >= gtimelow ) & (gjuldate <= gtimeshigh)]
new_lats=glats[(glats > latslow) & (glats < latshigh)]
new_lons=glons[(glons > lonlow) & (glons < lonhigh)]
new_alts=galts[(galts > altlow) & (galts < althigh)]

nlats=len(new_lats)
nlons=len(new_lons)
nalts=len(new_alts)  #should be for this plotting 
ntimes=len(new_times)

#doy1=np.array([int(dt.datetime(y,m,d).strftime('%j')) for y, m, d in zip(y_ar1,m_ar1,d_ar1)])

#subset of Altitudes
new_mlts=gmlt[ :,:,:,0] # same for all Alt
new_maglats=gmaglats[ :,:,:,0]  #same for all alt
new_temp=gtemp[ :,:,:,(galts > altlow) & (galts < althigh)]

#subset of latitudes
new_mlts=new_mlts[:,:,(glats > latslow) & (glats < latshigh)]
new_maglats=new_maglats[:,:,(glats > latslow) & (glats < latshigh)]
new_temp=new_temp[:,:,(glats > latslow) & (glats < latshigh),:]


#subset of longitudes
new_mlts=new_mlts[:,(glons > lonlow) & (glons < lonhigh)]
new_maglats=new_maglats[:,(glons > lonlow) & (glons < lonhigh),:]
new_temp=new_temp[:,(glons > lonlow) & (glons < lonhigh),:,:]

#add subset of times if needed

mltplot=22




#reset the data into MLT and Maglat coordinates

nlatlon=nlats*nlons

plot_maglats=np.reshape(new_maglats,(ntimes,nlatlon))
plot_mlts=np.reshape(new_mlts, (ntimes,nlatlon))
plot_temp=np.reshape(new_temp, (ntimes,nlatlon,nalts))

#mlts out of GITM -12 to 12 change to 0 to 24
plot_mlts[plot_mlts < 0]=plot_mlts[plot_mlts <0]+24.

#maglats 90-50 steps of 0.5 then 80.
lat_plot=[80,75,70,65,60,55]
lat_plot_print=['80','75','70','65','60','50']

fig,ax=plt.subplots(6,1,figsize=(7,9))

#norm=mplc.Normalize(-25,25)

for i in range(6):
    
        
    plotdata1=np.ndarray(shape=(ntimes,nalts),dtype=float)
    pmaglats=np.ndarray(shape=(ntimes),dtype=float)
    pmlts=np.ndarray(shape=(ntimes),dtype=float)
    #pull out the data for the correct MLT to plot
   
    for x in range(ntimes):
      
        xmlt=plot_mlts[x,:]
        xmaglat=plot_maglats[x,:]
        xdata=plot_temp[x,:,:]
    
        pmaglats[x]=np.mean(xmaglat[(xmaglat >= lat_plot[i]-.64) & (xmaglat < lat_plot[i]+.44) & (xmlt <= mltplot+.23) & (xmlt > mltplot-.23)])
    
        pmlts[x]=np.mean(xmlt[(xmaglat >= lat_plot[i]-.63) & (xmaglat < lat_plot[i]+.43) & (xmlt <= mltplot+.23) & (xmlt > mltplot-.23) ])

        for y in range(nalts):
            plotdata1[x,y]=np.mean(xdata[(xmaglat >= lat_plot[i]-.63) & (xmaglat < lat_plot[i]+.43) & (xmlt <= mltplot+.23) & (xmlt > mltplot-.23),y])
       
        
       
   
    #ax[i].yaxis.set_major_locator(plt.MaxNLocator(5))
    ax[i].set_yticks([250,300,350,400,450,500])
    ax[i].set_ylabel('Altitude (km)')

    ax[i].xaxis.set_major_locator(plt.MaxNLocator(6))
    if i < 5:
       ax[i].set_xticks([])
    else:
       ax[i].set_xlabel('UT Time')
    
    
    zz=np.array(range(72))
    plotdata=np.transpose(plotdata1)
    cs=ax[i].contourf(zz,new_alts,plotdata,200,cmap=cm.rainbow,vmin=500,vmax=2000)
    
    #plt.imshow(np.flipud(np.transpose(plotdata1)))
   
    ax[i].text(30,505,'Mag Latitude: '+lat_plot_print[i],fontsize=10)
  
    
  

   
m=plt.cm.ScalarMappable(cmap=cm.rainbow)

m.set_clim(vmin=500,vmax=2000)

fig.subplots_adjust(right=0.80)
cbar_ax=fig.add_axes([0.85,0.35,0.02,0.3])
cbar=fig.colorbar(m,cax=cbar_ax)
cbar.set_label('Kelvin')


fig.text(.35,.94,'1997 02 23 (SMC)',fontsize=17)
fig.text(.25,.90,'Temperature',fontsize =12)
fig.text(.70,.90,'MLT: 22',fontsize=12)



plt.show()

fig.savefig('smc_python_test.jpg',dpi=300)