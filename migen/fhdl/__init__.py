#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:noexpandtab:ts=8:sw=8:si:smarttab:tw=80

import sys
import os
from migen.fhdl.verilog import convert as verilog_convert
from migen.fhdl.vhdl import convert as vhdl_convert

__all__ = ('''
	main
	convert
	'''.split())


def main():
	import argparse

	parser = argparse.ArgumentParser(
			description='Convert fhdl to HDL',
			epilog='migen - Python toolbox for building '
			'complex digital hardware\n',
			add_help=True)
	parser.add_argument('--vhdl',
		dest='convert',
		const=vhdl_convert,
		default=verilog_convert,
		action='store_const',
		help='Generate VHDL HDL (default: generate Verilog HDL)')
	parser.add_argument('infile',
		type=argparse.FileType('r'),
		help='Input file')
	parser.add_argument('--outfile',
		type=argparse.FileType('w'),
		default=sys.stdout,
		help='Output file (default: stdout)')

	globals()['_args'] = parser.parse_args()
	globals()['__name__'] = os.path.split(_args.infile.name)[-1].split('.')[0]

	exec(compile(_args.infile.read(), _args.infile.name, 'exec'),
		globals(),
		locals())

def convert(*args, **kwargs):
	'''
	Wrapper for either verilog.convert() or vhdl.convert()
	'''
	try:
		with _args.outfile as out:
			out.write(_args.convert(*args, **kwargs))
	except NameError:
		print(verilog_convert(*args, **kwargs))
