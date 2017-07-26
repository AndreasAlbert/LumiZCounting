#!/usr/bin/env python
#-*- coding:utf-8 -*-

import string
import random
import os
import shutil
import subprocess
import sys
import multiprocessing
import datetime
config = os.path.abspath("python/ZCounting_ele_cfg.py")
tag = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
topdir = os.getcwd()

def run_single(infile):
   ID = "".join(random.sample(string.ascii_uppercase + string.digits, 8))
   print "Running over file {FILE}. ID is {ID}.".format(FILE=infile,ID=ID)

   outdir = os.path.join(topdir,"output/{TAG}/{ID}".format(TAG=tag, ID=ID))
   if(not os.path.exists(outdir)):
      os.makedirs(outdir)

   os.chdir(outdir)
   cmd = ["cmsRun",config,"inputFiles={INFILE}".format(INFILE=infile)]
   #~ print " ".join(cmd)
   with open("log.txt","w") as f:
      p = subprocess.Popen(cmd,stdout=f,stderr=f)
   p.communicate()
   os.chdir(topdir)


def read_files():
   with open("files.txt","r") as f:
      lines = [x.replace("\n","") for x in f.readlines()]
   return lines

def main():

   files = read_files()
   #~ run_single(files[0])
   print "Running over {NFILE} files. Tag is {TAG}.".format(NFILE=len(files),TAG=tag)
   pool = multiprocessing.Pool(60)
   try:
      res = pool.map_async(run_single,files)
      pool.close()
      pool.join()
   except KeyboardInterrupt:
      pool.terminate()
      pool.join()
   res.get()

if __name__ == '__main__':
   main()
