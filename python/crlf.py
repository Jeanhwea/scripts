#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import tempfile
import os


class CrlfCLI:

  LF = b'\n'
  CRLF = b'\r\n'
  NULL = b'\0'

  def __init__(self, args):
    self.force = args.force
    self.to = args.to
    self.folders = args.folders
    self.filelist = []

  def mktemp(self, data):
    tf = tempfile.NamedTemporaryFile(mode='wb', suffix='txt', delete=False)
    tf.write(data)
    tf.close()
    return tf.name

  def readdata(self, filename):
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data

  def writedata(self, filename, data):
    f = open(filename, 'wb')
    f.write(data)
    f.close()

  def tounix(self, filename):
    data = self.readdata(filename)
    if self.NULL in data:
      return
    newdata = data.replace(self.CRLF, self.LF)
    notunix = (newdata != data)
    if notunix:
      print(filename)
      if self.force:
        self.writedata(filename, newdata)

  def towindows(self, filename):
    data = self.readdata(filename)
    if self.NULL in data:
      return
    tempdata = data.replace(self.CRLF, self.NULL)
    notwindows = (tempdata.find(self.LF) >= 0)
    if notwindows:
      print(filename)
      newdata = data.replace(self.CRLF, self.LF).replace(self.LF, self.CRLF)
      if self.force:
        self.writedata(filename, newdata)

  def apply(self):
    if not self.force:
      print("Dry run, apply changes by add '-f' option!")
    for folder in self.folders:
      for root, dirs, files in os.walk(folder):
        for filename in files:
          filepath = os.path.join(root, filename)
          if self.to == "windows":
            self.towindows(filepath)
          else:
            self.tounix(filepath)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description="crlf line ending in a list of folders"
  )
  parser.add_argument(
      "-f", "--force", action="store_true",
      help="force to replace files, otherwise just dry run!"
  )
  parser.add_argument(
      "-t", "--to", type=str, choices=["unix", "windows"],
      help="change line ending to unix or windows style, default unix!"
  )
  parser.add_argument("folders", nargs='+', help="list of folders")
  args = parser.parse_args()

  cli = CrlfCLI(args)
  cli.apply()
