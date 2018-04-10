#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Tuple

__author__ = 'Laptop$'
__date__ = '2018-04-09'
__description__ = " "
__version__ = '1.0'

import matplotlib.pyplot as plt
import pandas as pd

from file_reader.abstract_file_reader import TimeSeriesFileReader, date_list, LineDefinition

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
            dates.append(pd.Timestamp(i[0].replace('"', '')))
        self.sites.visit_date = dates[-1]
        return dates


class CR1000withTDGprobe(DATCampbellCRFileReader):

    def __init__(self, file_path: str = None, header_length: int = 4):
        super().__init__(file_path, header_length)

    def plot(self, *args, **kwargs) -> Tuple[
        plt.Figure, List[plt.Axes]]:
        self.records['Bat_Volt_mean (volt)'] = self.records['Bat_Volt (volt)'].resample('D').mean()
        self.records['Bat_Volt_mean (volt)'] = self.records['Bat_Volt_mean (volt)'].interpolate()

        bat_line_def = LineDefinition('Bat_Volt (volt)', 'green', linewidth=0.5)
        outward = 50
        tdgp_avg_line_def = LineDefinition('TDGP1_Avg (mmHg)', 'darkorange', '-', outward * 2)
        press_line_def = LineDefinition('Pression_bridge (psi)', 'red', make_grid=True)
        press_avg_line_def = LineDefinition('Pression_bridge_Avg (psi)', 'black', '--', outward, linewidth=0.7)

        lines_definition = [tdgp_avg_line_def, press_line_def, press_avg_line_def]

        fig, all_axis = super().plot(bat_line_def, lines_definition, *args, **kwargs)
        bat_mean_line_def = LineDefinition('Bat_Volt_mean (volt)')
        bat_mean_axe = self._add_first_axis(all_axis[0], bat_mean_line_def)
        all_axis.append(bat_mean_axe)
        all_axis[0].set_ylim(0, 20)
        # set limite for press_line_def
        all_axis[2].set_ylim(self.records['Pression_bridge (psi)'].min() - 15,
                             self.records['Pression_bridge (psi)'].max() + 10)
        # set limite for press_avg_line_def
        all_axis[3].set_ylim(self.records['Pression_bridge (psi)'].min() - 15,
                             self.records['Pression_bridge (psi)'].max() + 10)
        all_axis[0].set_ylabel('Bat_Volt (volt)', color='black')
        fig.legend(loc='upper left')
        return fig, all_axis


if __name__ == '__main__':
    import os

    path = os.getcwd()
    while os.path.split(path)[1] != "scientific_file_reader":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')
    file_name = "cr_file_example.dat"
    file = os.path.join(file_loc, file_name)
    print(file)

    campbell_file = CR1000withTDGprobe(file)
    campbell_file.read_file()
    print(campbell_file.sites)

    # print(campbell_file.records.head())
    # print(campbell_file.records.describe())
    campbell_file.plot()

    plt.show(block=True)
