import numpy as np
import matplotlib.pyplot as plt
import sys
import timeit
import math
import conv
from getdata import *
import part

plt.rcParams['figure.figsize'] = 15, 10
res = 1
cutoffx = 0.2
cutoffz = 0.2

dxphys=1.5625e-08
ppqp=9155. #1144.
nc=4096*[28.75*ppqp]

"""
p = open('params.txt', 'r')
params = p.read()
params = params.split()

t = int(sys.argv[1])
radius = float(params[0])
gdims_x = int(params[1])
gdims_z = int(params[2])
dt = float(params[3])
dx = float(params[4])
dxphys = float(params[5])*1e6
"""
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

zline=np.linspace(0,gdims_z,gdims_z+1)*dxphys*1e6
#print size,zline,len(zline)

get_en = lambda px,py,pz: (np.sqrt(px*px + py*py + pz*pz +1) - 1)*mp*c*c/e
"computes kin. energy from momenta"

def get_phi_p(px,pz):
    if (pz>0.): phi = np.arctan(px/pz)*180/math.pi
    elif (px<0.) : phi = (-180.)+np.arctan(px/pz)*180/math.pi
    elif (px>0.) : phi = 180.+np.arctan(px/pz)*180/math.pi
    return (phi,np.sqrt(pz*pz+px*px)*mp*c/e)
"returns (angle,momentum in x,z-plane)"

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
#print xarr.size
#print pyarr.size


#allocating output-data
electron = part.Data("electron",0,conv.me,-1.,size)
proton = part.Data("proton",1,conv.mp,1.,size)
carbon = part.Data("carbon",2,conv.mc,6.,size)

Qin=0.
Qout=0.
phase=[(0,0)]

#sorting
for i in range(0,kindarr.size):
    """posx = int(xarr[i]*(1/dx))
    posz = int(zarr[i]*(1/dx))
    parttyp = kindarr[i]
    z=posz-8*128
    x=posx-512"""
    parttyp = kindarr[i]
    p = [int(xarr[i]*(1/dx)),int(zarr[i]*(1/dx)),pxarr[i],pyarr[i],pzarr[i]]
    if (parttyp == 0):
        electron.sort(p,radius,center)
            #if (np.sqrt(z*z+x*x)<radius*1.1/dxphys):
            #Qin+=-1.
            #else: Qout+=-1.
    elif (parttyp == 1):
        Ek=proton.sort(p,radius,center)
        phase+=[proton.ang_sort(p,Ek)]
    else:
        carbon.sort(p,radius,center)
    """        if (np.sqrt(z*z+x*x)<radius*1.1/dxphys):
            Qin+=6.
        else: Qout+=6.
        E = 12*get_en(pxarr[i],pyarr[i],pzarr[i])
        Ekinc[posx,posz] +=E
        specEc[posz]+=E"""
#sEx = cut(Ex,cutoffx,cutoffz)
#sEz = cut(Ez,cutoffx,cutoffz)
#cone = np.zeros_like(Ni)

#Rho = Ni + 6*Nc - Ne
#mass = Ni + 12*Nc
#Etot=np.sum(histp)
#phase = np.transpose(phas)
#phasein = np.transpose(phas1)
stop = timeit.default_timer()
#print histp
phase=zip(*phase)

#print phase
print 'processing time:',stop - start

plt.suptitle('pulse maximum hits target in ' + str(220-(t*dt*1e15)) +'fs')
#****************************************************
plt.subplot(3,2,1)
plt.imshow(proton.Emax,extent=[0,size[1]*dxphys*1e6,0,size[0]*dxphys*1e6],interpolation='bicubic')
plt.title("proton energy")
plt.ylabel("x")
plt.xlabel("z")
plt.xlim([5,40])
#plt.ylim([2,14])
plt.colorbar(orientation=u'vertical')
#****************************************************
plt.subplot(3,2,3)
plt.title("particle distribution")
plt.imshow(electron.N*(-1.)+carbon.N*(6.)+proton.N,cmap=plt.get_cmap('bwr'),extent=[0,size[1]*dxphys*1e6,0,size[0]*dxphys*1e6],vmin=-2., vmax=2.,interpolation='bicubic')
plt.ylabel("x")
plt.xlabel("z")
plt.xlim([5,40])
#plt.ylim([2,14])
plt.colorbar(orientation=u'vertical')
#****************************************************
plt.subplot(3,2,5)
#plt.imshow(np.log10(Ekinpp+Ekincp))
plt.scatter(phase[0],phase[1],alpha=0.1,color='red')
#plt.scatter(phasein[0],phasein[1],color='blue',alpha=0.01)
#plt.imshow(scat,origin='lower',interpolation='none',aspect='auto')
#plt.colorbar(orientation=u'horizontal')
plt.title("p/angle")
plt.xlabel("phi/degree")
plt.ylabel("E")
#plt.savefig('angles-'+str(t)+'r='+str(radius)+'.png')
#plt.show()
#plt.ylim([0,1.5])
#plt.colorbar(orientation=u'horizontal')
#****************************************************
plt.subplot(3,2,2)
plt.plot(zline,ppqp*proton.lineout,color ="red")
plt.plot(zline,ppqp*carbon.lineout,color="black")
plt.plot(zline,ppqp*electron.lineout,color="blue", linewidth=0.2)
plt.plot(nc,color='green')
#plt.ylim([0,4.5])
#plt.text(500,4, 'total charge in/outside sphere: '+str(np.around(Qin*9155,5))+'/'+str(np.around(Qout*9155,5)))
plt.title("density line out")
plt.xlabel("z")
plt.ylabel("n")
plt.xlim([0,64])

#****************************************************
plt.subplot(3,2,4)
plt.plot(zline,electron.lineE/200.,color='blue',linewidth=0.1)
plt.plot(zline,proton.lineE,color='red')
plt.plot(zline,carbon.lineE,color='black')
plt.title("maximum energy")
plt.xlabel("z")
plt.ylabel("E")
plt.xlim([0,64])
plt.ylim([0,1e8])
#****************************************************
plt.subplot(3,2,6)
#plt.hist(histp,bins=100,log=True,normed=False)
plt.hist(proton.ekin,bins= 50,log=True,normed=False,alpha=0.4,color='red',facecolor='red')
plt.hist(proton.econe,bins= 50,log=True,normed=False,alpha=0.1,color='blue',facecolor='blue')
#plt.text(6e7,0.5e4, 'total ion energy in cone: '+str(np.around(Etot/1e9,4))+'GeV\ntotal ion energy in box: '+str(np.around(sum(np.ravel(Ekinp)/1e9,4)))+'GeV\nelectron temperature:'+str(np.mean(Ekine))+'\nproton temperature:'+str(np.mean(Ekinp))+'\ncarbon temperature:'+str(np.mean(Ekinc)))
plt.xlim([0,1e8])
plt.ylim([0,1.5e4])
plt.xlabel("E")
plt.title("Energiespektrum (blue: in Cone)")
plt.ylabel("n")


plt.savefig('Images/CD2D/CD2D-'+str(t)+'r='+str(radius)+'.png')
#plt.show()

C=carbon.process(1e6,(radius+3.)*1e-6/dxphys,center,size)
E=electron.process(1e6,(radius+3.)*1e-6/dxphys,center,size)
P=proton.process(1e6,(radius+3.)*1e-6/dxphys,center,size)

print C,E,P

Q=ppqp*(C[0]+P[0]-E[0])
Qin=ppqp*(C[1]+P[1]-E[1])

tempc=C[2]
tempp=P[2]
tempe=E[2]
hotc=C[3]
hotp=P[3]
hote=E[3]
uhotc=C[4]
uhotp=P[4]
uhote=E[4]

Qstring = str(t*dt*1e15)+' '+str(Q)+' '+str(Qin)+'\n'

Estring = str(t*dt*1e15)+' '+str(tempe)+' '+str(tempp)+' '+str(tempc)+' \n'

Hotstring =str(t*dt*1e15)+' '+str(hote)+' '+str(hotp)+' '+str(hotc)+' \n'

UltHotstring =str(t*dt*1e15)+' '+str(uhote)+' '+str(uhotp)+' '+str(uhotc)+' \n'

file = open(pfad+'/AvTempMonitor'+str(radius)+'.txt','a')
file.write( Estring)
file.close()
file2 = open(pfad+'/ChargeMonitor'+str(radius)+'.txt','a')
file2.write(Qstring)
file2.close()
file3 = open(pfad+'/FastPartMonitor'+str(radius)+'.txt','a')
file3.write(Hotstring)
file3.close()
file4 = open(pfad+'/UltraFastMonitor'+str(radius)+'.txt','a')
file4.write(UltHotstring)
file4.close()

print 'timestep',t,'successful'