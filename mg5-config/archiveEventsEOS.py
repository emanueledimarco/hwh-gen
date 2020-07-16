#!/bin/env python
# usage: ./archiveEventsEOS.py yt_0_WW /eos/.../yt_0_WW

import os,sys
from os import path

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage='%prog mgdir eosdir [options] ')
    parser.add_option('-d',       '--dry-run'       , dest='dryRun'        , action='store_true', default=False, help='Do not run the job, only print the command');
    (options, args) = parser.parse_args()

    mgdir  = args[0].strip("/")
    eosdir = args[1].strip("/")

    if path.exists(eosdir):
        print "The target directory ",eosdir," exists: EXIT.\n"
        sys.exit(1)

    if not path.exists(mgdir+'/Events'):
        print "This directory does not contain Events dir. Something is fishy"
        sys.exit(1)
    
    tmp_filename = 'mgmover.txt'
    tmp_file = open(tmp_filename,'w')
    tmp_filecont = '''#!/bin/sh
mkdir {eosdir}
mv {mgdir}/Events {eosdir}
tar czvf {mgdir}.tgz {mgdir}
mv {mgdir}.tgz {eosdir}
'''.format(eosdir=eosdir,mgdir=mgdir)
    tmp_file.write(tmp_filecont)
    tmp_file.close()
    
    if options.dryRun:
        print 'I will execute ',tmp_filename
    else:
        os.system('bash '+tmp_filename)
        os.system('rm '+tmp_filename)
    print "DONE. Check the output in ",eosdir
