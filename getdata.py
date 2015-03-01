import os
import numpy as np
import h5py

def load_params(par):
    "load simulation parameters from file 'params.txt' or 'Params.txt'"
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
        return [radius,dt,dx,gdims_x,gdims_z]
    except:
        print "parameter file invalid"


def get_arr(t,n,typ,pfad):
        "loads array from particles-h5 file"
        try:
            print pfad
            name = 'particles.t' + str(t).zfill(6) + '_n00' + str(n).zfill(4) + '.h5'
            print 'loading '+pfad+'/'+name

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
                        return arr
        except: print "failed loading particle data t= "+str(t)


def get_ex(t,n,p):
    "extracts e-field x-component at time t from node n, patch p from pfd-h5 file"
    name = 'pfd.t0' + str(t).zfill(5) + '_n00' + str(n).zfill(4) + '.h5'
    #print name
    f = h5py.File(name)
    # f = h5py.File('Field-Data/' + name)
    for key in f:
        g = f[key]
        #   print g.keys()
        if 'ex' in g:
            mat = np.array(g['ex/p'+str(p)+'/3d'])
    return mat.reshape(mat.shape[0],mat.shape[2])

def get_ez(t,n,p):
    "extracts e-field z-component at time t from node n, patch p from pfd-h5 file"
    name = 'pfd.t0' + str(t).zfill(5) + '_n00' + str(n).zfill(4) + '.h5'
    #print name
    f = h5py.File(name)
    # f = h5py.File('Field-Data/' + name)
    for key in f:
        g = f[key]
        #   print g.keys()
        if 'ez' in g:
            mat = np.array(g['ez/p'+str(p)+'/3d'])
    return mat.reshape(mat.shape[0],mat.shape[2])

get_en = lambda px,py,pz: (np.sqrt(px*px + py*py + pz*pz +1) - 1)*mp*c*c/e
"computes kin. energy from momenta"

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
    for i in range (0,np_x):
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

if __name__ == "__main__":
        print "testing:\n"
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
            print get_arr(1000,0,'px',pfad)
        except:
            print "could not load particles.t001000"