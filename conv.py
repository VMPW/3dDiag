import math

global e
global mp
global me
global c

mp = 1.67262177e-27
c = 299792458
e = 1.602176565e-19
me = 9.10939e-31
mc= 6*mp

k = 1.3806488e-23
eps0 = 8.854187817e-12
n0 = 3.4e29

def debye_length(T,n): return math.sqrt(k*eps0*T/(n*e*e))
def plasma_parameter(l,n): return 4*math.pi*n*l*l*l
def plasma_frequency(n): return math.sqrt(e*e*n/(me*eps0))

def eV_to_kelvin(E): return 11600*E
def kelvin_to_eV(K): return K/11600
