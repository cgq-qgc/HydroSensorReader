# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © HydroSensorReader Project Contributors
# https://github.com/cgq-qgc/HydroSensorReader
#
# This file is part of HydroSensorReader.
# Licensed under the terms of the MIT License.
# -----------------------------------------------------------------------------

from .file_reader import (
    SolinstFileReader, DATCampbellCRFileReader,  XLSHannaFileReader,
    XSLMaxxamFileReader)
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBCoreSamplesDataFactory
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBCoreSamplesListWebScrapper
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBCoreSamplesNTSMapSearchWebScrapper
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBOilAndGasNTSMapSearchWebScrapper
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBOilAndGasWellsListWebScrapper
from .file_reader.web_page_reader.gnb_water_quality_web_file_reader import GNBWaterQualityStation


version_info = (1, 7, 6)
__version__ = '.'.join(map(str, version_info))
__date__ = '18/01/2022'
__project_url__ = "https://github.com/cgq-qgc/HydroSensorReader"
__author__ = 'Xavier Malet'
