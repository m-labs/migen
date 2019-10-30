# -*- coding: utf-8 -*-
import sys
from setuptools import setup
from setuptools import find_packages

if sys.version_info[:3] < (3, 3):
    raise SystemExit("You need Python 3.3+")


requirements = []

setup(
    name="migen",
    version="0.8.dev",
    description="Python toolbox for building complex digital hardware",
    long_description=open("README.md").read(),
    author="Sebastien Bourdeauducq",
    author_email="sb@m-labs.hk",
    url="https://m-labs.hk",
    download_url="https://github.com/m-labs/migen",
    packages=find_packages(),
    install_requires=requirements,
    test_suite="migen.test",
    license="BSD",
    platforms=["Any"],
    keywords=["HDL", "ASIC", "FPGA", "hardware design"],
    classifiers=[
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7'
    ],
)
