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
   
def run_single(infile):
   ID = "".join(random.sample(string.ascii_uppercase + string.digits, 8))
   print "Running over file {FILE}. ID is {ID}.".format(FILE=infile,ID=ID)
   
   outdir = "./output/{TAG}/{ID}".format(TAG=tag, ID=ID)
   if(not os.path.exists(outdir)):
      os.makedirs(outdir)

   os.chdir(outdir)
   cmd = ["cmsRun",config,"inputFiles=\"{INFILE}\"".format(INFILE=infile)]

   with open("log.txt","w") as f:
      p = subprocess.Popen(cmd,stdout=f,stderr=f)
   p.communicate()


def read_files():
   with open("files.txt","r") as f:
      lines = [x.replace("\n","") for x in f.readlines()]
   return lines

def main():
   files = read_files()
   files = files[:8]
   
   print "Running over {NFILE} files. Tag is {TAG}.".format(NFILE=len(files),TAG=tag)
   pool = multiprocessing.Pool(4)
   try:
      res = pool.map_async(run_single,files)
      pool.close()
   except KeyboardInterrupt:
      pool.terminate()
   pool.join()
   print res.get()

if __name__ == '__main__':
   main()
