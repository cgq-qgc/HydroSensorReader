#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'X-Malet'
__date__ = '2018-04-08'
__description__ = " "
__version__ = '1.0'

import datetime
import re

import matplotlib.pyplot as plt
import pandas as pd

from file_reader.abstract_file_reader import TimeSeriesFileReader, date_list


class TXTHydrolabFileReader(TimeSeriesFileReader):

    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)

    def _get_date_list(self) -> date_list:
        return super()._get_date_list()

    def plot(self, *args, **kwargs):
        super().plot(*args, **kwargs)

    def read_file(self):
        super().read_file()

    def _read_file_header(self):
        super()._read_file_header()

    def _read_file_data_header(self):
        super()._read_file_data_header()

    def _read_file_data(self):
        super()._read_file_data()
