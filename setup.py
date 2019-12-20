#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Installation script """

import os
import setuptools
from setuptools import setup
from hydsensread import __version__, __project_url__, __author__


this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, 'hydsensread', "file_example", '*.*')


INSTALL_REQUIRES = []
try:
    with open('requirements.txt', 'r') as f:
        for lines in f.readlines():
            INSTALL_REQUIRES.append(lines.replace('\n', ''))
except:
    INSTALL_REQUIRES = [
        'beautifulsoup4>=4.6.0',
        'requests>=2.18.4',
        'openpyxl>=2.4.8',
        'xlrd>=1.1.0',
        'xlwt>=1.3.0',
        'pandas>=0.22.0',
        'matplotlib>=2.2.2',
        'numpy>=1.14.2']


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='HydroSensorReader',
      version=__version__,
      description=('Tools to read files from probes, sensors, '
                   'or anything used in hydrogeology.'),
      long_description=read('docs/README.md'),
      long_description_content_type='text/markdown',
      license='MIT',
      author=__author__,
      author_email='maletxa@gmail.com',
      url=__project_url__,
      packages=setuptools.find_packages(),
      package_data={'hydsensread': [DATA_PATH]},
      include_package_data=True,
      install_requires=INSTALL_REQUIRES,
      classifiers=["License :: OSI Approved :: MIT License",
                   "Programming Language :: Python :: 3",
                   "Operating System :: OS Independent"]
      )
