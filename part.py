import numpy as np
from conv import *

class Data():
    
    def __init__(self,name,kind,mass,charge,size):
        self.name = name
        self.kind = kind
        self.m=mass
        self.q=charge
        self.E = np.zeros(size)
        self.Emax = np.zeros(size)
        self.N = np.zeros(size)
        self.Px = np.zeros(size)
        self.Py = np.zeros(size)
        self.Pz = np.zeros(size)
        self.pz = []
        self.angle= []
        self.ekin = []
        self.econe =[]
        self.lineout=np.zeros(size[1])
        self.lineE=np.zeros(size[1])
        self.sorted = False
        
    def sort(self,p,R,center): # p = posx,posz,px,py,pz
        self.N[p[0],p[1]]+=1
        self.Px[p[0],p[1]] +=p[2]
        self.Pz[p[0],p[1]] +=p[4]
        Ekin = (np.sqrt(p[2]*p[2] + p[3]*p[3] + p[4]*p[4] +1) - 1)*mp*c*c/e
        self.E[p[0],p[1]] +=Ekin
        if self.Emax[p[0],p[1]]<Ekin: self.Emax[p[0],p[1]]=Ekin
        if (p[0]<center[0]+30) and (p[0]>center[0]-30):
            self.lineout[p[1]]+= 1
            if self.lineE[p[1]]<Ekin: self.lineE[p[1]]=Ekin
        return Ekin
    
    def ang_sort(self,p,Ekin): # p = posx,posz,px,py,pz
        #Ekin = (np.sqrt(p[2]*p[2] + p[3]*p[3] + p[4]*p[4] +1) - 1)*mp*c*c/e
        self.ekin+=[Ekin]
        self.pz+=[p[4]]
        ang=math.atan(p[2]/p[4])*180/math.pi
        self.angle +=[ang]
        if (ang<10.) and (ang>-10.): self.econe+=[Ekin]
        return (ang,Ekin)

    def process(self,hot,R,center,size):
        Qin=[]
        print R,R/2.,center
        lx=center[0]-R/2.
        ux=center[0]+R/2.
        lz=center[0]-R/2.
        uz=center[0]+R/2.
        temp = np.average(self.E)
        hottemp = np.nan_to_num(np.average(self.E[self.E>hot]))
        Q = np.sum(self.N)*self.q
        print Q
        Qin=np.sum(self.N[lx:ux,lz:uz])*self.q
        return [Q,Qin,temp,hottemp]

