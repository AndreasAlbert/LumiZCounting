import FWCore.ParameterSet.Config as cms
# trigger filter
import os
cmssw_base = os.environ['CMSSW_BASE']
hlt_filename = "DQMOffline/LumiZCounting/data/HLT_50nsGRun"
process.load('HLTrigger/HLTfilters/hltHighLevel_cfi')
process.hltHighLevel.throw = cms.bool(False)
process.hltHighLevel.HLTPaths = cms.vstring()

hlt_file = open(cmssw_base + "/src/" + hlt_filename, "r")
for line in hlt_file.readlines():
  line = line.strip()              # strip preceding and trailing whitespaces
  if (line[0:3] == 'HLT'):         # assumes typical lines begin with HLT path name (e.g. HLT_Mu15_v1)
    hlt_path = line.split()[0]
    process.hltHighLevel.HLTPaths.extend(cms.untracked.vstring(hlt_path))

is_data_flag = True
do_hlt_filter = False
process.zcounting = cms.EDAnalyzer('SelectZmm',
                                 #outputName     = cms.untracked.string('Output.root'),
                                 skipOnHLTFail  = cms.untracked.bool(do_hlt_filter),
                                 TriggerFile    = cms.untracked.string(hlt_filename),
                                 TriggerEvent   = cms.InputTag('hltTriggerSummaryAOD','','HLT'),
                                 TriggerResults = cms.InputTag('TriggerResults','','HLT'),

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

                                 Info = cms.untracked.PSet(
    ),

                                 PV = cms.untracked.PSet(
    edmName       = cms.untracked.string('offlinePrimaryVertices'),
    minNTracksFit = cms.untracked.uint32(0),
    minNdof       = cms.untracked.double(4),
    maxAbsZ       = cms.untracked.double(24),
    maxRho        = cms.untracked.double(2)
    ),

                                 Muon = cms.untracked.PSet(
    minPt         = cms.untracked.double(20),
    edmName       = cms.untracked.string('muons'),
    edmPFCandName = cms.untracked.string('particleFlow'),

    # save general tracker tracks in our muon collection (used in tag-and-probe for muons)
    minTrackPt   = cms.untracked.double(20),
    edmTrackName = cms.untracked.string('generalTracks')

    ),
                                 )
