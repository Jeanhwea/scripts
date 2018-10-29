#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import hashlib
import argparse

class FindDupCLI:

  def __init__(self, args):
    self.folders = args.folders
    self.minisize = args.minisize
    self.maxnum = args.maxnum
    self.duplist = []


  @staticmethod
  def getfilesize(filepath):
    return os.stat(filepath).st_size


  @staticmethod
  def getfilemd5(filepath):
    obj = hashlib.md5()
    with open(filepath,'rb') as f:
      while True:
        bits = f.read(8096)
        if not bits: break
        obj.update(bits)
    return obj.hexdigest()


  def getduplicates(self):
    sizedict = {}

    # scan file size first
    for folder in self.folders:
      for root, dirs, files in os.walk(folder):
        for filename in files:
          filepath = os.path.join(root, filename)
          filesize = self.getfilesize(filepath)
          if filesize <= self.minisize: continue
          sizedict.setdefault(filesize, []).append(filepath)

    # check file md5 if the file size is same
    md5dict = {}
    for files in filter(lambda files: len(files) > 1, sizedict.values()):
      for filepath in files:
        md5 = self.getfilemd5(filepath)
        md5dict.setdefault(md5, []).append(filepath)

    # duplist if both file szie and md5 are same
    self.duplist = list(filter(lambda files: len(files) > 1, md5dict.values()))


  def display(self):
    for i in range(len(self.duplist)):
      if self.maxnum > 0 and i > self.maxnum: break
      print('[{i}/{n}] ===> {size}'.format(
        i=i,
        n=len(self.duplist),
        size=self.getfilesize(self.duplist[i][0])
      ))
      for j in range(len(self.duplist[i])):
        print('{j}. {name}'.format(
          j=j, name=self.duplist[i][j]
        ))


  def apply(self):
    self.getduplicates()
    self.display()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description="find duplicated files in a list of folders"
  )
  parser.add_argument(
    "-m", "--minisize", type=int, default=0,
    help="the minimum size of searched file"
  )
  parser.add_argument(
    "-n", "--maxnum", type=int, default=0,
    help="the maximum item for display"
  )
  parser.add_argument("folders", nargs='+', help="list of folders")
  args = parser.parse_args()

  cli = FindDupCLI(args)
  cli.apply()
