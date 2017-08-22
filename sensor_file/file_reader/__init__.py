#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-09$'
__description__ = " "
__version__ = '1.0'

from sensor_file.file_reader.web_page_reader.gnb_water_quality_web_file_reader import GNB_WaterQualityStation
from sensor_file.file_reader.abstract_file_reader import AbstractFileReader, GeochemistryFileReader, TimeSeriesFileReader, TimeSeriesGeochemistryFileReader
from sensor_file.file_reader.compagny_file_reader.solinst_file_reader import SolinstFileReader
from sensor_file.file_reader.compagny_file_reader.campbell_cr_file_reader import CampbellCRFileReader
from sensor_file.file_reader.compagny_file_reader.hanna_file_reader import CSVHannaFileReader
from sensor_file.file_reader.compagny_file_reader.maxxam_file_reader import XSLMaxxamFileReader
