#ifndef DQMOFFLINE_LUMIZCOUNTING_FILLEREVENTINFO_H
#define DQMOFFLINE_LUMIZCOUNTING_FILLEREVENTINFO_H

#include <string>
#include "FWCore/Framework/interface/Frameworkfwd.h"     // declaration of EDM types
#include "FWCore/Framework/interface/EDAnalyzer.h"       // EDAnalyzer class
#include "FWCore/ParameterSet/interface/ParameterSet.h"  // Parameters
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/MakerMacros.h"      // definitions for declaring plug-in modules
#include "FWCore/Framework/interface/ConsumesCollector.h"

// forward class declarations
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DQMOffline/LumiZCounting/interface/MiniBaconDefs.h"
namespace trigger {
  class TriggerEvent;
}


namespace baconhep
{
  class TEventInfo;  // foward declaration
  class FillerEventInfo
  {
    public:
    FillerEventInfo(const edm::ParameterSet &iConfig,edm::ConsumesCollector && iC);
      ~FillerEventInfo();
      
      void fill(TEventInfo         *evtInfo,       // output object to be filled
                const edm::Event   &iEvent,        // EDM event info
		const reco::Vertex &pv,            // event primary vertex
		const bool          hasGoodPV,     // flag for if PV passing cuts is found
		const TriggerBits   triggerBits);//,   // bits for corresponding fired triggers
//		TSusyGen           *susyGen=0);      // output for SUSY objects
	       
    protected:
    
  };
}
#endif
