from mpl_toolkits.mplot3d import Axes3D
from const import *
from getdata import *
from process import *
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import timeit


plt.rcParams['figure.figsize'] = 15, 10
cx = [0.,0.]
cz = [0.1,0.3]


t=int(sys.argv[1])
pfad = raw_input('Pfad zum Output-Ordner?')
if  os.path.isfile(pfad+'/params.txt') :
    par = pfad+'/params.txt'
    print par
    radius,gdims_x,gdims_y,gdims_z,dt,dx,npatch=load_params(par)
elif os.path.isfile(pfad+'/Params.txt') :
    par = pfad+'/Params.txt'
    print par
    radius,gdims_x,gdims_y,gdims_z,dt,dx,npatch=load_params(par)
else: print "no parameter file found"

"""try:
    p = open(par, 'r')
    params = p.read()
    params = params.split()
    radius = int(params[0])
    gdims_x = int(params[1])
    gdims_y = int(params[2])
    gdims_z = int(params[3])
    dt = float(params[4])
    dx = float(params[5])
    np = int(params[6])
    print dt,dx,radius,gdims_x,gdims_z
    except:
    print "parameter file invalid"""

size = [gdims_x+1,gdims_z+1]

Qtot=0
proton = [[],[],[],[],[],[],[]]
carbon = [[],[],[],[],[],[],[]]
#carbon = np.zeros(shape=(7,N))
electron = [[],[],[],[],[],[],[]]
print proton
print electron

namestr = raw_input('Unter welchem Namen Speichern? ')
format = '0'
while (format!='a' and format!='s' and format!='c'):
    format = raw_input('Input format? (s for spread, c for compact, a for asc) ')

start = timeit.default_timer()

if(format == 's' or format == 'c'):
    
    """global kindarr
        global pxarr
        global pyarr
        global pzarr
        global yarr
        global xarr
        global zarr"""
    
    kindarr = []
    xarr = []
    yarr = []
    zarr = []
    pxarr = []
    pyarr = []
    pzarr = []
    
    if(format == 's'):
        for i in range(0,npatch):
            kindarr = np.concatenate((kindarr,get_arr(t,i,'kind',pfad)))
            print kindarr.shape
            xarr =  np.concatenate((xarr,get_arr(t,i,'x',pfad)))
            print xarr.shape
            yarr = np.concatenate((yarr,get_arr(t,i,'y',pfad)))
            zarr = np.concatenate((zarr,get_arr(t,i,'z',pfad)))
            pxarr =  np.concatenate((pxarr,get_arr(t,i,'px',pfad)))
            pyarr =  np.concatenate((pyarr,get_arr(t,i,'py',pfad)))
            pzarr =  np.concatenate((pzarr,get_arr(t,i,'pz',pfad)))

    if(format == 'c'):
        for i in range(0,npatch):
            kindarr = np.concatenate((kindarr,get_compact(t,i,'kind',pfad)))
            #print kindarr.shape
            xarr =  np.concatenate((xarr,get_compact(t,i,'x',pfad)))
            #print xarr.shape
            yarr = np.concatenate((yarr,get_compact(t,i,'y',pfad)))
            zarr = np.concatenate((zarr,get_compact(t,i,'z',pfad)))
            pxarr =  np.concatenate((pxarr,get_compact(t,i,'px',pfad)))
            pyarr =  np.concatenate((pyarr,get_compact(t,i,'py',pfad)))
            pzarr =  np.concatenate((pzarr,get_compact(t,i,'pz',pfad)))


    N = kindarr.size
    print 'kindarr.size ',N, 'px.size ',pxarr.size, 'pz.size ',pzarr.size, 'z.size ',zarr.size
    for i in range(0,N):
        if kindarr[i]==1:
            Qtot+=1
            proton[0]+=[xarr[i]]
            #print proton
            proton[1]+=[yarr[i]]
            #print proton
            proton[2]+=[zarr[i]]
            #print proton
            proton[3]+=[pxarr[i]]
            #print proton
            proton[4]+=[pyarr[i]]
            #print proton
            proton[5]+=[pzarr[i]]
            #print proton
            proton[6]+=[get_en(pxarr[i],pyarr[i],pzarr[i],mp)]
        #print proton
        elif kindarr[i]==0:
            Qtot-=1
            electron[0]+=[xarr[i]]
            electron[1]+=[yarr[i]]
            electron[2]+=[zarr[i]]
            electron[3]+=[pxarr[i]]
            electron[4]+=[pyarr[i]]
            electron[5]+=[pzarr[i]]
            electron[6]+=[get_en(pxarr[i],pyarr[i],pzarr[i],me)]
        elif kindarr[i]==2:
            Qtot+=6
            carbon[0]+=[xarr[i]]
            carbon[1]+=[yarr[i]]
            carbon[2]+=[zarr[i]]
            carbon[3]+=[pxarr[i]]
            carbon[4]+=[pyarr[i]]
            carbon[5]+=[pzarr[i]]
            carbon[6]+=[get_en(pxarr[i],pyarr[i],pzarr[i],mp*1836)]
#print carbon

elif(format == 'a'):
    arr =np.zeros((7,1))
    for i in range(0,npatch):
        print 'arr', arr.shape
        arr=np.hstack((arr,np.transpose(get_asc(t,i,pfad))))
    Qtot = sum(arr[6,:])
    print 'Otot=',Qtot
    N=arr.shape[1]
    for i in range(0,N):
        if arr[6,i]==1:
            proton[0]+=[arr[0,i]]
            #print proton
            proton[1]+=[arr[1,i]]
            #print proton
            proton[2]+=[arr[2,i]]
            #print proton
            proton[3]+=[arr[3,i]]
            #print proton
            proton[4]+=[arr[4,i]]
            #print proton
            proton[5]+=[arr[5,i]]
            #print proton
            proton[6]+=[get_en(arr[3,i],arr[4,i],arr[5,i],mp)]
        #print proton
        elif arr[6,i]==-1:
            electron[0]+=[arr[0,i]]
            electron[1]+=[arr[1,i]]
            electron[2]+=[arr[2,i]]
            electron[3]+=[arr[3,i]]
            electron[4]+=[arr[4,i]]
            electron[5]+=[arr[5,i]]
            electron[6]+=[get_en(arr[3,i],arr[4,i],arr[5,i],me)]
        elif int(arr[6,i])==1836:
            carbon[0]+=[arr[0,i]]
            carbon[1]+=[arr[1,i]]
            carbon[2]+=[arr[2,i]]
            carbon[3]+=[arr[3,i]]
            carbon[4]+=[arr[4,i]]
            carbon[5]+=[arr[5,i]]
            carbon[6]+=[get_en(arr[3,i],arr[4,i],arr[5,i],mp*1836)]



proton = np.array(proton)
print proton.shape
electron = np.array(electron)
carbon = np.array(carbon)
print electron.shape
stop = timeit.default_timer()
print 'processing time:',stop - start
start = timeit.default_timer()

def fil1(arr,i,limx,limz):
     if (arr[0][i]<limx) and (arr[2][i]>limz): return False
     else: return True

newel=[[],[],[]]
newpro=[[],[],[]]
"""for i in range(0,carbon.shape[1]):
    if fil(carbon,i,75.,75.):
        newcar[0]+=[carbon[0][i]]
        newcar[1]+=[carbon[1][i]]
        newcar[2]+=[carbon[2][i]]
"""
for i in range(0,electron.shape[1]):
     if fil1(electron,i,75.,75.):
         newel[0]+=[electron[0][i]]
         newel[1]+=[electron[1][i]]
         newel[2]+=[electron[2][i]]

for i in range(0,proton.shape[1]):
     if fil1(proton,i,75.,75.):
         newpro[0]+=[proton[0][i]]
         newpro[1]+=[proton[1][i]]
         newpro[2]+=[proton[2][i]]

stop = timeit.default_timer()
print 'cutting time:',stop - start

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(newel[0],newel[1],newel[2],alpha=0.001)
plt.savefig('newel.png')
plt.hold(True)
ax.scatter(newpro[0],newpro[1],newpro[2],alpha=0.01)
plt.savefig('newpro.png')
plt.hold(True)
ax.scatter(carbon[0],carbon[1],carbon[2],alpha=0.01)

ax.set_xlabel('Z')
ax.set_ylabel('Y')
ax.set_zlabel('X')
plt.savefig('all.png')
plt.show()