import os
from Mi_Functions import *
data=open('JPGs.txt','r').readlines()

#For JPG
original_size=0
optimized_size=0
#print 'No\tURL\tSize'
for l in data:
    try:
        if '.jpg' in l:
            #print str(data.index(l))+'\t'+l.strip()+'\t'+str(float(l.split('(')[1].split('K')[0].strip()))
            original_size+=float(l.split('(')[1].split('K')[0].strip())
            optimized_size+=float(l.split(' size')[1].split('K')[0].strip())
            #print l.split('%')[0].split(' ')[-1].strip()
    except Exception,e:
        print 'PIZDEC --> '+str(e)+' '+l.strip()+" Won't be calculated! :( "
print '-'*100
print 'Total original in MB:',original_size/1024
print 'Total optimized in MB:',optimized_size/1024
print 'Reduce percentage:',100-optimized_size*100/original_size,'%'

