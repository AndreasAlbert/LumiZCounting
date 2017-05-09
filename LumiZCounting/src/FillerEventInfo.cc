#include "DQMOffline/LumiZCounting/interface/FillerEventInfo.h"
#include "DQMOffline/LumiZCounting/interface/TEventInfo.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include <TLorentzVector.h>
#include <string>

using namespace baconhep;

//--------------------------------------------------------------------------------------------------
FillerEventInfo::FillerEventInfo(const edm::ParameterSet &iConfig,edm::ConsumesCollector && iC)
{
}

//--------------------------------------------------------------------------------------------------
FillerEventInfo::~FillerEventInfo(){}

//--------------------------------------------------------------------------------------------------
void FillerEventInfo::fill(TEventInfo *evtInfo,
                           const edm::Event &iEvent, const reco::Vertex &pv,
                           const bool hasGoodPV,
			   const TriggerBits triggerBits)//,TSusyGen *iSusyGen)
{
  assert(evtInfo);
  
  evtInfo->runNum  = iEvent.id().run();
  evtInfo->lumiSec = iEvent.luminosityBlock();
  evtInfo->evtNum  = iEvent.id().event();

  //
  // primary vertex info
  //==============================
  evtInfo->hasGoodPV  = hasGoodPV;
 
  //
  // fired triggers
  //==============================
  evtInfo->triggerBits = triggerBits;
}
