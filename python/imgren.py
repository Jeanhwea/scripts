#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hashlib
import time
import cv2 as cv


class ImageRenameCLI:

  def __init__(self, args):
    self.folders = args.rests
    self.force = args.force

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
    _, ext = os.path.splitext(filepath)
    timestr = ImageRenameCLI.fmttime(filepath)
    hashstr = ImageRenameCLI.getfilemd5(filepath)
    dimstr = ImageRenameCLI.imgshape(filepath)
    return '_'.join([timestr, hashstr, dimstr]) + ext

  @staticmethod
  def isimg(filename):
    return (not filename.startswith('.')) and \
        (os.path.splitext(filename)[1].lower() in ['.jpg', '.png'])

  def handle(self):
    for folder in self.folders:
      for root, dirs, files in os.walk(folder):
        print('Enter {path}:'.format(path=os.path.abspath(root)))
        for filename in filter(lambda f: self.isimg(f), files):
          filepath = os.path.join(root, filename)
          des = self.target(filepath)
          if self.force:
            if filename != des:
              print("  rename: {src} -> {des}".format(src=filename, des=des))
              os.rename(filepath, os.path.join(root, des))
          else:
            print("  {src} -> {des}".format(src=filename, des=des))

  def apply(self):
    self.handle()


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
