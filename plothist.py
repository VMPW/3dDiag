import conv
from getdata import *
import matplotlib.pyplot as plt
import sys
import os
import numpy as np

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

n=0
electrons = get_hist(t,n,0,pfad)
protons = get_hist(t,n,1,pfad)
carbons = get_hist(t,n,2,pfad)
print electrons.shape
ne=electrons.sum(axis=0)
ni=protons.sum(axis=0)
nc=carbons.sum(axis=0)
print ne.shape
ee=electrons.sum(axis=1).sum(axis=1)
print ee.shape
plt.rcParams['figure.figsize'] = 15, 10

#plt.suptitle('electrons \n   Qges= '+str(np.around(Qtot,3))+'e \n pulse maximum hits target in ' + str(52-(t*dt*1e15)) +'fs')
plt.subplot(2,2,1)
plt.imshow(ne)
plt.xlabel('z')
plt.ylabel('y')
plt.title('density distribution electrons')

#plt.savefig('Images/'+namestr+'charge'+str(t)+'.png')


plt.subplot(2,2,2)
plt.imshow(ni)
plt.xlabel('x')
plt.ylabel('y')
plt.title('density distribution protons')
#plt.savefig(namestr+'detec'+str(t)+'.png')

#plt.suptitle('electrons \n   Qges= '+str(np.around(Qtot,3))+'e \n pulse maximum hits target in ' + str(52-(t*dt*1e15)) +'fs')
plt.subplot(2,2,3)
plt.plot(np.array(electrons.sum(axis=1).sum(axis=1)))
plt.ylabel('n')
plt.xlabel('e')
plt.title('energy distribution electrons')
#plt.savefig('Images/'+'charge'+str(t)+'.png')


plt.subplot(2,2,4)
plt.plot(np.array(protons.sum(axis=1).sum(axis=1)))
plt.ylabel('n')
plt.xlabel('e')
plt.title('energy distribution protons')
plt.savefig('Images/Histsliceplot'+str(t)+'.png')

plt.show()
