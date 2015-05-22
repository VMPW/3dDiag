import math

global e
global mp
global me
global c

mp = 1.67262177e-27
c = 299792458
e = 1.602176565e-19
me = 9.10939e-31
mc= 12.*mp
wL=1.883651567308853e15
nc=1.107562595e27

k = 1.3806488e-23
eps0 = 8.854187817e-12
n0 = 3.4e29

def eV_to_kelvin(E): return 11600*E
def kelvin_to_eV(K): return K/11600

def debye_length(T,n): return math.sqrt(k*eps0*T/(n*e*e))
def plasma_parameter(l,n): return 4/3.*math.pi*n*l*l*l
def plasma_frequency(n): return math.sqrt(e*e*n/(me*eps0))
def coll_freq(L,wp): return wp/(32.*math.pi)*(math.log(L)/L)

def closest_approach(T): return e**2/k/T
def thermal_vel(T,m): return math.sqrt(k*T/m)
def skin_depth(w): return c/w
def free_path(V,v): return V/v
def sound_vel(T) : return math.sqrt(5./3.*k*T/mp)

def give_params(t,n):
    T=eV_to_kelvin(t)
    l=debye_length(T,n)
    L=plasma_parameter(l,n)
    wp=plasma_frequency(n)
    v=coll_freq(L,wp)
    V=thermal_vel(T,me)
    Vi = thermal_vel(T,mp)
    print 'dens ',n,'temp ',T,'omega_p ',wp,'skin depth ', skin_depth(wp),'debye length ',l,'plasma par ',L,'coll_freq ',v,'thermal velocity el',V,'thermal velocity ions',Vi, 'free path el', free_path(V,v),'ion sound vel', sound_vel(T)
    return (n,T,wp,l,L,v)