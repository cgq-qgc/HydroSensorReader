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

    def __init__(self, file_name: str = None, header_length: int = 11):
        super().__init__(file_name, header_length)
        self.data_header_index = 0

    def _get_date_list(self) -> date_list:
        for i in self.file_content[15:]:
            print(i)
        return super()._get_date_list()

    def plot(self, *args, **kwargs):
        super().plot(*args, **kwargs)

    def read_file(self):
        self._get_date_list()
        super().read_file()

    def _read_file_header(self):
        for row in self.file_reader.get_file_header:
            try:
                row = row.replace('"', '').split(' : ')
                self.header_content[row[0]] = row[1]
            except IndexError as i:
                if 'hydrolab ms' in row[0].lower():
                    row = row[0].split(" ")
                    self.header_content['probe_id'] = row[2]
        self._set_site_info()

    def _set_site_info(self):
        self._set_site_name()
        self._set_site_visite_date()
        self._set_site_probe_id()

    def _set_site_probe_id(self):
        self.sites.instrument_serial_number = self.header_content['probe_id']

    def _set_site_name(self, ):
        self.sites.site_name = self.header_content['Log File Name']

    def _set_site_visite_date(self):
        self.sites.visit_date = pd.Timestamp("{} {}".format(
            self.header_content['Setup Date (YYYY-MM-DD)'],
            self.header_content['Setup Time (HH:MM:SS)']))

    def _read_file_data_header(self):
        for i in self.file_content:
            row = i.split(',')

            if row[0].lower() == '"date"':
                break
            else:
                self.data_header_index += 1
        data_head = self.file_content[self.data_header_index].replace('"', '').split(',')
        data_unit = self.file_content[self.data_header_index + 1].replace('"', '').split(',')
        data_header = zip((data_head, data_unit))

        self.header_content['data_header'] = ["{} ({})".format(i, j)
                                              for i, j in data_header]

    def _read_file_data(self):
        self.
        self.sites.records  = pd.DataFrame()


if __name__ == '__main__':
    import os
    import pprint

    path = os.getcwd()
    while os.path.split(path)[1] != "scientific_file_reader":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')
    file_name = 'hydrolab_file.txt'
    file = os.path.join(file_loc, file_name)
    print(file)

    hydro_file = TXTHydrolabFileReader(file)
    hydro_file.read_file()
    print(hydro_file.sites)
    # pprint.pprint(hanna_file.file_reader.get_file_header, width=250)

    # print(hanna_file.records.head())
    # print()
    # hanna_file.plot(subplots=True, title=hanna_file.sites.site_name)
    # plt.show(block=True)
