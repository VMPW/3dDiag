from const import *
from getdata import *
from process import *
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

ne=electrons.sum(axis=0)
np=protons.sum(axis=0)
nc=carbons.sum(axis=0)



#plt.suptitle('electrons \n   Qges= '+str(np.around(Qtot,3))+'e \n pulse maximum hits target in ' + str(52-(t*dt*1e15)) +'fs')
plt.subplot(2,2,1)
plt.imshow(ne)
plt.xlabel('z')
plt.ylabel('y')
plt.colorbar(orientation=u'horizontal')
plt.title('charge distribution')
#plt.savefig('Images/'+namestr+'charge'+str(t)+'.png')


plt.subplot(2,2,2)
plt.imshow(np)
plt.xlabel('x')
plt.ylabel('y')
#plt.savefig(namestr+'detec'+str(t)+'.png')

plt.show()