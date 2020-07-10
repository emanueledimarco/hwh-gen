#!/bin/env python

# usage: ./submitMG5.py -t 6 -r 48 --outdir pp-tjwpwm/ pp-tjwpwm/proc_card_mg5.dat

jobstring  = '''#!/bin/sh
ulimit -c 0 -S
ulimit -c 0 -H
set -e
cd CMSSWBASE
export SCRAM_ARCH=slc7_amd64_gcc820
eval `scramv1 runtime -sh`
cd OUTDIR
MG5STRING

'''

mgexec = '/afs/cern.ch/work/e/emanuele/hwh/mcprod/CMSSW_10_6_12/src/hwh-gen/mg5-config/MG5_aMC_v2_7_3/bin/mg5_aMC'

def makeCondorFile(jobdir, srcFiles, options, logdir, errdir, outdirCondor):
    dummy_exec = open(jobdir+'/dummy_exec.sh','w')
    dummy_exec.write('#!/bin/bash\n')
    dummy_exec.write('bash $*\n')
    dummy_exec.close()
     
    condor_file_name = jobdir+'/condor_submit.condor'
    condor_file = open(condor_file_name,'w')
    condor_file.write('''Universe = vanilla
Executable = {de}
use_x509userproxy = False
Log        = {ld}/$(ProcId).log
Output     = {od}/$(ProcId).out
Error      = {ed}/$(ProcId).error
getenv      = True
next_job_start_delay = 1
environment = "LS_SUBCWD={here}"
+MaxRuntime = {rt}\n
'''.format(de=os.path.abspath(dummy_exec.name), ld=os.path.abspath(logdir), od=os.path.abspath(outdirCondor),ed=os.path.abspath(errdir),
           rt=int(options.runtime*3600), here=os.environ['PWD'] ) )
    if hasattr(options,'nThreads'):
        condor_file.write('request_cpus = {nt} \n\n'.format(nt=options.nThreads))
    for sf in srcFiles:
        condor_file.write('arguments = {sf} \nqueue 1 \n\n'.format(sf=os.path.abspath(sf)))
    condor_file.close()
    return condor_file_name


import ROOT, random, array, os, sys

if __name__ == "__main__":
    
    from optparse import OptionParser
    parser = OptionParser(usage='%prog file.hdf5 ntoys [prefix] [options] ')
    parser.add_option('-t'  , '--threads'       , dest='nThreads'      , type=int           , default=4    , help='use nThreads in the fit (suggested 2 for single charge, 1 for combination)')
    parser.add_option(        '--dry-run'       , dest='dryRun'        , action='store_true', default=False, help='Do not run the job, only print the command');
    parser.add_option('-r'  , '--runtime'       , default=24            , type=int                          , help='New runtime for condor resubmission in hours. default None: will take the original one.');
    parser.add_option('--outdir', dest='outdir', type="string", default=None, help='outdirectory');
    (options, args) = parser.parse_args()

    ## for tensorflow the ws has to be the .hdf5 file made from the datacard with text2hdf5.py!
    
    proccard = os.path.abspath(args[0]);
    print "Submitting MG5 with PROC_CARD {pc}...".format(pc=proccard)

    absopath  = os.path.abspath(options.outdir)
    if not options.outdir:
        raise RuntimeError, 'ERROR: give at least an output directory. there will be a HUGE number of jobs!'
    else:
        if not os.path.isdir(absopath):
            print 'making a directory and running in it'
            os.system('mkdir -p {od}'.format(od=absopath))


    jobdir = absopath+'/jobs/'
    if not os.path.isdir(jobdir):
        os.system('mkdir {od}'.format(od=jobdir))
    logdir = absopath+'/logs/'
    if not os.path.isdir(logdir):
        os.system('mkdir {od}'.format(od=logdir))
    errdir = absopath+'/errs/'
    if not os.path.isdir(errdir):
        os.system('mkdir {od}'.format(od=errdir))
    outdirCondor = absopath+'/outs/'
    if not os.path.isdir(outdirCondor):
        os.system('mkdir {od}'.format(od=outdirCondor))
        
    random.seed()

    srcfiles = []
    job_file_name = jobdir+'/job.sh'
    log_file_name = logdir+'/job.log'
    tmp_file = open(job_file_name, 'w')

    tmp_filecont = jobstring
    cmd = mgexec + ' ' + proccard

    tmp_filecont = tmp_filecont.replace('MG5STRING', cmd)
    tmp_filecont = tmp_filecont.replace('CMSSWBASE', os.environ['CMSSW_BASE']+'/src/')
    tmp_filecont = tmp_filecont.replace('OUTDIR', absopath+'/')
    tmp_file.write(tmp_filecont)
    tmp_file.close()
    srcfiles.append(job_file_name)
    cf = makeCondorFile(jobdir,srcfiles,options, logdir, errdir, outdirCondor)
    subcmd = 'condor_submit {rf} '.format(rf = cf)

    print subcmd

    sys.exit()

