#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate argument parse session for python command

parser = argparse.ArgumentParser(description="long description.")
parser.add_argument("-b", "--base", type=float)
parser.add_argument("-g", "--goal", type=float)
parser.add_argument("-c", "--change", type=float)
args = parser.parse_args()

"""
import re


def parse_optstr(optstr):
  regexp = re.match(r'^([A-Za-z]{1}|[A-Za-z]{1}:|[A-Za-z]{1}/)([_A-Za-z][_\-0-9A-Za-z]*)(|=([^=]*))$', optstr)
  if regexp:
    return regexp.group(1), regexp.group(2), regexp.group(4)
  else:
    return None


def add_args(name):
  "fflag for boolean, s:string for string, n/number for int"
  res = parse_optstr(name)
  if res:
    short_name = res[0][0]
    full_name = res[1]
    if len(res[0]) < 2:
      detail = "action='store_true'"
    elif res[0][1] == '/':
      detail = "type=int{default}".format(
          default=", default=" + res[2] if res[2] is not None else ', default=0')
    elif res[0][1] == ':':
      detail = "type=str{default}".format(
          default=", default='" + res[2] + "'" if res[2] is not None else '')
    return "parser.add_argument('-{short_name}', '--{full_name}', {detail})".format(
        short_name=short_name, full_name=full_name, detail=detail)


def add_parser(args):
  "build parser lines"
  lines = []
  lines.append("import argparse")
  if args.description is not None:
    lines.append("parser = argparse.ArgumentParser(description='{desc}')".format(desc=args.description))
  else:
    lines.append("parser = argparse.ArgumentParser()")
  for name in args.rests:
    lines.append(add_args(name))
  if args.rest:
    lines.append("parser.add_argument('rests', nargs='+')")
  else:
    lines.append("parser.add_argument('rests', nargs='*')")
  lines.append("args = parser.parse_args()")
  return lines


def gen_output(args):
  indent = '  '
  return "\n".join(map(lambda line: indent * args.indent_level + line, add_parser(args)))


if __name__ == '__main__':
  # codetta: start
  # python python/pyargs.py -i 1 -d 'genenrate argument parser for python' i/indent-level=0 d:description rrest
  # codetta: output
  import argparse
  parser = argparse.ArgumentParser(description='genenrate argument parser for python')
  parser.add_argument('-i', '--indent-level', type=int, default=0)
  parser.add_argument('-d', '--description', type=str)
  parser.add_argument('-r', '--rest', action='store_true')
  parser.add_argument('rests', nargs='*')
  args = parser.parse_args()
  # codetta: end

  out = gen_output(args)
  print(out)
