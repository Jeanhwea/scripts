#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import hashlib
import os
import sys

class RenameCLI:

  def __init__(self, args):
    self.force = args.force
    self.folders = args.folders

  @staticmethod
  def getfilemd5(filepath):
    obj = hashlib.md5()
    with open(filepath, 'rb') as f:
      while True:
        bits = f.read(8096)
        if not bits: break
        obj.update(bits)
    return obj.hexdigest()

  def movefiles(self, md5dict):
    for name, md5name in md5dict.items():
      if self.force:
        os.rename(name, md5name)
      else:
        print('{src} -> {des}'.format(src=name, des=md5name))

  def apply(self):
    for folder in self.folders:
      md5dict = {}
      for root, dirs, files in os.walk(folder):
        for filename in files:
          filepath = os.path.join(root, filename)
          md5dict[filepath] = '{name}{ext}'.format(
            name=os.path.join(root, self.getfilemd5(filepath)),
            ext=os.path.splitext(filepath)[1]
          )
      self.movefiles(md5dict)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description="rename all the files in the list of folders to their md5sum"
  )
  parser.add_argument(
    "-f", "--force", action="store_true",
    help="force to rename files, otherwise just dry run!"
  )
  parser.add_argument("folders", nargs='+', help="list of folders")
  args = parser.parse_args()

  cli = RenameCLI(args)
  cli.apply()

