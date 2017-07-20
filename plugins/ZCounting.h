#ifndef ZCounting_H
#define ZCounting_H

#include "FWCore/Framework/interface/MakerMacros.h"      // definitions for declaring plug-in modules
#include "FWCore/Framework/interface/Frameworkfwd.h"     // declaration of EDM types
#include "FWCore/Framework/interface/EDAnalyzer.h"       // EDAnalyzer class
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"  // Parameters
#include "FWCore/Utilities/interface/InputTag.h"

#include <string>                                        // string class
#include <TMath.h>
#include <cassert>

#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/EgammaCandidates/interface/ElectronFwd.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

#include "DQMServices/Core/interface/DQMEDAnalyzer.h"
#include "DQMServices/Core/interface/DQMStore.h"
#include "DQMServices/Core/interface/MonitorElement.h"

#include "DQMOffline/LumiZCounting/interface/MiniBaconDefs.h"
#include "DQMOffline/LumiZCounting/interface/TTrigger.h"
#include "DQMOffline/LumiZCounting/interface/TriggerTools.h"
#include "DQMOffline/LumiZCounting/interface/ElectronIdentifier.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


class TFile;
class TH1D;
class TTree;
class TClonesArray;
namespace edm {
  class TriggerResults;
  class TriggerNames;
}
namespace baconhep {
  class TTrigger;
}

class ZCounting: public DQMEDAnalyzer{

public:

  ZCounting(const edm::ParameterSet& ps);
  virtual ~ZCounting();

protected:

  void dqmBeginRun(edm::Run const &, edm::EventSetup const &) override;
  void bookHistograms(DQMStore::IBooker &, edm::Run const &, edm::EventSetup const &) override;
  void analyze(edm::Event const& e, edm::EventSetup const& eSetup) override;
  void beginLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& eSetup) override ;
  void endLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& eSetup) override;

private:
  void analyze_electrons(edm::Event const& e, edm::EventSetup const& eSetup);
  //other functions

  bool isMuonTrigger(baconhep::TTrigger triggerMenu, TriggerBits hltBits);
  bool isMuonTriggerObj(baconhep::TTrigger triggerMenu, TriggerObjects hltMatchBits);

  bool isElectronTrigger(baconhep::TTrigger triggerMenu, TriggerBits hltBits);
  bool isElectronTriggerObj(baconhep::TTrigger triggerMenu, TriggerObjects hltMatchBits);

  bool passMuonID(const reco::Muon& muon, const reco::Vertex& vtx, const std::string idType);
  bool passMuonIso(const reco::Muon& muon, const std::string isoType, const float isoCut);

  bool passElectronID(const reco::GsfElectron& electron, const reco::Vertex& vtx, const std::string idType);

  // specify trigger paths of interest
  void setTriggers();

  // initialization from HLT menu; needs to be called on every change in HLT menu
  void initHLT(const edm::TriggerResults&, const edm::TriggerNames&);

  // EDM object collection names
  edm::ParameterSetID fTriggerNamesID;
  std::string         fHLTFile;
  edm::InputTag       fHLTObjTag;
  edm::InputTag       fHLTTag;
  edm::EDGetTokenT<trigger::TriggerEvent> fHLTObjTag_token;
  edm::EDGetTokenT<edm::TriggerResults> fHLTTag_token;
  std::string fPVName;
  edm::EDGetTokenT<reco::VertexCollection> fPVName_token;
  std::string fMuonName;
  edm::EDGetTokenT<reco::MuonCollection> fMuonName_token;
  std::string fTrackName;
  edm::EDGetTokenT<reco::TrackCollection> fTrackName_token;

  // Electrons
  std::string fElectronName;
  edm::EDGetTokenT<edm::View<reco::GsfElectron>> fGsfElectronName_token;
  std::string fSCName;
  edm::EDGetTokenT<edm::View<reco::SuperCluster>> fSCName_token;



  edm::InputTag fRhoTag;
  edm::EDGetTokenT<double> fRhoToken;

  edm::InputTag fBeamspotTag;
  edm::EDGetTokenT<reco::BeamSpot> fBeamspotToken;

  edm::InputTag fConversionTag;
  edm::EDGetTokenT<reco::ConversionCollection> fConversionToken;


  edm::EDGetTokenT<edm::ValueMap<bool> > eleIdMapToken_;
  // bacon fillers
  baconhep::TTrigger        *fTrigger;

  std::string IDType_;
  std::string IsoType_;
  double IsoCut_;

  ElectronIdentifier EleID_;
  //~ GsfEleMissingHitsCut GsfCutMissingHits;
  double PtCutL1_;
  double PtCutL2_;
  double EtaCutL1_;
  double EtaCutL2_;

  int    MassBin_;
  double MassMin_;
  double MassMax_;

  int    LumiBin_;
  double LumiMin_;
  double LumiMax_;

  int    PVBin_;
  double PVMin_;
  double PVMax_;

  double VtxNTracksFitCut_;
  double VtxNdofCut_;
  double VtxAbsZCut_;
  double VtxRhoCut_;

  bool IsData_;
  const Double_t MUON_MASS  = 0.105658369;
  const Double_t MUON_BOUND = 0.9;

  const Double_t ELECTRON_MASS  = 0.000511;

  const Double_t ELE_PT_CUT_TAG = 40;
  const Double_t ELE_PT_CUT_PROBE = 35;
  const Double_t ELE_ETA_CUT_TAG = 2.5;
  const Double_t ELE_ETA_CUT_PROBE = 2.5;

  const Double_t ELE_ETA_CRACK_LOW = 1.4442;
  const Double_t ELE_ETA_CRACK_HIGH = 1.56;
    
  
  // Histograms
  MonitorElement* h_mass_HLT_pass_central;
  MonitorElement* h_mass_HLT_pass_forward;
  MonitorElement* h_mass_HLT_fail_central;
  MonitorElement* h_mass_HLT_fail_forward;

  MonitorElement* h_mass_SIT_pass_central;
  MonitorElement* h_mass_SIT_pass_forward;
  MonitorElement* h_mass_SIT_fail_central;
  MonitorElement* h_mass_SIT_fail_forward;

  MonitorElement* h_mass_Sta_pass_central;
  MonitorElement* h_mass_Sta_pass_forward;
  MonitorElement* h_mass_Sta_fail_central;
  MonitorElement* h_mass_Sta_fail_forward;

  MonitorElement* h_npv;
  MonitorElement* h_yield_Z;

  MonitorElement* h_ee_mass_id_pass;
  MonitorElement* h_ee_mass_id_fail;
                                 ;
  MonitorElement* h_ee_mass_HLT_pass;
  MonitorElement* h_ee_mass_HLT_fail;

  MonitorElement* h_ee_yield_Z;

  MonitorElement* h_ee_cutflow;
  
  TH2D * h_ee_mass_id_pass_debug;
  TH2D * h_ee_mass_id_fail_debug;
  TH2D * h_ee_mass_HLT_pass_debug;
  TH2D * h_ee_mass_HLT_fail_debug;

  TH1D * h_ee_yield_Z_debug;


  edm::Service<TFileService> fileservice;
};


#endif
