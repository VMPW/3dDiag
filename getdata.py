import os
import numpy as np
import h5py
from conv import *

def load_params(par):
    "load simulation parameters from file 'params.txt' or 'Params.txt'"
    try:
        p = open(par, 'r')
        print 'opened '+par
        params = p.read()
        params = params.split()
        print params
        radius = int(params[0])
        gdims_x = int(params[1])
        gdims_y = int(params[2])
        gdims_z = int(params[3])
        dt = float(params[4])
        dx = float(params[5])
        npatch = int(params[6])
        try:
            dxphys = float(params[7])
        except:
            print 'no dxphys in parameter file'
            print radius,gdims_x,gdims_z,dt,dx,npatch
            p.close()
            return [radius,gdims_x,gdims_y,gdims_z,dt,dx,npatch]
        p.close()
        print[radius,gdims_x,gdims_y,gdims_z,dt,dx,npatch,dphys]
        return [radius,gdims_x,gdims_y,gdims_z,dt,dx,npatch,dphys]
    except:
        print "parameter file invalid"

def load_params2d(par):
    "load simulation parameters from file 'params.txt' or 'Params.txt'"
    try:
        p = open(par, 'r')
        print 'opened '+par
        params = p.read()
        params = params.split()
        print params
        radius = float(params[0])
        gdims_x = int(params[1])
        gdims_z = int(params[2])
        dt = float(params[3])
        dx = float(params[4])
        npatch = int(params[5])
            #try:
            #dxphys = float(params[6])
            #except:
            #print 'no dxphys in parameter file'
            #print radius,gdims_x,gdims_z,dt,dx,npatch
            #p.close()
            #return [radius,gdims_x,gdims_z,dt,dx,npatch]
        p.close()
        return [radius,gdims_x,gdims_z,dt,dx,npatch]
    except:
        print "parameter file invalid"


def get_arr(t,n,typ,pfad):
        "loads array from particles-h5 file"
        try:
            name = 'particles.t' + str(t).zfill(6) + '_n00' + str(n).zfill(4) + '.h5'
            #print 'loading '+typ+' from '+pfad+'/'+name

            f = h5py.File(pfad+'/'+name)
        
            arr = []
            for key in f:
                for i in range(0,len(typ)):
                    if (key[i]==typ[i]):
                        valid = True
                    else:
                        valid = False
                if valid:
                    arr = np.concatenate((arr,np.array(f[key])))
                    print arr
            return arr
        except: print "failed loading particle data t= "+str(t)

def get_hist(t,n,kind,pfad):
    try:
        print pfad, t, n , kind
        name = 'hist.t' + str(t).zfill(6) + '_n00' + str(n).zfill(4) + '.h5'
        print 'loading kind '+str(kind)+' from '+pfad+'/'+name
        f = h5py.File(pfad+'/'+name)
        arr = [0.]
        try:
		for key in f:
			if 'fld' in key: g = f[key][u'fld']
            	return g[:,:,:,kind]
        except: print name,' exists but could not be loaded (kind must be 0,1 or 2)'
    except: print "failed loading hist data t= "+str(t)

def get_ex(t,n,pfad):
    "extracts e-field x-component at time t from node n, from pfd-h5 file"
    name = 'pfd.t0' + str(t).zfill(5) + '_n00' + str(n).zfill(4) + '.h5'
    #print 'loading '+pfad+'/'+name
    f = h5py.File(pfad+'/'+name)
    # f = h5py.File('Field-Data/' + name)
    for key in f:
        g = f[key]
        #   print g.keys()
        if 'ex' in g:
            mat = np.array(g['ex/p'+str(n)+'/3d'])
    return mat.reshape(mat.shape[0],mat.shape[2])

def get_ez(t,n,p,pfad):
    "extracts e-field z-component at time t from node n, patch p from pfd-h5 file"
    name = 'pfd.t0' + str(t).zfill(5) + '_n00' + str(n).zfill(4) + '.h5'
    #print 'loading '+pfad+'/'+name
    f = h5py.File(pfad+'/'+name)
    # f = h5py.File('Field-Data/' + name)
    for key in f:
        g = f[key]
        #   print g.keys()
        if 'ez' in g:
            mat = np.array(g['ez/p'+str(n)+'/3d'])
    return mat.reshape(mat.shape[0],mat.shape[2])


def get_phi_pz(px,pz):
    phi = np.arctan(px/pz)
    if (phi<0.142) and (phi>-0.142) : 	return (phi,pz*mp*c/e)
    else : return (0,0)
"returns (angle,momentum pz) (for '16 degree detector')"


def cut(arr,cutoffx,cutoffz):
    "extracts center portion by cutting off cutoff-size rims of 2d-arr"
    start0 = arr.shape[0]*cutoffx
    end0 = arr.shape[0] - start0
    start1 = arr.shape[1]*cutoffz
    end1 = arr.shape[1] - start1
    return arr[start0:end0,start1:end1]

"""def node_concat(nn_x,nn_z):
    "stitch nodes back together"
    for i in range(0,n_x):"""

def patch_concat(get_x,n):
    "stitch patches back together"
    mat = np.zeros((1,gdims_z/2 + 1))
    # print mat.shape
    for i in range(0,np_x):
        arr = np.zeros((gdims_x/(np_x),1))
        #    print arr.shape
        for j in range(0,np_z):
            p=np_z*i+j
            new = np.array(get_x(t,n,p))
            #       print new.shape
            arr = np.hstack((arr,new))
        #      print arr.shape
        mat = np.vstack((mat,arr))
    return mat

def get_asc(t,n,pfad):
    "extracts particles at time t from node n from .asc file"
    "arr = x,y,z,px,py,pz,q (N,7)"
    name = 'prt.t' + str(t).zfill(6) + '_n00' + str(n).zfill(4) + '.asc'
    arr = []
    try:
        arr=np.genfromtxt(pfad+'/'+name)[:,1:8]
    except:
        print name, ' empty or none existent'
        arr = np.zeros((1,7))
    print name, 'loaded as',arr.shape
    return arr



if __name__ == "__main__":
        print "\n testing:"
        pfad = raw_input('Pfad zum Output-Ornder?')
        if  os.path.isfile(pfad+'/params.txt') :
            par = pfad+'/params.txt'
            print par
            load_params(par)
        elif os.path.isfile(pfad+'/Params.txt') :
            par = pfad+'/Params.txt'
            print par
            load_params(par)
        else: print "no parameter file found"
        try:
            print get_asc(50,0,pfad)
        except:
            print "could not load particles.t001000"
