#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-09$'
__description__ = " "
__version__ = '1.0'

from file_reader.abstract_file_reader import AbstractFileReader, GeochemistryFileReader, TimeSeriesFileReader, \
    TimeSeriesGeochemistryFileReader
from .compagny_file_reader import SolinstFileReader, DATCampbellCRFileReader, XLSHannaFileReader, XSLMaxxamFileReader
from .web_page_reader import GNB_WaterQualityStation
