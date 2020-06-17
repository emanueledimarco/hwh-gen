from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'step_1_premixraw_TJZZ_2018'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'hwh_1_cfg.py'
config.JobType.allowUndistributedCMSSW = True # this is to run the GEN-SIM for 2018 in CMSSW_10_6_12
config.JobType.maxMemoryMB = 4000

#config.Data.inputDataset = '/TJWW_1l_2018_GENSIM/emanuele-step_0_fromLHE_TJWW_1l_2018-32f87610ed172b187077c1c71278d822/USER'
#config.Data.inputDataset = '/TJWW_2l_2018_GENSIM/emanuele-step_0_fromLHE_TJWW_2l_2018-32f87610ed172b187077c1c71278d822/USER'
#config.Data.inputDataset = '/TJWZ_2018_GENSIM/emanuele-step_0_fromLHE_TJWZ_2018-32f87610ed172b187077c1c71278d822/USER'
config.Data.inputDataset = '/TJZZ_2018_GENSIM/emanuele-step_0_fromLHE_TJZZ_2018-32f87610ed172b187077c1c71278d822/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = True
config.Data.outputDatasetTag = 'step_1_premixraw_TJZZ_2018'

config.Site.storageSite = 'T2_IT_Rome'
