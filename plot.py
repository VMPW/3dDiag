from getdata import *
from process import *
import matplotlib.pyplot as plt


plt.rcParams['figure.figsize'] = 15, 10
cx = [0.,0.]
cz = [0.1,0.3]


try:
    p = open(par, 'r')
    params = p.read()
    params = params.split()
    radius = int(params[0])
    gdims_x = int(params[1])
    gdims_z = int(params[2])
    dt = float(params[3])
    dx = float(params[4])
    print dt,dx,radius,gdims_x,gdims_z

except:
    print "parameter file invalid"

size = [gdims_x+1,gdims_z+1]
mp = 1.67262177e-27
c = 299792458
e = 1.602176565e-19
me = 9.10939e-31

namestr = raw_input('Unter welchem Namen Speichern?')
size = [gdims_x+1,gdims_z+1]
np = raw_input('largest patch number?')
t = int(raw_input('which timestep?'))

plt.imshow(cut(proton.Ehigh,cx,cz))
plt.savefig(namestr+'yslice'+str(t)+'.png')
plt.show()