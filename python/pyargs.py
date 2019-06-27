#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate argument parse session for python command

parser = argparse.ArgumentParser(description="long description.")
parser.add_argument("-b", "--base", type=float)
parser.add_argument("-g", "--goal", type=float)
parser.add_argument("-c", "--change", type=float)
args = parser.parse_args()

"""


def add_args(name):
  "fflag for boolean, s:string for string, n/number for int"

  if len(name) <= 2:
    return "parser.add_argument('-{short_name}')".format(short_name=name[0])

  default = name[name.find('=') + 1:] if name.find('=') >= 0 else None

  if name[1] == '/':  # integer
    short_name = name[0]
    full_name = name[2:name.find('=')] if default is not None else name[2:]
    detail = "type=int{default}".format(
        default=", default=" + default if default is not None else ', default=0')
  elif name[1] == ':':  # string
    short_name = name[0]
    full_name = name[2:name.find('=')] if default is not None else name[2:]
    detail = "type=str{default}".format(
        default=", default='" + default + "'" if default is not None else '')
  else:
    short_name = name[0]
    full_name = name[1:name.find('=')] if default is not None else name[1:]
    detail = "action='store_true'"

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
  indent = '  ' * args.indent_level
  return "\n".join(map(lambda x: indent + x, add_parser(args)))


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
