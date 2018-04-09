#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyparsing import col

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
COL_HEADER = 'col_header'
class DATCampbellCRFileReader(TimeSeriesFileReader):
    def __init__(self, file_path: str = None, header_length: int = 4):
        super().__init__(file_path, header_length)
        self.datas = [i.split(',') for i in self.file_content[VALUES_START:]]

    @property
    def data_header(self):
        return self.header_content[COL_HEADER]

    def read_file(self):
        self._date_list = self._get_date_list()
        super().read_file()

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        header_content = [i.replace('"', '') for i in self.file_content[0].split(',')]
        print(header_content)
        self.sites.site_name = header_content[-1]
        self.sites.instrument_serial_number = header_content[3]


    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        datas = []
        for row in self.datas:
            row_content = []
            for val in row[2:]:
                row_content.append(float(val))
            datas.append(row_content)
        self.records = pd.DataFrame(data=datas,
                                    index=self._date_list,
                                    columns=self.data_header[2:])
        self.remove_duplicates()

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        start_row = 1
        column_name = [i.replace('"', '') for i in self.file_content[start_row].split(',')]
        column_unit = [i.replace('"', '') for i in self.file_content[start_row + 1].split(',')]
        column_agg = zip(column_name, column_unit)
        header_col_def = ['{} ({})'.format(i, j) for i, j in column_agg]
        self.header_content[COL_HEADER] = header_col_def

    def _get_date_list(self) -> date_list:
        dates = []
        for i in self.datas:
            dates.append(pd.Timestamp(i[0].replace('"','')))
        self.sites.visit_date = dates[-1]
        return dates



    def plot(self, *args, **kwargs):
        fig, axe = plt.subplots(figsize=(20, 10))

        bat_axe = self._add_first_axis(axe,'Bat_Volt (volt)',color='green')
        bat_axe.set_ylim(0,15)
        outward = 50
        self._add_axe_to_plot(axe,'TDGP1_Avg (mmHg)','orange','-',outward*2)

        press_axe = self._add_axe_to_plot(axe,'Pression_bridge (psi)','red')
        new_axis = press_axe.twinx()
        new_axis.plot(self.records['Pression_bridge_Avg (psi)'], color='black', linestyle='--')
        new_axis.set_axis_off()
        press_axe.set_ylabel('Pression (meas.=red; avg.=black) (psi)', color='black',labelpad=35)
        self._set_date_time_plot_format(axe)
        fig.legend(loc='upper left')







if __name__ == '__main__':
    import os
    import pprint

    path = os.getcwd()
    while os.path.split(path)[1] != "scientific_file_reader":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')
    file_name = "F-4_F4_XM20160620.dat"
    file = os.path.join(file_loc, file_name)
    print(file)

    campbell_file = DATCampbellCRFileReader(file)
    campbell_file.read_file()
    print(campbell_file.sites)

    # print(campbell_file.records.head())
    # print(campbell_file.records.describe())
    campbell_file.plot()
    plt.show(block=True)
