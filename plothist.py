import conv
from getdata import *
import matplotlib.pyplot as plt
import sys
import os
import numpy as np

size=96

t=int(sys.argv[1])
#pfad = raw_input('Pfad zum Output-Ordner?')
pfad = sys.argv[2 ]
name = sys.argv[3 ]
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
electrons_xh = get_hist(t,n,0,pfad,'hist_xze_high')
protons_xh = get_hist(t,n,1,pfad,'hist_xze_high')
#carbons_xh = get_hist(t,n,2,pfad,hist_xze_high)

electrons_yh = get_hist(t,n,0,pfad,'hist_yze_high')
protons_yh = get_hist(t,n,1,pfad,'hist_yze_high')
#carbons_yh = get_hist(t,n,2,pfad,hist_yze_high)

electrons_xl = get_hist(t,n,0,pfad,'hist_xze_low')
protons_xl = get_hist(t,n,1,pfad,'hist_xze_low')
carbons_xl = get_hist(t,n,2,pfad,'hist_xze_low')

electrons_yl = get_hist(t,n,0,pfad,'hist_yze_low')
protons_yl = get_hist(t,n,1,pfad,'hist_yze_low')
carbons_yl = get_hist(t,n,2,pfad,'hist_yze_low')

def energy_sum(x,start,end):
    en=np.zeros((size,size))
    for i in range(start,end):
        for j in range(0,size):
            for k in range(0,size):
                en[j][k]+=i*x[i][j][k]
    return en


#print electrons.shape
#ne=electrons_xh.sum(axis=0)
#ni=protons.sum(axis=0)
#nc=carbons.sum(axis=0)
#print ne.shape
ee=electrons_xh.sum(axis=1).sum(axis=1)
print ee.shape
plt.rcParams['figure.figsize'] = 15, 10

#plt.suptitle('electrons \n   Qges= '+str(np.around(Qtot,3))+'e \n pulse maximum hits target in ' + str(52-(t*dt*1e15)) +'fs')
plt.subplot(2,2,1)
plt.imshow(electrons_xh.sum(axis=0),interpolation='gaussian')
plt.xlabel('x')
plt.ylabel('z')
plt.title('density distribution electrons')

#plt.savefig('Images/'+namestr+'charge'+str(t)+'.png')


plt.subplot(2,2,2)
plt.imshow(protons_xh.sum(axis=0),interpolation='gaussian')
plt.xlabel('x')
plt.ylabel('z')
plt.title('density distribution protons')
#plt.savefig(namestr+'detec'+str(t)+'.png')

#plt.suptitle('electrons \n   Qges= '+str(np.around(Qtot,3))+'e \n pulse maximum hits target in ' + str(52-(t*dt*1e15)) +'fs')
plt.subplot(2,2,3)
plt.plot(np.array(electrons_xh.sum(axis=1).sum(axis=1)))
plt.ylabel('n')
plt.xlabel('e')
plt.title('energy spectrum electrons')
#plt.savefig('Images/'+'charge'+str(t)+'.png')


plt.subplot(2,2,4)
plt.imshow(energy_sum(electrons_xh,0,100))
plt.ylabel('n')
plt.xlabel('e')
plt.title('energy distribution electrons')
plt.savefig('Images/Histsliceplot'+name+'-'+str(t)+'.png')

plt.show()

#plt.subplot(2,3,0)
#plt.imshow(protons_xh.sum(axis=0),interpolation='gaussian')
#plt.xlabel('x')
#plt.ylabel('z')
#plt.title('density distribution protons')
#plt.savefig(namestr+'detec'+str(t)+'.png')
plt.subplot(2,3,1)
plt.imshow(protons_yl.sum(axis=0),interpolation='gaussian')
plt.xlabel('y')
plt.ylabel('z')
plt.title('protons y')
#plt.savefig(namestr+'detec'+str(t)+'.png')
plt.subplot(2,3,2)
plt.plot(0.938*protons_yl.sum(axis=1).sum(axis=1))
plt.xlabel('y')
plt.ylabel('z')
plt.title('y-slice energy protons (spol)')
#plt.savefig(namestr+'detec'+str(t)+'.png')
plt.subplot(2,3,3)
plt.imshow(carbons_yl.sum(axis=0),interpolation='gaussian')
plt.xlabel('y')
plt.ylabel('z')
plt.title('density distribution carbon (y)')
#plt.savefig(namestr+'detec'+str(t)+'.png')
plt.subplot(2,3,4)
plt.imshow(protons_xl.sum(axis=0),interpolation='gaussian')
plt.xlabel('x')
plt.ylabel('z')
plt.title('density distribution protons (x)')
#plt.savefig(namestr+'detec'+str(t)+'.png')
plt.subplot(2,3,5)
plt.plot(0.938protons_xl.sum(axis=1).sum(axis=1))
plt.xlabel('x')
plt.ylabel('z')
plt.title('x-slice energy protons (ppol)')
#plt.savefig(namestr+'detec'+str(t)+'.png')
plt.subplot(2,3,6)
plt.imshow(carbons_xl.sum(axis=0),interpolation='gaussian')
plt.xlabel('x')
plt.ylabel('z')
plt.title('density distribution carbon (x)')
plt.savefig(name+'histcomp'+str(t)+'.png')
plt.show()