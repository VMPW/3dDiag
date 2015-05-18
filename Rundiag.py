import subprocess

start = int(raw_input('First timestep: '))
end = int(raw_input('Last timestep: '))
#nt=int(raw_input('Number of threads: '))
step=int(raw_input('stepsize: '))
pfad = raw_input('Pfad zum Output-Ordner?')

for t in range (start,end,2*step):
    print t
    c1 = "python CD2D.py "+str(t)+' '+ pfad
    p1 = subprocess.Popen(c1,shell=True)
    c2 = "python CD2D.py "+str(t+step)+' '+ pfad
    p2 = subprocess.Popen(c2,shell=True)
    p1.wait()
    print "p1 done"
    p2.wait()
    print "p2 done"

"""	p3.wait()
	print "p3 done"				
	p4.wait()
	print "p4 done" """
	

print "done"


"""	c3 = "python CD2D.py "+str(t+200)+' '+ pfad
    p3 = subprocess.Popen(c3,shell=True)
    c4 = "python CD2D.py "+str(t+300)+' '+ pfad
    p4 = subprocess.Popen(c4,shell=True)"""