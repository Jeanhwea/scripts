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
  if name is None:
    return "parser.add_argument('rest', nargs='+')"

  if len(name) <= 2:
    return "parser.add_argument('-{short_name}')".format(short_name=name[0])
  elif len(name) > 2:
    detail = "action='store_true'"
    short_name = name[0]
    full_name = name[1:]
    if name[1] == '/':
      detail = "type=int, default=0"
      full_name = name[2:]
    elif name[1] == ':':
      detail = "type=str"
      full_name = name[2:]
    return "parser.add_argument('-{short_name}', '--{full_name}', {detail})".format(
        short_name=short_name, full_name=full_name, detail=detail
    )


def add_parser(args):
  "build parser lines"
  lines = []
  lines.append("import argparse")
  lines.append("parser = argparse.ArgumentParser(description='{desc}')".format(desc=args.description))
  for name in args.rest:
    lines.append(add_args(name))
  lines.append(add_args(None))
  lines.append("args = parser.parse_args()")
  return lines


def gen_output(args):
  indent = '  ' * args.indent_level
  lines = map(lambda x: indent + x, add_parser(args))
  return "\n".join(lines)


if __name__ == '__main__':
  # codetta: start
  # python pyargs.py -i 1 \
  #   -d 'gen argument parser for python' \
  #   i/indent-level d:description
  # Codetta: output
  import argparse
  parser = argparse.ArgumentParser(description='gen argument parser for python')
  parser.add_argument('-i', '--indent-level', type=int, default=0)
  parser.add_argument('-d', '--description', type=str)
  parser.add_argument('rest', nargs='+')
  args = parser.parse_args()
  # codetta: end

  out = gen_output(args)
  print(out)
