import numpy as np
import sys
import matplotlib.pyplot as plt

pfad = sys.argv[1]
radius = sys.argv[2]

file1=pfad+'/ChargeMonitor'+radius+'.txt'
file2=pfad+'/AvTempMonitor'+radius+'.txt'
file3=pfad+'/FastPartMonitor'+radius+'.txt'
file4=pfad+'/UltraFastMonitor'+radius+'.txt'

data=np.genfromtxt(file1,delimiter=' ',skip_header=1)
sorted = data[data[:,0].argsort(0)]
print sorted

#field=np.genfromtxt(sys.argv[2],delimiter=' ')
plt.plot(sorted[:,:1],sorted[:,1:2],color='blue')
plt.plot(sorted[:,:1],sorted[:,2:3],color='red')
#plt.plot(sorted[:,:1],sorted[:,3:4]/12.,color='black')
#plt.plot(field[:,0],field[:,1],color='green')
plt.xlabel('time/fs')
plt.ylabel('q/eV')
name = file1[:-4]
plt.savefig(name+'.png')
plt.show()

data=np.genfromtxt(file2,delimiter=' ',skip_header=1)
sorted = data[data[:,0].argsort(0)]
print sorted

#field=np.genfromtxt(sys.argv[2],delimiter=' ')
plt.plot(sorted[:,:1],sorted[:,1:2],color='blue')
plt.plot(sorted[:,:1],sorted[:,2:3],color='red')
#plt.plot(sorted[:,:1],sorted[:,3:4]/12.,color='black')
#plt.plot(field[:,0],field[:,1],color='green')
plt.xlabel('time/fs')
plt.ylabel('energy/eV')
name = file2[:-4]
plt.savefig(name+'.png')
plt.show()

data=np.genfromtxt(file3,delimiter=' ',skip_header=1)
sorted = data[data[:,0].argsort(0)]
print sorted

#field=np.genfromtxt(sys.argv[2],delimiter=' ')
plt.plot(sorted[:,:1],sorted[:,1:2],color='blue')
plt.plot(sorted[:,:1],sorted[:,2:3],color='red')
#plt.plot(sorted[:,:1],sorted[:,3:4]/12.,color='black')
#plt.plot(field[:,0],field[:,1],color='green')
plt.xlabel('time/fs')
plt.ylabel('energy/eV')
name = file3[:-4]
plt.savefig(name+'.png')
plt.show()

data=np.genfromtxt(file4,delimiter=' ',skip_header=1)
sorted = data[data[:,0].argsort(0)]
print sorted

#field=np.genfromtxt(sys.argv[2],delimiter=' ')
plt.plot(sorted[:,:1],sorted[:,1:2],color='blue')
plt.plot(sorted[:,:1],sorted[:,2:3],color='red')
plt.plot(sorted[:,:1],sorted[:,3:4]/12.,color='black')
#plt.plot(field[:,0],field[:,1],color='green')
plt.xlabel('time/fs')
plt.ylabel('energy/eV')
name = file4[:-4]
plt.savefig(name+'.png')
plt.show()
