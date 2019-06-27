#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


while_tmpl = '''{decalre_stmts}
while getopts "{optstring}" opt; do
$>case "${{opt}}" in
{case_stmts}$>$>*)
$>$>$>echo 'default'
$>$>$>;;
$>esac
done
shift $((OPTIND-1))'''

case_tmpl = '''$>$>{short_name})
$>$>$>{full_name}={value}
$>$>$>;;
'''


def parse_optstr(optstr):
  regexp = re.match(r'^([A-Za-z]{1}|[A-Za-z]{1}:)([_A-Za-z][_\-0-9A-Za-z]*)(|=([^=]*))$', optstr)
  if regexp:
    return regexp.group(1), regexp.group(2), regexp.group(4)
  else:
    return None


def gen_declare(res):
  return "{full_name}={default}\n".format(
      full_name=res[1],
      default=('off' if len(res[0]) < 2 else "''") if res[2] is None else res[2])


def gen_while_str(decalre_str, optstring, case_str):
  return while_tmpl.format(decalre_stmts=decalre_str, optstring=optstring, case_stmts=case_str)


def gen_case_str(res):
  return case_tmpl.format(
      short_name=res[0][0],
      full_name=res[1],
      value='on' if len(res[0]) < 2 else '${OPTARG}')


def gen_output(args):
  indent = '  ' * args.indent_level
  declare_str = ''
  case_str = ''
  optstring = ':' if args.no_error else ''
  for optstr in args.rests:
    res = parse_optstr(optstr)
    if res:
      declare_str += gen_declare(res)
      optstring += res[0]
      case_str += gen_case_str(res)
  lines = gen_while_str(declare_str, optstring, case_str).replace("$>", '  ').split('\n')
  return '\n'.join(map(lambda line: indent + line if len(line) > 0 else line, lines))


if __name__ == '__main__':
  # codetta: start
  # python python/pyargs.py -i 1 -d 'genenrate argument parser for bash' i/indent-level=0 nno-error
  # codetta: output
  import argparse
  parser = argparse.ArgumentParser(description='genenrate argument parser for bash')
  parser.add_argument('-i', '--indent-level', type=int, default=0)
  parser.add_argument('-n', '--no-error', action='store_true')
  parser.add_argument('rests', nargs='*')
  args = parser.parse_args()
  # codetta: end

  out = gen_output(args)
  print(out)
