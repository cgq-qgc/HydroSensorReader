#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2018-04-09'
__description__ = " "
__version__ = '1.0'

from file_reader.abstract_file_reader import TimeSeriesFileReader, date_list
import datetime
import re

import matplotlib.pyplot as plt
import pandas as pd

from file_reader.abstract_file_reader import TimeSeriesFileReader, date_list


class DATCampbellCRFileReader(TimeSeriesFileReader):
    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        pass

    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        pass

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        pass

    def _get_date_list(self) -> date_list:
        return super()._get_date_list()
