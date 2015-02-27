import numpy as np

def cut(arr,cutoffx,cutoffz):
    "extracts center portion by cutting off cutoff-sized rims of 2d-arr"
    start0 = arr.shape[0]*cutoffx[0]
    end0 = arr.shape[0] - arr.shape[0]*cutoffx[1]
    start1 = arr.shape[1]*cutoffz[0]
    end1 = arr.shape[1] - arr.shape[1]*cutoffz[1]
    return arr[start0:end0,start1:end1]

def slice(arr,up,low):
    np.where(arr[]<up and arr>low)
    return arr