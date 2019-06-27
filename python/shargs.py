#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''

import re


while_tmpl = '''{decalre_stmts}while getopts "{optstring}" opt; do
$>case "${{opt}}" in
{case_stmts}$>$>*)
$>$>$>echo '{help_str}'
$>$>$>exit
$>$>$>;;
$>esac
done
shift $((OPTIND-1)){rests}'''

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
      full_name=res[1].replace('-', '_'),
      default=('off' if len(res[0]) < 2 else "''") if res[2] is None else res[2])


def gen_while_str(decalre_str, optstring, case_str, help_str, args):
  return while_tmpl.format(
      decalre_stmts=decalre_str,
      optstring=optstring,
      case_stmts=case_str,
      help_str=help_str,
      rests='\nrests=$*' if args.rest else '')


def gen_case_str(res):
  return case_tmpl.format(
      short_name=res[0][0],
      full_name=res[1].replace('-', '_'),
      value='on' if len(res[0]) < 2 else '${OPTARG}')


def gen_output(args):
  indent = '  '
  declare_str = ''
  optstring = ':' if args.no_error else ''
  help_list = []
  case_str = ''
  for optstr in args.rests:
    res = parse_optstr(optstr)
    if res:
      declare_str += gen_declare(res)
      optstring += res[0]
      help_list.append(
          "[-{short_name} {full_name}]".format(
              short_name=res[0][0], full_name=res[1].upper().replace('-', '_')))
      case_str += gen_case_str(res)
  help_str = 'do NOT need argument!' if len(help_list) <= 0 else 'options: ' + ' '.join(help_list)
  lines = gen_while_str(declare_str, optstring, case_str, help_str, args).replace("$>", indent).split('\n')
  return '\n'.join(map(lambda line: indent * args.indent_level + line if len(line) > 0 else line, lines))


if __name__ == '__main__':
  # codetta: start
  # python python/pyargs.py -i 1 -d 'genenrate argument parser for bash' i/indent-level=0 nno-error rrest
  # codetta: output
  import argparse
  parser = argparse.ArgumentParser(description='genenrate argument parser for bash')
  parser.add_argument('-i', '--indent-level', type=int, default=0)
  parser.add_argument('-n', '--no-error', action='store_true')
  parser.add_argument('-r', '--rest', action='store_true')
  parser.add_argument('rests', nargs='*')
  args = parser.parse_args()
  # codetta: end

  out = gen_output(args)
  print(out)
