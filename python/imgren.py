#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hashlib


class ImageRenameCLI:

  def __init__(self, args):
    self.folders = args.rests

  @staticmethod
  def getfilemd5(filepath):
    obj = hashlib.md5()
    with open(filepath, 'rb') as f:
      while True:
        bits = f.read(8096)
        if not bits:
          break
        obj.update(bits)
    return obj.hexdigest()

  def apply(self):
    print('apply...')


if __name__ == '__main__':
  # codetta: start
  # python pyargs.py -r -i 1 \
  #    -d 'rename image files in a list of folders' \
  #    fforce
  # codetta: output
  import argparse
  parser = argparse.ArgumentParser(description='rename image files in a list of folders')
  parser.add_argument('-f', '--force', action='store_true')
  parser.add_argument('rests', nargs='+')
  args = parser.parse_args()
  # codetta: end

  cli = ImageRenameCLI(args)
  cli.apply()
