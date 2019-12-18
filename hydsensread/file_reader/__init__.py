#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-09$'
__description__ = " "
__version__ = '1.0'

from hydsensread.file_reader.abstract_file_reader import (
    AbstractFileReader, GeochemistryFileReader, TimeSeriesFileReader,
    TimeSeriesGeochemistryFileReader)
from .compagny_file_reader import (
    SolinstFileReader, DATCampbellCRFileReader, XLSHannaFileReader,
    XSLMaxxamFileReader)
try:
    from .web_page_reader import (GNBWaterQualityStation,
                                  GNBCoreSamplesNTSMapSearchWebScrapper)
except:
    pass
