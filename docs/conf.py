#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop'
__date__ = '2018-04-16'
__description__ = " "
__version__ = '1.0'

from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}

print(source_parsers)
source_suffix = ['.rst', '.md']
