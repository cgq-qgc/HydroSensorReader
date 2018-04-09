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

VALUES_START = 4
class DATCampbellCRFileReader(TimeSeriesFileReader):
    def __init__(self, file_path: str = None, header_length: int = 4):
        super().__init__(file_path, header_length)

    @property
    def data_header(self):
        start_row = 1
        column_name = [i.replace('"', '') for i in self.file_content[start_row].split(',')]
        column_unit = [i.replace('"', '') for i in self.file_content[start_row + 1].split(',')]
        column_agg = zip(column_name, column_unit)
        header_col_def = ['{} ({})'.format(i, j) for i, j in column_agg]
        return header_col_def

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        print(self.data_header)
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


if __name__ == '__main__':
    import os
    import pprint

    path = os.getcwd()
    while os.path.split(path)[1] != "scientific_file_reader":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')
    file_name = 'cr_file_example.dat'
    file = os.path.join(file_loc, file_name)
    print(file)

    campbell_file = DATCampbellCRFileReader(file)
    campbell_file.read_file()
    print(campbell_file.sites)
    pprint.pprint(campbell_file.file_reader.get_file_header, width=250)

    # print(campbell_file.records.head())
    # print(campbell_file.records.describe())
    # campbell_file.plot()
    # plt.show(block=True)
