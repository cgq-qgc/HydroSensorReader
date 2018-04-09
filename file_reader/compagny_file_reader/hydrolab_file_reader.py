#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'X-Malet'
__date__ = '2018-04-08'
__description__ = " "
__version__ = '1.0'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from file_reader.abstract_file_reader import TimeSeriesFileReader, date_list

DATA_HEADER = 'data_header'
PROBE_ID = 'probe_id'
LOG_FILE_NAME = 'Log File Name'
SETUP_DATE = 'Setup Date (YYYY-MM-DD)'
SETUP_TIME = 'Setup Time (HH:MM:SS)'

_START_DATA_WO_DATES = 2

class TXTHydrolabFileReader(TimeSeriesFileReader):

    def __init__(self, file_name: str = None, header_length: int = 11):
        super().__init__(file_name, header_length, encoding='cp1252')
        self.data_header_index = 0

    @property
    def data_as_list(self) -> list:
        datas = self.file_content[self.data_header_index + 3:]
        data_liste = [i.split(',') for i in datas if len(i.split(',')) > 1]
        return data_liste

    @property
    def data_header(self) -> list:
        return self.header_content[DATA_HEADER]

    @data_header.setter
    def data_header(self, value: list):
        self.header_content[DATA_HEADER] = value

    def _get_date_list(self) -> date_list:
        dates = []
        for i in self.data_as_list:
            try:
                dates.append(pd.Timestamp("{} {}".format(i[0], i[1])))
            except IndexError:
                pass

        return dates

    def read_file(self):
        self._set_data_header_index()
        self._date_list = self._get_date_list()
        super(TXTHydrolabFileReader, self).read_file()

    def _read_file_header(self):
        for row in self.file_reader.get_file_header:
            try:
                row = row.replace('"', '').split(' : ')
                self.header_content[row[0]] = row[1]
            except IndexError as i:
                if 'hydrolab ms' in row[0].lower():
                    row = row[0].split(" ")
                    self.header_content[PROBE_ID] = row[2]
        self._set_site_info()

    def _set_site_info(self):
        self._set_site_name()
        self._set_site_visite_date()
        self._set_site_probe_id()

    def _set_site_probe_id(self):
        self.sites.instrument_serial_number = self.header_content[PROBE_ID]

    def _set_site_name(self, ):
        self.sites.site_name = self.header_content[LOG_FILE_NAME]

    def _set_site_visite_date(self):

        self.sites.visit_date = pd.Timestamp("{} {}".format(
            self.header_content[SETUP_DATE],
            self.header_content[SETUP_TIME]))

    def _set_data_header_index(self):
        for i in self.file_content:
            row = i.split(',')
            if row[0].lower() == '"date"':
                break
            else:
                self.data_header_index += 1

    def _read_file_data_header(self):
        data_head = self.file_content[self.data_header_index].replace('"', '').split(',')
        data_unit = self.file_content[self.data_header_index + 1].replace('"', '').split(',')
        data_header = zip(data_head, data_unit)
        self.data_header = ["{} ({})".format(i, j) for i, j in data_header if i != '']

    def _read_file_data(self):
        datas = []
        # iterate through row
        for row in self.data_as_list:
            try:
                row_content = []
                # iterate through values
                for val in [i.replace('"','') for i in row[_START_DATA_WO_DATES:]]:
                    if val != '':
                        if val not in ['#','NAN']:
                            row_content.append(float(val))
                        else:
                            row_content.append(np.nan)
                datas.append(row_content[:len(self.data_header[_START_DATA_WO_DATES:])])
            except:
                pass
        self._site_of_interest.records = pd.DataFrame(data=datas,
                                                      index=self._date_list,
                                                      columns=self.data_header[_START_DATA_WO_DATES:])
        print(self.records.dtypes)

    def plot(self, *args, **kwargs):
        fig, main_axis = plt.subplots(figsize=(20, 10))

        temperature_text = 'Temp (°C)'
        self._add_first_axis(main_axis, temperature_text)


        TDG_PSI = 'TDG (psia)'
        tdg_axe = self._add_axe_to_plot(main_axis, TDG_PSI, 'red')
        tdg_axe.grid(True)
        outward = 50
        i_batt = 'IBatt (Volts)'
        self._add_axe_to_plot(main_axis, i_batt, 'green', outward=outward)
        self._set_date_time_plot_format(main_axis)

        fig.legend(loc='upper left')


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
    pprint.pprint(hydro_file.file_reader.get_file_header, width=250)

    print(hydro_file.records.head())
    print(hydro_file.records.describe())
    hydro_file.plot()
    plt.show(block=True)
