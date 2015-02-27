
class Data():
    
    def __init__(self,name,kind,size):
        self.name = name
        self.kind = kind
        self.E = np.zeros(size)
        self.N = np.zeros(size)
        self.Px = np.zeros(size)
        self.Py = np.zeros(size)
        self.Pz = np.zeros(size)
        self.pz = []
        self.angle= []
        self.ekin = []
        self.econe =[]
        self.sorted = False
        
    def full_process(self, p, slice): # p = posx,posz,px,py,pz
        self.N[p[0],p[1]]+=1
        self.Px[p[0],p[1]] +=p[2]
        self.Pz[p[0],p[1]] +=p[4]
        Ekin = (np.sqrt(p[2]*p[2] + p[3]*p[3] + p[4]*p[4] +1) - 1)*mp*c*c/e
        self.E[p[0],p[1]] +=Ekin
    
    def hist_process(self, p): # p = posx,posz,px,py,pz
        Ekin = (np.sqrt(p[2]*p[2] + p[3]*p[3] + p[4]*p[4] +1) - 1)*mp*c*c/e
        self.ekin+=[Ekin]
        self.angle +=[math.atan(p[2]/p[4])*180/math.pi]
        if (proton.angle[i]<10.) and (proton.angle[i]>-10.): self.econe+=[Ekin]
        
        self.Px[p[0],p[1]] +=p[2]
        self.pz+=[p[4]]
