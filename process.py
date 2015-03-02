import numpy as np
import math

def cut(arr,cutoffx,cutoffz):
    "extracts center portion by cutting off cutoff-sized rims of 2d-arr"
    start0 = arr.shape[0]*cutoffx[0]
    end0 = arr.shape[0] - arr.shape[0]*cutoffx[1]
    start1 = arr.shape[1]*cutoffz[0]
    end1 = arr.shape[1] - arr.shape[1]*cutoffz[1]
    return arr[start0:end0,start1:end1]

def get_angle(px,py,pz):
    return (math.atan(math.sqrt(px*px+py*py)/pz))*(180/math.pi)

def get_anglexy(pxy,pz):
    return math.atan(pxy/pz)*180/math.pi

def get_slice(typ,arr,gdims,gdimsz,dx,up,low):
    slice = np.zeros((gdims+10,gdimsz+10))
    for i in range(0,arr.shape[1]):
        if (arr[not typ,i]<up and arr[not typ,i]>low) :
            slice[arr[typ,i]/dx,arr[2,i]/dx]+=arr[6,i]
    print "slice "+str(typ)+','+str(not typ)
    return slice

def get_detec(arr):
    detec=np.zeros(shape=(40,40))
    for i in range(0,arr.shape[1]):
        #print arr[3,i],arr[4,i],arr[5,i]
        #print i
        ang = get_angle(arr[3,i],arr[4,i],arr[5,i])
        #print ang
        if (math.fabs(ang))<20.:
            detec[int(get_anglexy(arr[3,i],arr[5,i]))+20,int(get_anglexy(arr[4,i],arr[5,i]))+20]+=arr[6,i]
    print detec
    return detec