#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
import os


class CrlfCLI:

  LF = b'\n'
  CRLF = b'\r\n'
  NULL = b'\0'

  def __init__(self, args):
    self.force = args.force
    self.to_dos = args.to_dos
    self.folders = args.rests
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

  def todos(self, filename):
    data = self.readdata(filename)
    if self.NULL in data:
      return
    tempdata = data.replace(self.CRLF, self.NULL)
    notdos = (tempdata.find(self.LF) >= 0)
    if notdos:
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
          if self.to_dos:
            self.todos(filepath)
          else:
            self.tounix(filepath)


if __name__ == '__main__':
  # codetta: start
  # python pyargs.py -r -i 1 -d 'crlf line ending in a list of folders' fforce tto-dos
  # codetta: output
  import argparse
  parser = argparse.ArgumentParser(description='crlf line ending in a list of folders')
  parser.add_argument('-f', '--force', action='store_true')
  parser.add_argument('-t', '--to-dos', action='store_true')
  args = parser.parse_args()
  # codetta: end

  cli = CrlfCLI(args)
  cli.apply()
