#!/ProgramData\Anaconda3\python 
import request
global senda
import time
import datetime
import os
Nodata = "aaaa"
def sending(data1):
    print("Content-Type: text/html\n")
    print(str(data1)) 
aaaa= request.POST.get('statement')
ab1,ab2,ab3,ab4,dataa=aaaa.split(".")
ipp = ab1 +'.' + ab2+"."+ab3+"."+ab4
senda=dataa
readfile = ab4 + "_read"
writefile = ab4 + "_write"
if(os.path.exists(writefile+'.txt') == False):
    f = open("Iplist.txt",'w')
    f.write(ipp)
    f.close()
    f = open(writefile+'.txt','w')
    f.close()
    
f = open(readfile+'.txt','w')
f.write(senda)
f.close()
tic = datetime.datetime.now()
while True:
    toc = datetime.datetime.now() - tic
    if(os.stat(writefile+'.txt').st_size != 0):
        f = open(writefile+'.txt','r+')
        alpha=f.read()
        f.truncate(0)
        f.close()
        sending(alpha)
        break
    if toc.seconds > 8:
        sending("AAAA")
        break

    
    
