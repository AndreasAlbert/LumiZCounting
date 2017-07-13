#!/usr/bin/env python
#-*- coding:utf-8 -*-
import ROOT as r
import os
from ROOT import gSystem
gSystem.Load('libRooFit')
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData,RooBreitWigner,RooDataHist,RooVoigtian,RooCBShape,RooAddPdf,RooExponential,RooPolynomial,RooNumConvPdf,RooFFTConvPdf,RooHist,RooChi2Var,RooFitResult,RooMsgService,RooLinkedList,RooCMSShape
from cms_plot import create_tdr_style,add_text
import sys

MZ = 91
create_tdr_style(True)


def do_single_fit(h2d, run, sigpdf=None, bkgpdf=None):
   bin_number = h2d.Fill(run,0)
   h = h2d.ProjectionY("",bin_number,bin_number)


   dx = 10
   mass = RooRealVar("mass","M_{#mu#mu}",MZ-dx,MZ+dx,"GeV")
   mass.setRange(MZ-dx,MZ+dx)


   
   ### Signal PDF
   if(not sigpdf):
      delta = min(2,h.GetRMS())
      mean =  RooRealVar("mean","Peak Mass",MZ,MZ-5*delta,MZ+5*delta,"GeV")
      sigma = RooRealVar("sigma","Peak Width",1,0.01,10,"GeV")
      sig = RooBreitWigner("sig","sig",mass,mean,sigma);

   ### Background PDF
   y1 = h.GetBinContent(1)
   y2 = h.GetBinContent(h.GetNbinsX()-1)
   dy = y2-y1
   sy = 0.5 * (y2 + y1)


   if(not bkgpdf):
      alpha= RooRealVar("alpha","alpha",sy,0,100) ;
      beta= RooRealVar("beta","beta",dy / dx,-100./dx,100/dx) ;
      bkg = RooPolynomial("bkg","Background",mass,RooArgList(alpha,beta),0) ;
   elif(bkgpdf.lower()=="cms"):
      alpha= RooRealVar("alpha","alpha",sy,0,100) ;
      beta= RooRealVar("beta","beta",0.5,0,1) ;
      gamma= RooRealVar("gamma","gamma",0.5,0,1) ;
      peak = RooRealVar("peak","peak",0.5,0,1) ;
   

   bkgfrac=RooRealVar("bkgfrac","fraction of background",0.5,0.,1.) ;

   
   ### Final Model
   model=RooAddPdf("model","bkg+signal",RooArgList(bkg,sig),RooArgList(bkgfrac)) ;

#~ 
   dh = RooDataHist("dh","dh",RooArgList(mass),h,1) ;
   fit_result = model.fitTo(dh,RooFit.Save(1))
   
   histos = []
   histos.append(h)
   c1 = r.TCanvas( 'c1','c1', 200, 10, 700, 500 )
   
   frame = mass.frame() ;
   dh.plotOn(frame)
   model.plotOn(frame)
   model.plotOn(frame,RooFit.Components('sig'),RooFit.LineStyle(r.kDashed))
   model.plotOn(frame,RooFit.Components('bkg'),RooFit.LineStyle(r.kDashed))
   frame.Draw()
   t=add_text(0.6,0.9,0.7,0.9,["Breit-Wigner","Mean = ({0:.3f} #pm {1:.3f}) GeV".format(mean.getValV(),mean.getError()),"Width = ({0:.3f} #pm {1:.3f}) GeV".format(sigma.getValV(),sigma.getError())])
   c1.SaveAs('run{RUN}.pdf'.format(RUN=run))
   
   #~ return (1-bkgfrac.getValV()) * 
#~ path_to_file = "/disk1/albert/zcounting/dqmoffline/CMSSW_9_0_0/src/DQMOffline/LumiZCounting/DQM_V0001_R000281616__SingleMuon__Run2016H-PromptReco-v2__RECO.root"

path_to_file = sys.argv[1]
if(not os.path.exists(path_to_file)):
   print "File does not exist:" + path_to_file
   print "Exiting"
   sys.exit(1)
f = r.TFile(path_to_file)
if(not f):
   print "Could not open file:" + path_to_file
   print "Exiting"
   sys.exit(1)

   
runs = [ int(x.GetTitle().replace("Run ","")) for x in list(f.Get("DQMData").GetListOfKeys()) ]
base = "DQMData/Run {RUN}/ZCounting/Run summary/Histograms/"
print runs
for run in runs:
   #~ do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_HLT_fail"),run)
   do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_id_fail"),run)
