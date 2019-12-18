# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © HydroSensorReader Project Contributors
# https://github.com/cgq-qgc/HydroSensorReader
#
# This file is part of HydroSensorReader.
# Licensed under the terms of the MIT License.
# -----------------------------------------------------------------------------

from .file_reader.compagny_file_reader.solinst_file_reader import (
    read_solinst_file)
from .file_reader import (
    DATCampbellCRFileReader,  XLSHannaFileReader,
    XSLMaxxamFileReader)
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBCoreSamplesDataFactory
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBCoreSamplesListWebScrapper
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBCoreSamplesNTSMapSearchWebScrapper
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBOilAndGasNTSMapSearchWebScrapper
from .file_reader.web_page_reader.gnb_core_samples_web_scraper import GNBOilAndGasWellsListWebScrapper
from .file_reader.web_page_reader.gnb_water_quality_web_file_reader import GNBWaterQualityStation
