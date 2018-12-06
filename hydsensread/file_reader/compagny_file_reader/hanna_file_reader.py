#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Tuple

__author__ = 'Laptop$'
__date__ = '2017-07-16'
__description__ = " "
__version__ = '1.0'
import datetime
import re

import matplotlib.pyplot as plt
import pandas as pd

from hydsensread.file_reader.abstract_file_reader import TimeSeriesFileReader, date_list, LineDefinition


class XLSHannaFileReader(TimeSeriesFileReader):
    def __init__(self, file_path: str = None, header_length: int = 10,wait_read:bool = False):
        super().__init__(file_path, header_length,wait_read=wait_read)

    def read_file(self):
        self._date_list = self._get_date_list()
        super(XLSHannaFileReader, self).read_file()

    @property
    def header_info(self):
        return self.file_content[' Lot Info ']

    @property
    def data_sheet(self):
        return self.file_content[' Log data - 1']

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        for row in self.header_info:
            if row[0] is None or row[0] in ['GENERAL INFORMATION', 'LOT INFORMATION', 'SETTINGS']:
                pass
            else:
                key = re.sub('^ *', '', row[0])
                self.header_content[key] = row[1]

    def _get_date_list(self) -> date_list:
        date_list = [d[0] for d in self.data_sheet[1:]]
        time_list = [datetime.time(d[1].hour, d[1].minute, d[1].second) for d in self.data_sheet[1:]]
        date_time = [datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
                     for d, t in zip(date_list, time_list)]
        return date_time

    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        values = [val[2:] for val in self.data_sheet[1:]]
        self._site_of_interest.records = pd.DataFrame(data=values, columns=self.data_sheet[0][2:],
                                                      index=self._date_list)

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        self.sites.site_name = self.header_content['Lot Name']
        self.sites.instrument_serial_number = self.header_content['Instrument Serial No.']
        self.sites.visit_date = self.header_content['Started Date and Time']

    def plot(self, *args, **kwargs) -> Tuple[
        plt.Figure, List[plt.Axes]]:
        main_temperature_line_def = LineDefinition('Temp.[°C]')
        ph_line_def = LineDefinition('pH ', 'black', '--')
        outward = 50
        do_line_Def = LineDefinition('D.O.[%]', 'red', outward=outward)
        orp_line_def = LineDefinition('ORP[mV]', 'green', outward=2 * outward)
        other_axis = [ph_line_def, do_line_Def, orp_line_def]

        fig, axes = super().plot(main_temperature_line_def, other_axis, *args, **kwargs)
        return fig, axes





if __name__ == '__main__':
    import os
    import pprint

    path = os.getcwd()
    while os.path.split(path)[1] != "hydsensread":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')
    file_name = 'LOG006_0621113447.xls'
    file_name_2 = 'LOG001_1011105528.xls'
    file = os.path.join(file_loc, file_name)
    file_2 = os.path.join(file_loc, file_name_2)
    print(file)

    hanna_file = XLSHannaFileReader(file)
    hanna_file.read_file()
    pprint.pprint(hanna_file.header_content, width=250)

    hanna_file_2 = XLSHannaFileReader(file_2)
    hanna_file_2.read_file()
    hanna_file_2.plot()

    print(hanna_file.records.head())
    print("*" * 15)
    print(hanna_file_2.records.head())

    hanna_file.plot(subplots=True, title=hanna_file.sites.site_name, x_compat=True)
    plt.show(block=True)
