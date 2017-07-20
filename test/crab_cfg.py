from WMCore.Configuration import Configuration 
import datetime

config = Configuration()

config.section_("General")
config.General.requestName = 'dqmoffline_'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
config.General.workArea = './crab/'
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'ANALYSIS'
config.JobType.psetName = './python/ZCounting_ele_cfg.py'
config.JobType.pyCfgParams = []
config.JobType.outputFiles = ['histo.root']

config.section_("Data")
config.Data.inputDataset = '/SingleElectron/Run2016G-03Feb2017-v1/RECO'
config.Data.inputDBS = 'global'
config.Data.publication = False
#~ config.Data.publishDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 300
config.Data.outLFNDirBase = '/store/user/aalbert/dqmoffline' # e.g. /store/user/aalbert/myFolder 
config.Data.outputDatasetTag = 'Run2016G-03Feb2017-v1' # e.g. 76X_mcRun2_asymptotic_RunIIFall15DR76_v1

config.section_("Site")
config.Site.storageSite = 'T2_DE_RWTH'

config.section_("User")
config.User.voGroup = 'dcms'
