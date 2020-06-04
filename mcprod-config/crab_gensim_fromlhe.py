from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'step_0_fromLHE_TJWW_1l_2018'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'hwh_0_cfg.py'
config.JobType.allowUndistributedCMSSW = True # this is to run the GEN-SIM for 2018 in CMSSW_10_6_12

config.Data.userInputFiles = open('/afs/cern.ch/work/e/emanuele/hwh/mcprod/CMSSW_10_6_12/src/crab/step0/pp-tjww-1l.list').readlines()
config.Data.outputPrimaryDataset = 'TJWW_1l_2018_GENSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = len(config.Data.userInputFiles)
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'step_0_fromLHE_TJWW_1l_2018'

config.Site.storageSite = 'T2_IT_Rome'
