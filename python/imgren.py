#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hashlib
import time
import cv2 as cv


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
    value = obj.hexdigest()
    return value[0:8]

  @staticmethod
  def imgshape(filepath):
    img = cv.imread(filepath)
    return '{width}x{height}'.format(width=img.shape[1], height=img.shape[0])

  @staticmethod
  def fmttime(filepath):
    timestamp = os.path.getmtime(filepath)
    return time.strftime('%Y%m%d_%H%M%S', time.localtime(timestamp))

  @staticmethod
  def target(filepath):
    return '_'.join([
        ImageRenameCLI.fmttime(filepath),
        ImageRenameCLI.getfilemd5(filepath),
        ImageRenameCLI.imgshape(filepath)])

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
