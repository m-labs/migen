#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: noexpandtab:tabstop=8:softtabstop=8
""" Migen's distutils distribution and installation script. """

import sys, os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README")).read()

required_version = (3, 1)
if sys.version_info < required_version:
	raise SystemExit("migen requires python {0} or greater".format(
		".".join(map(str, required_version))))

setup(
	name="migen",
	version="unknown",
	description="Python toolbox for building complex digital hardware",
	long_description=README,
	author="Sebastien Bourdeauducq",
	author_email="sebastien@milkymist.org",
	url="http://www.milkymist.org",
	download_url="https://github.com/milkymist/migen",
	packages=find_packages(here),
	license="GPL",
	platforms=["Any"],
	keywords="HDL ASIC FPGA hardware design",
	classifiers=[
		"Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
		"Environment :: Console",
		"Development Status :: Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
	],
	entry_points = {"console_scripts": [
	    "migen_fhdl_convert = migen.fhdl:main",
	    ]
	}
)
