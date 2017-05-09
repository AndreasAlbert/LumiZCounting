import FWCore.ParameterSet.Config as cms

process = cms.Process('RECODQM')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/GeometryDB_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load('TrackingTools/TransientTrack/TransientTrackBuilder_cfi')
process.load('Configuration.StandardSequences.EDMtoMEAtRunEnd_cff')

# load DQM
process.load("DQMServices.Core.DQM_cfg")
process.load("DQMServices.Components.DQMEnvironment_cfi")

# my analyzer
process.load('DQMOffline.LumiZCounting.SelectZmm_cfi')

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v3'

from CondCore.CondDB.CondDB_cfi import *

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
'/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/693/00000/000146F7-1686-E611-BD78-FA163E90B8E2.root',
#'/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/727/00000/000744C8-D286-E611-BBEE-02163E012677.root'
                                )
                                )
process.source.inputCommands = cms.untracked.vstring("keep *",
                                                         "drop *_MEtoEDMConverter_*_*")

process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(False),
  Rethrow     = cms.untracked.vstring('ProductNotFound'),
  fileMode    = cms.untracked.string('NOMERGE')
  )

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
                                     fileName = cms.untracked.string("OUT_step1.root"))

# Path and EndPath definitions
process.dqmoffline_step = cms.Path(process.zcounting)
process.dqmsave_step = cms.Path(process.DQMSaver)
#process.DQMoutput_step = cms.EndPath(process.DQMoutput)


# Schedule definition
process.schedule = cms.Schedule(
    process.dqmoffline_step,
#    process.DQMoutput_step
    process.dqmsave_step
    )

process.dqmSaver.workflow = '/SingleMuon/Run2016H-PromptReco-v2/RECO'
