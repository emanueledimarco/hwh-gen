#!/bin/env python
import os,sys,commands
import string, random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if len(sys.argv) < 3 :
    print "Syntax: splitlhe.py input.lhe neventschunk [outputdir]"
inname=sys.argv[1]
nevents_chunk=int(sys.argv[2])

outdir = None
if len(sys.argv) > 3:
    outdir = sys.argv[3]
    print "The output chunks will be put into ",outdir

print "Splitting file ",inname," into chunks with ",nevents_chunk," events each."

basename=os.path.basename(inname).split('.')[0]
ext='.'+'.'.join(os.path.basename(inname).split('.')[1:])
residualfile = id_generator(6)+ext
while os.path.isfile(residualfile):
    residualfile = id_generator(6)+ext
residual_basename = os.path.basename(residualfile).split('.')[0]

os.system('cp {inf} {res}'.format(inf=inname,res=residualfile))

if residualfile.endswith('.gz'):
    print "Unzipping ",residualfile,"..."
    os.system("gunzip {inf}".format(inf=residualfile))
    residualfile = residualfile.replace('.gz','')
tmpfile='tmp_'+residualfile

output = commands.getstatusoutput("grep nevents %s | awk '{print $1}'" % residualfile)
nevents = int(output[1])

nfiles = int(nevents/nevents_chunk)
print "The sample contains ",nevents," and it will split in ",nfiles,"  files of ",nevents_chunk," events each."

for step in range(nfiles-1):
    chunkname = residual_basename+'_chunk'+str(step)+'.lhe'
    if os.path.isfile(chunkname):
        print "ERROR! The chunk ",chunkname," exists. Probably splitting in the wrong outut directory! Stop."
        os.exit(1)
    print "making chunk ",chunkname
    cmd1 = "./split.pl {nevents} {ifile} {tmpfile} {infile}".format(nevents=nevents_chunk,ifile=chunkname,tmpfile=tmpfile,infile=residualfile)
    cmd2 = "mv {tmpfile} {infile}".format(tmpfile=tmpfile,infile=residualfile)
    os.system(cmd1)
    os.system(cmd2)
    if outdir:
        os.system("mv {chunk} {od}/{chunk2}".format(chunk=chunkname,od=outdir,chunk2=chunkname.replace(residual_basename,basename)))
os.system("mv {residual} {lastchunk}".format(residual=residualfile,lastchunk=basename+'_chunk'+str(step+1)+'.lhe'))
print "DONE."

