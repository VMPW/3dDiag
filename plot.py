from const import *
from getdata import *
from process import *
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from math import *
#from mpl_toolkits.mplot3dold import Axes3D
import mpl_toolkits

plt.rcParams['figure.figsize'] = 18, 10
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
    format = raw_input('Output format? (s for spread, c for compact, a for asc) ')
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
            #print kindarr.shape
            xarr =  np.concatenate((xarr,get_arr(t,i,'x',pfad)))
            #print xarr.shape
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
            carbon[6]+=[get_en(pxarr[i],pyarr[i],pzarr[i],mp)]
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
            carbon[6]+=[get_en(arr[3,i],arr[4,i],arr[5,i],mp)]

proton = np.array(proton)
print proton.shape
electron = np.array(electron)
carbon = np.array(carbon)
print electron.shape
#print proton
#print electron

up=(dx*gdims_x/2.)+2*dx
low=(dx*gdims_x/2.)-2*dx
print up
print low

"""
plt.suptitle('ions\n  Qges='+str(np.around(Qtot,3))+' e \n pulse maximum hits target in ' + str(200-(t*dt*1e15)) +'fs')
plt.subplot(2,2,1)
plt.imshow(np.log10(get_slice(1,carbon,gdims_y,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('y')
plt.title('s-polarisation, carbon density')
plt.colorbar(orientation=u'horizontal')
#plt.savefig('Images/'+namestr+'hist'+str(t)+'.png')

plt.subplot(2,2,2)
plt.imshow(np.transpose(get_detec(proton,mp)),extent=[-20,20,-20,20],interpolation='none',cmap=plt.get_cmap("OrRd"))
plt.xlabel('x')
plt.ylabel('y')
#plt.savefig(namestr+'detec'+str(t)+'.png')

plt.subplot(2,2,3)
plt.imshow(np.log10(get_slice_energy(0,proton,gdims_x,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('x')
plt.title('p-polarisation, protons total energy')
plt.colorbar(orientation=u'horizontal')
#plt.savefig(namestr+'xslice'+str(t)+'.png')

plt.subplot(2,2,4)
plt.imshow(np.log10(get_slice_energy(1,proton,gdims_y,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('y')
plt.title('s-polarisation, protons total energy')
plt.colorbar(orientation=u'horizontal')
plt.savefig('Images/'+namestr+'-Vierer-prot-'+str(t)+'.png')
plt.show()


plt.suptitle('electrons \n   Qges= '+str(np.around(Qtot,3))+'e \n pulse maximum hits target in ' + str(200-(t*dt*1e15)) +'fs')
plt.subplot(2,2,1)
plt.imshow(np.subtract(np.nan_to_num(np.log10(np.add(286.*get_slice(1,proton,gdims_y,gdims_z,dx,up,low),286*6.*get_slice(1,carbon,gdims_y,gdims_z,dx,up,low)))),np.nan_to_num(np.log10(286.*get_slice(1,electron,gdims_y,gdims_z,dx,up,low)))),cmap=plt.get_cmap("bwr"), vmin=-5,vmax=5, interpolation='bicubic')
plt.xlabel('z')
plt.ylabel('y')
plt.colorbar(orientation=u'horizontal')
plt.title('charge distribution')
#plt.savefig('Images/'+namestr+'charge'+str(t)+'.png')


plt.subplot(2,2,2)
plt.imshow(np.transpose(get_detec(electron,me)),extent=[-20,20,-20,20],interpolation='none',cmap=plt.get_cmap("OrRd"))
plt.xlabel('x')
plt.ylabel('y')
#plt.savefig(namestr+'detec'+str(t)+'.png')

plt.subplot(2,2,3)
plt.imshow(np.log10(get_slice(0,electron,gdims_x,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('x')
plt.colorbar(orientation=u'horizontal')
plt.title('p-polarisation')
#plt.savefig(namestr+'xslice'+str(t)+'.png')

plt.subplot(2,2,4)
plt.imshow(np.log10(get_slice(1,electron,gdims_y,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('y')
plt.title('s-polarisation')
plt.colorbar(orientation=u'horizontal')
plt.savefig('Images/'+namestr+'-Vierer-el-'+str(t)+'.png')
plt.show()
"""
conep=[[],[]]
conekin=[[],[]]

def filcone(arr,i,maxang):
    if fabs(get_angle(arr[3][i],arr[4][i],arr[5][i]))<maxang and fabs(get_anglexy(arr[3][i],arr[5][i]))<0.5: return True
    else: return False

for i in range(0,proton.shape[1]):
    if filcone(proton,i,18.):
        conep[0]+=[proton[2][i]]
        conep[1]+=[proton[5][i]]
        conekin[0]+=[proton[2][i]]
        conekin[1]+=[proton[6][i]]

plt.suptitle('Energy histograms\n \n pulse maximum hits target in ' + str(200-(t*dt*1e15)) +'fs')
plt.subplot(2,3,1)
plt.hist(get_sliceravel(0,proton,up,low),bins=20,log=True,normed=False)
plt.title('protons p-pol')

plt.subplot(2,3,2)
plt.hist(get_sliceravel(1,proton,up,low),bins=20,log=True,normed=False)
plt.title('protons s-pol')
#plt.savefig(namestr+'detec'+str(t)+'.png')

plt.subplot(2,3,3)
plt.hist(proton[6,:],bins=20,log=True,normed=False)
plt.title('protons all')
#plt.savefig(namestr+'xslice'+str(t)+'.png')

plt.subplot(2,3,4)
plt.hist(electron[6,:],bins=20,log=True,normed=False)
plt.title('electrons')

plt.subplot(2,3,5)
plt.hist(carbon[6,:],bins=20,log=True,normed=False)
plt.title('carbon all')
#plt.savefig(namestr+'phasespace'+str(t)+'.png')

plt.subplot(2,3,6)
plt.hist(conekin[1],bins=20,log=True,normed=False)
plt.title('proton forward cone')

plt.savefig('Images/'+namestr+'-hists'+str(t)+'.png')
plt.show()



plt.suptitle('Phase space protons\n \n pulse maximum hits target in ' + str(200-(t*dt*1e15)) +'fs')
plt.subplot(2,2,1)
plt.scatter(proton[2,:],proton[5,:],alpha=0.005)
plt.title('proton phase space (z momentum)')
plt.subplot(2,2,2)
plt.scatter(proton[2,:],proton[6,:],alpha=0.005)
plt.title('proton phase space (kin. energy)')
plt.subplot(2,2,3)
plt.scatter(conep[0],conep[1],alpha=0.05)
plt.title('proton phase space (z momentum)')
plt.subplot(2,2,4)
plt.scatter(conekin[0],conekin[1],alpha=0.05)
plt.title('proton phase space (kin. energy)')
plt.savefig('Images/proton-phasespace'+str(t)+'.png')
plt.show()

plt.rcParams['figure.figsize'] = 13, 10
reload(mpl_toolkits)
print mpl_toolkits.__path__
from mpl_toolkits.mplot3d import Axes3D


a=get_slice(1,proton,gdims_y,gdims_z,dx,up,low)[:,:1344]
b=get_slice(0,proton,gdims_x,gdims_z,dx,up,low)[:,:1344]
c=get_slice(0,carbon,gdims_x,gdims_z,dx,up,low)[:,:1344]
d=get_slice(1,carbon,gdims_x,gdims_z,dx,up,low)[:,:1344]

v=np.linspace(0,69,20)
v2=np.linspace(0,99,3)
x,y=np.mgrid[20:45,20:45]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.contour(x,y,np.transpose(c.reshape(64,24,64,21).sum(axis=1).sum(axis=2)[20:45,20:45]),v2, alpha=0.9,colors='k',zdir='z',offset=32.)
plt.contour(y,d.reshape(64,24,64,21).sum(axis=1).sum(axis=2)[20:45,20:45],x,v2, alpha=0.9,colors='k',zdir='y',offset=32.)
plt.contourf(y,a.reshape(64,24,64,21).sum(axis=1).sum(axis=2)[20:45,20:45],x,v, alpha=0.3,zdir='y',offset=32.)
plt.contourf(x,y,np.transpose(b.reshape(64,24,64,21).sum(axis=1).sum(axis=2))[20:45,20:45],v, alpha=0.3,zdir='z',offset=32.)

plt.contour(x,y,np.transpose(c.reshape(64,24,64,21).sum(axis=1).sum(axis=2)[20:45,20:45]),v2, alpha=0.9,colors='k',zdir='z',offset=32.)
plt.contour(y,d.reshape(64,24,64,21).sum(axis=1).sum(axis=2)[20:45,20:45],x,v2, alpha=0.9,colors='k',zdir='y',offset=32.)
plt.contourf(y,a.reshape(64,24,64,21).sum(axis=1).sum(axis=2)[20:45,20:45],x,v, alpha=0.3,zdir='y',offset=32.)
plt.contourf(x,y,np.transpose(b.reshape(64,24,64,21).sum(axis=1).sum(axis=2))[20:45,20:45],v, alpha=0.3,zdir='z',offset=32.)

ax.set_xlabel('Z')
ax.set_ylabel('Y')
ax.set_zlabel('X')
ax.set_xlim([20,45])
ax.set_ylim([20,45])
ax.set_zlim([20,45])
plt.colorbar()
plt.savefig(namestr+str(t)+'3dslices-new2.png')
plt.show()
