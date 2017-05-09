#ifndef DQMOFFLINE_LUMIZCOUNTING_LINKDEF_H
#define DQMOFFLINE_LUMIZCOUNTING_LINKDEF_H
#include "DQMOffline/LumiZCounting/interface/TEventInfo.h"
#include "DQMOffline/LumiZCounting/interface/TMuon.h"
#include "DQMOffline/LumiZCounting/interface/TVertex.h"
#endif

#ifdef __CINT__
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclass;
#pragma link C++ nestedtypedef;
#pragma link C++ namespace baconhep;

#pragma link C++ class baconhep::TEventInfo+;
#pragma link C++ class baconhep::TMuon+;
#pragma link C++ class baconhep::TVertex+;
#endif
