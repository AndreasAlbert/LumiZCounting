#!/usr/bin/env python
#-*- coding:utf-8 -*-
import ROOT as r
import os
from ROOT import gSystem
gSystem.Load('libRooFit')
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData,RooBreitWigner,RooDataHist,RooVoigtian,RooCBShape,RooAddPdf,RooExponential,RooPolynomial,RooNumConvPdf,RooFFTConvPdf,RooHist,RooChi2Var,RooFitResult,RooMsgService,RooLinkedList,RooCMSShape
from cms_plot import create_tdr_style,add_text
import sys

MZ = 90
create_tdr_style(True)


def do_single_fit(h2d, run, sigpdf=None, bkgpdf=None):
   bin_number = h2d.Fill(run,0)
   h = h2d.ProjectionY("",bin_number,bin_number)


   dx = 10
   mass = RooRealVar("mass","M_{#mu#mu}",MZ-dx,MZ+dx,"GeV")
   mass.setRange(MZ-dx,MZ+dx)



   ### Signal PDF
   delta = max(2,h.GetRMS())
   if(not sigpdf):
      mean =  RooRealVar("mean","Peak Mass",MZ,MZ-5*delta,MZ+5*delta,"GeV")
      sigma = RooRealVar("sigma","Peak Width",1,0.1,50,"GeV")
      sig = RooBreitWigner("sig","sig",mass,mean,sigma);
   elif(sigpdf=="bwcrystal"):
      # Signal
      mean =  RooRealVar("mean","Peak Mass",MZ,MZ-3*delta,MZ+3*delta,"GeV")
      sigma = RooRealVar("sigma","Peak Width",1,0.001,10,"GeV")
      bw = RooBreitWigner("bw","bw",mass,mean,sigma);
   
      # Resolution
      resolution_mean =  RooRealVar("resolution_mean","resolution_mean",0,"GeV")
      resolution_width = RooRealVar("resolution_width","resolution_width",1,0.0001,10,"GeV")
      resolution_a = RooRealVar("a","a",1,0,4)
      resolution_n = RooRealVar("n","n",2,0,200)

      resolution = RooCBShape("CBShape", "Cystal Ball Function", mass, resolution_mean, resolution_width, resolution_a, resolution_n);

      # Convolution
      sig = RooFFTConvPdf("sig","sig",mass,bw,resolution)

   ### Background PDF
   y1 = h.GetBinContent(1)
   y2 = h.GetBinContent(h.GetNbinsX()-1)
   dy = y2-y1
   sy = 0.5 * (y2 + y1)


   if(not bkgpdf):
      #~ alpha= RooRealVar("alpha","alpha",sy,-1e3,1e3) ;
      alpha= RooRealVar("alpha","alpha",0) ;
      #~ beta = RooRealVar("beta","beta",dy / dx,-100./dx,100/dx) ;
      beta= RooRealVar("beta","beta",0) ;
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
   #~ fit_result = model.fitTo(dh,RooFit.Save(1))
   model.fitTo(dh,RooFit.Save(1))
   #~ model.chi2FitTo(dh,RooLinkedList())

   histos = []
   histos.append(h)
   c1 = r.TCanvas( 'c1','c1', 200, 10, 700, 500 )
   outdir="./pdf"
   if(not os.path.exists(outdir)):
      os.makedirs(outdir)

   frame = mass.frame(RooFit.Title(h2d.GetTitle().replace("h_ee_mass_",""))) ;
   dh.plotOn(frame)
   frame.Draw()
   #~ c1.SaveAs('{OUT}/run{RUN}_{TITLE}_nofit.pdf'.format(OUT=outdir,RUN=run,TITLE=h2d.GetTitle()))
   model.plotOn(frame)
   model.plotOn(frame,RooFit.Components('sig'),RooFit.LineStyle(r.kDashed))
   model.plotOn(frame,RooFit.Components('bkg'),RooFit.LineStyle(r.kDashed))
   frame.Draw()


   chi2 = RooChi2Var("chi2","chi2",model,dh) ;
   parameters = model.getParameters(dh);
   npar = parameters.selectByAttrib("Constant",r.kFALSE).getSize()
   
   texts = []
   if(sigpdf=="bwcrystal"):
      texts.append(add_text(0.65,0.95,0.7,0.9,["Breit-Wigner","Mean = ({0:.3f} #pm {1:.3f}) GeV".format(mean.getValV(),mean.getError()),"Width = ({0:.3f} #pm {1:.3f}) GeV".format(sigma.getValV(),sigma.getError())]))
      texts.append(add_text(0.65,0.95,0.4,0.7,["Crystal Ball",
                                  "Width = ({0:.3f} #pm {1:.3f}) GeV".format(resolution_width.getValV(),resolution_width.getError()),
                                  "a = {0:.3f} #pm {1:.3f}".format(resolution_a.getValV(),resolution_a.getError()),
                                  "n = {0:.3f} #pm {1:.3f}".format(resolution_n.getValV(),resolution_n.getError()),
                                  "",
                                  "\chi^{{2}}/NDF = {0:.1f} / {1:.0f}".format(chi2.getValV() , npar),
                                  "N_{{sig}} = {0:.0f}".format(dh.sumEntries() * (1-bkgfrac.getValV()))]))
                              
      for t in texts:
         t.SetFillStyle(1)
         t.SetFillColor(r.kWhite)


   c1.SaveAs('{OUT}/run{RUN}_{TITLE}.pdf'.format(OUT=outdir,RUN=run,TITLE=h2d.GetTitle()))


   return (1-bkgfrac.getValV()) * dh.sumEntries()
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
   sigpdf = "bwcrystal"
   n_fail = do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_HLT_fail"),run,sigpdf=sigpdf)
   n_pass = do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_HLT_pass"),run,sigpdf=sigpdf)
   print 'HLT Pass / Fail / Eff: ', n_pass, n_fail, n_pass/(n_pass + n_fail)

   n_fail = do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_id_fail"),run,sigpdf=sigpdf)
   n_pass = do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_id_pass"),run,sigpdf=sigpdf)
   print 'ID Pass / Fail / Eff: ', n_pass, n_fail, n_pass/(n_pass + n_fail)
