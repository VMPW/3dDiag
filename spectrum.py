import numpy as np
import matplotlib.pyplot as plt
import sys
import timeit
import math
import conv
from getdata import *
import part

plt.rcParams['figure.figsize'] = 12, 10
res = 1
cutoffx = 0.2
cutoffz = 0.2

dxphys=1.5625e-08
ppqp=9155. #1144.
nc=4096*[28.75*ppqp]

t=int(sys.argv[1])
#pfad = raw_input('Pfad zum Output-Ordner?')
pfad = sys.argv[2]

if  os.path.isfile(pfad+'/params.txt') :
    par = pfad+'/params.txt'
    print par
    radius,gdims_x,gdims_z,dt,dx,npatch=load_params2d(par)
elif os.path.isfile(pfad+'/Params.txt') :
    par = pfad+'/Params.txt'
    print par
    radius,gdims_x,gdims_z,dt,dx,npatch=load_params2d(par)
else: print "no parameter file found"

gridsize_x = gdims_x/res
gridsize_z = gdims_z/res

center=(512,1024)
size = [gdims_x+1,gdims_z+1]

R=radius/dxphys*1e-6
print R

zline=np.linspace(0,gdims_z,gdims_z+1)*dxphys*1e6
histp=[0]
#histo=[0]
log=[0]

start = timeit.default_timer()

kindarr = []
pxarr = []
pyarr = []
pzarr = []
zarr = []
xarr = []

#collecting input-data
for i in range(0,128):
    kindarr = np.concatenate((kindarr,get_arr(t,i,'kind',pfad)))
    xarr =  np.concatenate((xarr,get_arr(t,i,'x',pfad)))
    zarr = np.concatenate((zarr,get_arr(t,i,'z',pfad)))
    pxarr =  np.concatenate((pxarr,get_arr(t,i,'px',pfad)))
    pyarr =  np.concatenate((pyarr,get_arr(t,i,'py',pfad)))
    pzarr =  np.concatenate((pzarr,get_arr(t,i,'pz',pfad)))
print kindarr.size

proton = part.Data("proton",1,conv.mp,1.,size)

for i in range(0,kindarr.size):
    parttyp = kindarr[i]
    p = [int(xarr[i]*(1/dx)),int(zarr[i]*(1/dx)),pxarr[i],pyarr[i],pzarr[i]]
    if (parttyp == 1):
        Ek=proton.sort(p,radius,center)
        phas=proton.ang_sort(p,Ek)
        #histo+=[Ek]
        #phase+=[proton.ang_sort(p,Ek)]
        f=proton.r_cor(p,phas[0],Ek,R,center)
        log+=[f[0]]
        histp+=[f[1]]

stop = timeit.default_timer()

print np.average(histp),np.average(log),np.amax(log)

#phase=zip(*phase)

plt.hist(histp,bins=50,log=True,normed=False,alpha=0.6,color='red',facecolor='red')
plt.hist(proton.ekin,bins= 50,log=True,normed=False,alpha=0.2,color='yellow',facecolor='red')
#plt.hist(proton.econe,bins= 50,log=True,normed=False,alpha=0.1,color='blue',facecolor='blue')
#plt.text(6e7,0.5e4, 'total ion energy in cone: '+str(np.around(Etot/1e9,4))+'GeV\ntotal ion energy in box: '+str(np.around(sum(np.ravel(Ekinp)/1e9,4)))+'GeV\nelectron temperature:'+str(np.mean(Ekine))+'\nproton temperature:'+str(np.mean(Ekinp))+'\ncarbon temperature:'+str(np.mean(Ekinc)))
plt.xlim([0,1e8])
plt.ylim([0,1.5e4])
plt.xlabel("E")
plt.title("Energiespektrum (comparison)")
plt.ylabel("n")
plt.savefig('Images/Spectra/spectrum-comp'+str(t)+'r='+str(radius)+'.png')
plt.show()

#plt.hist(histp,bins=100,log=True,normed=False,alpha=0.6,color='red',facecolor='red')
#plt.hist(histo,bins= 100,log=True,normed=False,alpha=0.2,color='yellow',facecolor='red')
plt.hist(proton.ekin,bins= 50,log=True,normed=False,alpha=0.1,color='blue',facecolor='blue')
plt.hist(proton.econe,bins= 50,log=True,normed=False,alpha=0.4,color='blue',facecolor='blue')
#plt.text(6e7,0.5e4, 'total ion energy in cone: '+str(np.around(Etot/1e9,4))+'GeV\ntotal ion energy in box: '+str(np.around(sum(np.ravel(Ekinp)/1e9,4)))+'GeV\nelectron temperature:'+str(np.mean(Ekine))+'\nproton temperature:'+str(np.mean(Ekinp))+'\ncarbon temperature:'+str(np.mean(Ekinc)))
plt.xlim([0,1e8])
plt.ylim([0,1.5e4])
plt.xlabel("E")
plt.title("Energiespektrum (original)")
plt.ylabel("n")
plt.savefig('Images/Spectra/spectrum-norm-'+str(t)+'r='+str(radius)+'.png')
plt.show()

plt.hist(histp,bins=50,log=True,normed=False,alpha=0.6,color='red',facecolor='red')
#plt.hist(histo,bins= 100,log=True,normed=False,alpha=0.2,color='yellow',facecolor='red')
#plt.hist(proton.ekin,bins= 50,log=True,normed=False,alpha=0.1,color='blue',facecolor='blue')
plt.hist(proton.ecorcone,bins= 50,log=True,normed=False,alpha=0.2,color='blue',facecolor='blue')
#plt.text(6e7,0.5e4, 'total ion energy in cone: '+str(np.around(Etot/1e9,4))+'GeV\ntotal ion energy in box: '+str(np.around(sum(np.ravel(Ekinp)/1e9,4)))+'GeV\nelectron temperature:'+str(np.mean(Ekine))+'\nproton temperature:'+str(np.mean(Ekinp))+'\ncarbon temperature:'+str(np.mean(Ekinc)))
plt.xlim([0,0.3e8])
plt.ylim([0,1e4])
plt.xlabel("E")
plt.title("Energiespektrum (corrected)")
plt.ylabel("n")
plt.savefig('Images/Spectra/spectrum-cor-'+str(t)+'r='+str(radius)+'.png')
plt.show()