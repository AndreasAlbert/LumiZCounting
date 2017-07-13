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

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v3'

# trigger filter
import os
cmssw_base = os.environ['CMSSW_BASE']
hlt_filename = "DQMOffline/LumiZCounting/data/HLT_50nsGRun"
process.load('HLTrigger/HLTfilters/hltHighLevel_cfi')
process.hltHighLevel.throw = cms.bool(False)
process.hltHighLevel.HLTPaths = cms.vstring()


from CondCore.CondDB.CondDB_cfi import *

hlt_file = open(cmssw_base + "/src/" + hlt_filename, "r")
for line in hlt_file.readlines():
  line = line.strip()              # strip preceding and trailing whitespaces
  if (line[0:3] == 'HLT'):         # assumes typical lines begin with HLT path name (e.g. HLT_Mu15_v1)
    hlt_path = line.split()[0]
    process.hltHighLevel.HLTPaths.extend(cms.untracked.vstring(hlt_path))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                #~ 'file:/disk1/albert/cms_data/reco/Run2016H/SingleElectron/429D95FC-5785-E611-82AD-02163E0140F5.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/612/00000/6E6F18FB-7484-E611-8BE1-02163E014313.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/1816C32D-A684-E611-8DC8-FA163E837358.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/26027F5E-A684-E611-833A-02163E0133DE.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/30ABA327-A684-E611-8882-02163E01434F.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/32AB99D1-B384-E611-AFFD-FA163E69A996.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/340F39F4-B384-E611-BF90-02163E013759.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/4AEFC7E2-B384-E611-A953-02163E014550.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/4E56B9EA-B384-E611-8883-02163E014132.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/4E66F97A-B584-E611-81EB-FA163E60DE95.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/4E799EDD-B384-E611-A22F-FA163E5A1011.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/6A786A05-B484-E611-9B19-02163E0134AF.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/6C52DBC1-5985-E611-94DB-02163E012AA5.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/6C6EBEF0-B384-E611-B0A5-02163E014476.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/828CBB3C-B484-E611-A84C-02163E013406.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/86814F05-B484-E611-A473-02163E014609.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/8E61E332-A684-E611-AF28-FA163E55C63B.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/A6BE2509-B484-E611-8E8C-02163E014749.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/B0DE45F6-B384-E611-8585-02163E01427B.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/C2C3291B-B484-E611-9737-02163E0134BF.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/D27C52E3-B384-E611-BF81-FA163ECBB35D.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/D49E77DB-B384-E611-A156-FA163E9E4DE4.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/DA91C5DB-B784-E611-A55F-FA163EEB44F9.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/DE226307-B484-E611-9320-02163E014199.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/E87FC7E6-B384-E611-B9EA-FA163E1309A1.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/EAE95F14-B484-E611-876E-FA163E1BACC3.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/F4B42A41-A684-E611-B0F6-02163E0135FB.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/613/00000/FE530E41-A684-E611-B745-02163E012816.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/0C3B7BA2-D384-E611-BDF9-02163E012715.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/12B382B3-D384-E611-8AC4-FA163EF32538.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/1EAE65BA-D384-E611-985C-02163E01263D.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/26508591-D384-E611-841D-FA163E4C67D9.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/2868FC96-D384-E611-A186-02163E01437E.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/28E305BD-D384-E611-966A-02163E011CAC.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/2AAF6AAD-D384-E611-9B5C-02163E011C65.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/2ED807CA-D384-E611-864B-02163E01357C.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/4A2925C2-D384-E611-AC8A-02163E013963.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/720A40A3-D384-E611-B363-02163E01355F.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/72C14CA8-D384-E611-9975-02163E0118E1.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/7480DEA5-D384-E611-AD13-02163E012B1B.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/78FD54BD-D384-E611-B0DC-02163E0126CD.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/82FB86D3-D384-E611-8FF9-02163E0119D3.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/86B085AD-D384-E611-B31B-02163E01288B.root',
                                '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/88D12F9F-D384-E611-9D59-02163E011B2A.root', ### THIS
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/8E15A2A6-D384-E611-948B-02163E01419A.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/AA0A04BB-D384-E611-883A-02163E01249F.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/D2E394A1-D384-E611-AF6C-02163E0141A4.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/D8012ACF-D384-E611-A3FF-02163E011D59.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/DA70109B-D384-E611-AC37-FA163E61D84C.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/DA836CA4-D384-E611-B2C4-02163E0122A2.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/E2A7A250-2985-E611-A8DA-02163E0146A0.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/F4F7ABB8-D384-E611-9254-02163E011A16.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/F6FD8DA6-D384-E611-B4AC-02163E01457B.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/FACEE2A9-D384-E611-AE4B-02163E012B4C.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/616/00000/FEE82AA8-D384-E611-A3C1-02163E01355B.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/624/00000/487F083F-ED84-E611-AB7D-02163E01343D.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/626/00000/26D646C5-0285-E611-9E8D-02163E0140E3.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/632/00000/BC5594D4-1785-E611-B24D-FA163E65E93C.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/636/00000/803D0C5B-4F85-E611-A9E9-02163E01462D.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/637/00000/C4A2FE58-5185-E611-A38E-FA163EA86425.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/638/00000/786492FF-5085-E611-983B-02163E011E15.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/0054A4EC-5785-E611-BA96-FA163E823565.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/0403C707-5885-E611-9EBC-02163E014772.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/08756705-5885-E611-BACC-02163E011B5C.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/0E5F56FE-5785-E611-9B56-02163E01453F.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/10DFBA0D-5885-E611-8B8B-02163E0135DD.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/121EBE00-5885-E611-B240-02163E012B5A.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/144593FD-5785-E611-8242-02163E014262.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/188544FE-5785-E611-905A-02163E014497.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/18AF26FC-5785-E611-A654-02163E0141BA.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/266D2AF0-5785-E611-989E-FA163E95898B.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/288D1128-5885-E611-B8D0-02163E012A43.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/2EED9DF4-5785-E611-828F-02163E0144A5.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/30C94E0B-5885-E611-A190-02163E011DC7.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/3634CC12-5885-E611-B9A4-02163E013393.root',
                                #~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/281/639/00000/36E5DA07-5885-E611-9704-02163E014772.root'
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/001082E6-9E87-E611-94E2-FA163EA5F432.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/00120EEF-9E87-E611-BB98-FA163ED6E8DE.root",
                                #~ "file:/disk1/albert/zcounting/dqmoffline/CMSSW_9_0_0/src/DQMOffline/LumiZCounting/input/SingleMuon/001082E6-9E87-E611-94E2-FA163EA5F432.root",
                                #~ "file:/disk1/albert/zcounting/dqmoffline/CMSSW_9_0_0/src/DQMOffline/LumiZCounting/input/SingleMuon/00120EEF-9E87-E611-BB98-FA163ED6E8DE.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/0037FC7F-7887-E611-A515-02163E014735.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/0079EF77-7887-E611-AAFF-02163E01199C.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/007A1E6E-9D87-E611-B114-02163E01420D.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/0083A01B-A187-E611-9B14-02163E0138E9.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/00C12B85-7887-E611-B869-02163E011ADF.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/00F3D963-7887-E611-9A2F-FA163E609329.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/797/00000/02CE9F64-7A87-E611-9B27-02163E0141C5.root",
                                #~ "/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/382/00000/9EDFAA2D-F882-E611-9F3A-FA163E940FAB.root"
                                
#~ '/store/data/Run2016H/SingleMuon/RECO/PromptReco-v2/000/281/727/00000/000744C8-D286-E611-BBEE-02163E012677.root'                              
#~ '/store/data/Run2016H/SingleElectron/RECO/PromptReco-v2/000/284/035/00000/F85C82FE-ED9E-E611-B34B-FA163E9907EA.root'

                                )
                                )
process.source.inputCommands = cms.untracked.vstring("keep *",
                                                         "drop *_MEtoEDMConverter_*_*")

process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(False),
  Rethrow     = cms.untracked.vstring('ProductNotFound'),
  fileMode    = cms.untracked.string('NOMERGE')
  )
#~ 
#~ ### VID BEGIN
#~ from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
#~ # turn on VID producer, indicate data format  to be
#~ # DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
#~ if False :
    #~ dataFormat = DataFormat.AOD
#~ else :
    #~ dataFormat = DataFormat.MiniAOD
#~ 
#~ switchOnVIDElectronIdProducer(process, dataFormat)
#~ 
#~ # define which IDs we want to produce
#~ my_id_modules = [
    #~ 'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff'
    #~ ]
#~ 
#~ #add them to the VID producer
#~ for idmod in my_id_modules:
    #~ setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
#~ ### VID END
    #~ 
process.zcounting = cms.EDAnalyzer('ZCounting',
                                  TriggerFile     = cms.untracked.string(hlt_filename),
                                  TriggerEvent    = cms.InputTag('hltTriggerSummaryAOD','','HLT'),
                                  TriggerResults  = cms.InputTag('TriggerResults','','HLT'),
                                  edmPVName       = cms.untracked.string('offlinePrimaryVertices'),
                                  edmName       = cms.untracked.string('muons'),
                                  
                                  edmTrackName = cms.untracked.string('generalTracks'),
  
                                  edmGsfEleName = cms.untracked.string('gedGsfElectrons'),
                                  edmSCName = cms.untracked.string('particleFlowEGamma'),
                                  #~ eleIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1"),
  
                                  effAreasConfigFile = cms.FileInPath("RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt"),
  
                                  rhoname = cms.InputTag('fixedGridRhoFastjetAll'),
                                  beamspotName = cms.InputTag('offlineBeamSpot'),
                                  conversionsName = cms.InputTag('conversions'),
                                  IDType   = cms.untracked.string("Medium"),# Tight, Medium, Loose
                                  IsoType  = cms.untracked.string("NULL"),  # Tracker-based, PF-based
                                  IsoCut   = cms.untracked.double(0.),     # {0.05, 0.10} for Tracker-based, {0.15, 0.25} for PF-based
  
                                  PtCutL1  = cms.untracked.double(27.0),
                                  PtCutL2  = cms.untracked.double(27.0),
                                  EtaCutL1 = cms.untracked.double(2.4),
                                  EtaCutL2 = cms.untracked.double(2.4),
  
                                  MassBin  = cms.untracked.int32(50),
                                  MassMin  = cms.untracked.double(66.0),
                                  MassMax  = cms.untracked.double(116.0),
  
                                  LumiBin  = cms.untracked.int32(400),
                                  LumiMin  = cms.untracked.double(0.0),
                                  LumiMax  = cms.untracked.double(2000.0),
  
                                  PVBin    = cms.untracked.int32(60),
                                  PVMin    = cms.untracked.double(0.0),
                                  PVMax    = cms.untracked.double(60.0),
  
                                  VtxNTracksFitMin = cms.untracked.double(0.),
                                  VtxNdofMin       = cms.untracked.double(4.),
                                  VtxAbsZMax       = cms.untracked.double(24.),
                                  VtxRhoMax        = cms.untracked.double(2.),

                                  IsData = cms.untracked.bool(True)
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
