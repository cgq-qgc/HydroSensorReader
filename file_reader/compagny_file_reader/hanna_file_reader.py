#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = " "
__version__ = '1.0'
import datetime

import pandas as pd

from file_reader.abstract_file_reader import TimeSeriesFileReader, date_list


class XLSHannaFileReader(TimeSeriesFileReader):
    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)

    def read_file(self):
        self._date_list = self._get_date_list()
        self._read_file_data()

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
        pass

    def _get_date_list(self) -> date_list:
        date_list = [d[0] for d in hanna_file.data_sheet[1:]]
        time_list = [datetime.time(d[1].hour, d[1].minute, d[1].second) for d in hanna_file.data_sheet[1:]]
        date_time = [datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
                     for d, t in zip(date_list, time_list)]
        return date_time

    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        values = [val[2:] for val in hanna_file.data_sheet[1:]]
        self._site_of_interest.records = pd.DataFrame(data=values, columns=hanna_file.data_sheet[0][2:],
                                                      index=self._get_date_list())

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        pass



if __name__ == '__main__':
    import os
    import pprint
    import matplotlib.pyplot as plt
    path = os.getcwd()
    while os.path.split(path)[1] != "scientific_file_reader":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')
    file_name = 'LOG006_0621113447.xls'
    file = os.path.join(file_loc, file_name)
    print(file)

    hanna_file = XLSHannaFileReader(file)
    date_list = [d[0] for d in hanna_file.data_sheet[1:]]
    time_list = [datetime.time(d[1].hour, d[1].minute, d[1].second) for d in hanna_file.data_sheet[1:]]
    date_time = [datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
                 for d, t in zip(date_list, time_list)]
    values = [val[2:] for val in hanna_file.data_sheet[1:]]
    hanna_file.read_file()
    print(len(values))
    print(len(date_time))
    pprint.pprint(date_time[:5], width=350)
    pprint.pprint(hanna_file.data_sheet[0][2:], width=250)
    df = pd.DataFrame(data=values, columns=hanna_file.data_sheet[0][2:], index=date_time)
    print(df.head())
    print()
    hanna_file.records.plot(subplots=True, title=file_name)
    plt.show(block=True)
