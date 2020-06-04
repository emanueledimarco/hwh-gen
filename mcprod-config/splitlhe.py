#!/bin/env python
import os,sys,commands

if len(sys.argv) < 3 :
    print("Syntax: splitlhe.py input.lhe neventschunk")
inname=sys.argv[1]
nevents_chunk=int(sys.argv[2])

basename=os.path.basename(inname).split('.')[0]
residualfile=inname
tmpfile='tmp.lhe'
residualfile = 'residual.lhe'
os.system('cp {inf} {res}'.format(inf=inname,res=residualfile))

output = commands.getstatusoutput("grep nevents %s | awk '{print $1}'" % residualfile)
nevents = int(output[1])

nfiles = int(nevents/nevents_chunk)
print "The sample contains ",nevents," and it will split in ",nfiles,"  files of ",nevents_chunk," events each."

for step in range(nfiles-1):
    chunkname = basename+'_chunk'+str(step)+'.lhe'
    print "making chunk ",chunkname
    cmd1 = "./split.pl {nevents} {ifile} {tmpfile} {infile}".format(nevents=nevents_chunk,ifile=chunkname,tmpfile=tmpfile,infile=residualfile)
    cmd2 = "mv {tmpfile} {infile}".format(tmpfile=tmpfile,infile=residualfile)
    os.system(cmd1)
    os.system(cmd2)
os.system("mv {tmpfile} {lastchunk}".format(tmpfile=tmpfile,lastchunk=basename+'_chunk'+str(step+1)+'.lhe'))
print "DONE."

