#!/usr/bin/env python
#-*- coding:utf-8 -*-
import ROOT as r
import os
from ROOT import gSystem
gSystem.Load('libRooFit')
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData,RooBreitWigner,RooDataHist,RooVoigtian,RooCBShape,RooAddPdf,RooExponential,RooPolynomial,RooNumConvPdf,RooFFTConvPdf,RooHist,RooChi2Var,RooFitResult,RooMsgService,RooLinkedList,RooCMSShape
from cms_plot import create_tdr_style,add_text
import sys
from tabulate import tabulate

r.gROOT.SetBatch(1)
MZ = 90
create_tdr_style(True)

#~ RooMsgService.instance().SetStreamStatus(1,false);
#~ print dir(RooMsgService.instance())
RooMsgService.instance().setStreamStatus(0,False);
RooMsgService.instance().setStreamStatus(1,False);
RooMsgService.instance().setStreamStatus(2,False);
RooMsgService.instance().setSilentMode(True);
#~ r.gErrorIgnoreLevel = r.kError
REBIN=10
def do_single_fit(h2d, run, ibin, sigpdf=None, bkgpdf=None):
   h2d.RebinX(REBIN)
   h = h2d.ProjectionY("",ibin,ibin)
   if(h.Integral() == 0): return 0
   ls = int(h2d.GetXaxis().GetBinCenter(ibin) - 0.5 * h2d.GetXaxis().GetBinWidth(ibin))


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
      alpha= RooRealVar("alpha","alpha",0,0,100) ;
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
                                  "\chi^{{2}}/NDF = {0:.3f} / {1:.0f}".format(chi2.getValV() , npar),
                                  "N_{{sig}} = {0:.0f}".format(dh.sumEntries() * (1-bkgfrac.getValV()))]))

      for t in texts:
         t.SetFillStyle(1)
         t.SetFillColor(r.kWhite)


   c1.SaveAs('{OUT}/run{RUN}_ls{LS}_{TITLE}.pdf'.format(OUT=outdir,RUN=run,LS=ls,TITLE=h2d.GetTitle()))


   return (1-bkgfrac.getValV()) * dh.sumEntries()
#~ path_to_file = "/disk1/albert/zcounting/dqmoffline/CMSSW_9_0_0/src/DQMOffline/LumiZCounting/DQM_V0001_R000281616__SingleMuon__Run2016H-PromptReco-v2__RECO.root"

def main():
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


   fout = r.TFile("fit_out.root","RECREATE")
   runs = [ int(x.GetTitle().replace("Run ","")) for x in list(f.Get("DQMData").GetListOfKeys()) ]
   for run in runs:
      table = []
      base = "DQMData/Run {RUN}/ZCounting/Run summary/Histograms/"
      h = f.Get(base.format(RUN=run) + "h_ee_mass_HLT_fail").Clone()
      h.RebinX(REBIN)
      lumis = [h.GetXaxis().GetBinCenter(i) - 0.5 * h.GetXaxis().GetBinWidth(i) for i in range(1,h.GetNbinsX()+1)]
      print lumis

      ### Set up histograms to use as input for TEfficiency
      h_fail_hlt = h.ProjectionX("tmppp",1,1).Clone("h_fail_hlt")
      h_fail_hlt.Reset()
      h_pass_hlt = h_fail_hlt.Clone("h_pass_hlt")
      h_pass_id = h_fail_hlt.Clone("h_pass_id")
      h_fail_id = h_fail_hlt.Clone("h_fail_id")

      nls = len(lumis)
      for ibin,ls in enumerate(lumis):
         print "{0}/{1}".format(ibin,nls)
         #~ if(ibin>3):break
         ### Do the fits
         sigpdf = "bwcrystal"
         n_fail_hlt = do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_HLT_fail").Clone(),run,ibin,sigpdf=sigpdf)
         n_pass_hlt = do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_HLT_pass").Clone(),run,ibin,sigpdf=sigpdf)

         n_fail_id = do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_id_fail").Clone(),run,ibin,sigpdf=sigpdf)
         n_pass_id = do_single_fit(f.Get(base.format(RUN=run)+"h_ee_mass_id_pass").Clone(),run,ibin,sigpdf=sigpdf)

         ### Fill the histos
         for i in range(int(n_fail_hlt)): h_fail_hlt.Fill(ls)
         for i in range(int(n_pass_hlt)): h_pass_hlt.Fill(ls)
         for i in range(int(n_fail_id)): h_fail_id.Fill(ls)
         for i in range(int(n_pass_id)): h_pass_id.Fill(ls)

         ### Fill Table
         try:
            eff_hlt = n_pass_hlt/(n_pass_hlt + n_fail_hlt)
         except ZeroDivisionError:
            eff_hlt = -1
         try:
            eff_id = n_pass_id/(n_pass_id + n_fail_id)
         except ZeroDivisionError:
            eff_id = -1
         if(eff_id == -1 and eff_hlt == -1 ):continue
         table.append([run,int(ls),n_fail_hlt,n_pass_hlt,eff_hlt,n_fail_id,n_pass_id,eff_id])


      ### Set up TEfficiency
      h_total_hlt = h_pass_hlt.Clone()
      h_total_hlt.Add(h_fail_hlt)
      teff_hlt = r.TEfficiency(h_pass_hlt,h_total_hlt)

      h_total_id = h_pass_id.Clone()
      h_total_id.Add(h_fail_id)
      teff_id = r.TEfficiency(h_pass_id,h_total_id)

      ### Plot efficiency
      c3 = r.TCanvas( 'c3','c3', 200, 10, 700, 500 )
      teff_hlt.Draw("APE")
      teff_id.Draw("PE,SAME")
      r.gPad.Update()
      teff_hlt.GetPaintedGraph().SetMinimum(0)
      teff_hlt.GetPaintedGraph().SetMaximum(1)
      teff_id.SetLineColor(r.kRed)
      c3.SaveAs("test.pdf")

      ### Print table
      print tabulate(table,headers=["Run","LS","HLT Fail","HLT Pass","HLT eff.","ID Fail","ID Pass", "ID Eff."],floatfmt=".2f")

      ### Write everything to file
      subdir = fout.mkdir("run{RUN}".format(RUN=run))
      subdir.cd()
      h_pass_hlt.Write()
      h_fail_hlt.Write()
      h_pass_id.Write()
      h_fail_id.Write()
      teff_hlt.Write()
      teff_id.Write()
   fout.Close()
   f.Close()

if __name__ == '__main__':
   main()
