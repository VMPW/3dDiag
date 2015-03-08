from getdata import *
from process import *
import matplotlib.pyplot as plt
import sys
import os
import numpy as np


plt.rcParams['figure.figsize'] = 15, 10
cx = [0.,0.]
cz = [0.1,0.3]

global dx

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
mp = 1.67262177e-27
c = 299792458
e = 1.602176565e-19
me = 9.10939e-31
    
proton = [[],[],[],[],[],[],[]]
#carbon = np.zeros(shape=(7,N))
electron = [[],[],[],[],[],[],[]]
print proton
print electron

namestr = raw_input('Unter welchem Namen Speichern? ')
format = '0'
while (format!='a' and format!='h'):
    format = raw_input('Output format? (h for h5, a for asc) ')
if(format == 'h'):

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

    N = kindarr.size
    print N


    for i in range(0,N):
        if kindarr[i]==1:
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
            proton[6]+=[get_en(pxarr[i],pyarr[i],pzarr[i],mp,c,e)]
        #print proton
        elif kindarr[i]==0:
            electron[0]+=[xarr[i]]
            electron[1]+=[yarr[i]]
            electron[2]+=[zarr[i]]
            electron[3]+=[pxarr[i]]
            electron[4]+=[pyarr[i]]
            electron[5]+=[pzarr[i]]
            electron[6]+=[get_en(pxarr[i],pyarr[i],pzarr[i],mp,c,e)]
    #print electron

elif(format == 'a'):
    arr =np.zeros((7,1))
    for i in range(0,npatch):
        print 'arr', arr.shape
        arr=np.hstack((arr,np.transpose(get_asc(t,i,pfad))))
    Qtot = sum(arr[6,:])
    print Qtot
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
            proton[6]+=[get_en(arr[3,i],arr[4,i],arr[5,i],mp,c,e)]
        #print proton
        elif arr[6,i]==-1:
            electron[0]+=[arr[0,i]]
            electron[1]+=[arr[1,i]]
            electron[2]+=[arr[2,i]]
            electron[3]+=[arr[3,i]]
            electron[4]+=[arr[4,i]]
            electron[5]+=[arr[5,i]]
            electron[6]+=[get_en(arr[3,i],arr[4,i],arr[5,i],mp,c,e)]

proton = np.array(proton)
print proton.shape
electron = np.array(electron)
print electron.shape
print proton
print electron


up=(dx*gdims_x/2.)+1.
low=(dx*gdims_x/2.)-1.
print up
print low

plt.subplot(2,2,1)
plt.hist(proton[6,:],bins=50,log=True,normed=False)
#plt.xlim([0,8e7])
plt.savefig(namestr+'hist'+str(t)+'.png')

plt.subplot(2,2,2)
plt.imshow(np.transpose(get_detec(proton)),extent=[-20,20,-20,20])
plt.xlabel('x')
plt.ylabel('y')
#plt.savefig(namestr+'detec'+str(t)+'.png')

plt.subplot(2,2,3)
plt.imshow(np.log10(get_slice(0,proton,gdims_x,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('x')
plt.title('p-polarisation')
#plt.savefig(namestr+'xslice'+str(t)+'.png')

plt.subplot(2,2,4)
plt.imshow(np.log10(get_slice(1,proton,gdims_y,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('y')
plt.title('s-polarisation')
plt.savefig(namestr+'-Vierer-prot-'+str(t)+'.png')
plt.show()

plt.subplot(2,2,1)
plt.hist(electron[6,:],bins=50,log=True,normed=False)
#plt.xlim([0,8e7])
plt.savefig(namestr+'hist'+str(t)+'.png')

plt.subplot(2,2,2)
plt.imshow(np.transpose(get_detec(electron)),extent=[-20,20,-20,20])
plt.xlabel('x')
plt.ylabel('y')
#plt.savefig(namestr+'detec'+str(t)+'.png')

plt.subplot(2,2,3)
plt.imshow(np.log10(get_slice(0,electron,gdims_x,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('x')
plt.title('p-polarisation')
#plt.savefig(namestr+'xslice'+str(t)+'.png')

plt.subplot(2,2,4)
plt.imshow(np.log10(get_slice(1,electron,gdims_y,gdims_z,dx,up,low)))
plt.xlabel('z')
plt.ylabel('y')
plt.title('s-polarisation')
plt.savefig(namestr+'-Vierer-el-'+str(t)+'.png')