#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Tuple

__author__ = 'Laptop$'
__date__ = '2018-04-09'
__description__ = " "
__version__ = '1.0'

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from hydsensread.file_reader.abstract_file_reader import TimeSeriesFileReader, date_list, LineDefinition

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
                if val == '"NAN"':
                    row_content.append(np.nan)
                else:
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

    def _add_common_subplots(self) -> List[LineDefinition]:
        outward = 0
        out_linedef = []
        params_list = [LineDefinition('TDGP1_Avg (mmHg)', 'darkorange', '-'),
                       LineDefinition('Pression_bridge (psi)', 'red', make_grid=True),
                       LineDefinition('Pression_bridge_Avg (psi)', 'black', '--', linewidth=0.7),
                       LineDefinition('CH4 (%)', 'orange', '-', ),
                       LineDefinition('CH4_Avg (%)', 'brown', '--'),
                       LineDefinition('Ptot (mbar)', 'blue', '-.', linewidth=0.7)]

        for i in params_list:
            if i.param in self.records.dtypes.index:
                i.outward = outward
                out_linedef.append(i)
                outward += 50
        return out_linedef

    def _add_mean_batt_voltage(self, all_axis: List[plt.Axes]) -> List[plt.Axes]:
        bat_mean_line_def = LineDefinition('Bat_Volt_mean (volt)')
        bat_mean_axe = self._add_first_axis(all_axis[0], bat_mean_line_def)
        all_axis.append(bat_mean_axe)
        all_axis[0].set_ylim(0, 20)
        all_axis[0].set_ylabel('Bat_Volt (volt)', color='black')
        return all_axis

    def _define_axis_limite_for_pressure_and_ch4(self, all_axis: List[plt.Axes]) -> List[plt.Axes]:
        for ax in all_axis:
            for lines in ax.lines:
                if lines._label in ['Pression_bridge (psi)', 'Pression_bridge_Avg (psi)']:
                    ax.set_ylim(self.records['Pression_bridge (psi)'].min() - 15,
                                self.records['Pression_bridge (psi)'].max() + 10)
                if lines._label in ['CH4 (%)', 'CH4_Avg (%)']:
                    ax.set_ylim(0, 105)
        return all_axis

    def plot(self, main_axis_def: LineDefinition = None, other_axis: List[LineDefinition] = None,
             legend_loc='upper left', *args, **kwargs) -> \
            Tuple[
                plt.Figure, List[plt.Axes]]:
        self.records['Bat_Volt_mean (volt)'] = self.records['Bat_Volt (volt)'].resample('D').mean()
        self.records['Bat_Volt_mean (volt)'] = self.records['Bat_Volt_mean (volt)'].interpolate()
        if main_axis_def is None:
            main_axis_def = LineDefinition('Bat_Volt (volt)', 'green', linewidth=0.5)
        if other_axis is None:
            other_axis = self._add_common_subplots()

        fig, all_axis = super().plot(main_axis_def, other_axis, legend_loc, *args, **kwargs)
        all_axis = self._add_mean_batt_voltage(all_axis)
        all_axis = self._define_axis_limite_for_pressure_and_ch4(all_axis)

        return fig, all_axis


if __name__ == '__main__':
    import os

    path = os.getcwd()
    while os.path.split(path)[1] != "hydsensread":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')
    file_name = "PO-03_F2_XM20170222.dat"
    file = os.path.join(file_loc, file_name)
    print(file)

    campbell_file = DATCampbellCRFileReader(file)
    campbell_file.read_file()
    print(campbell_file.sites)

    # print(campbell_file.records.head())
    print(campbell_file.records.describe())
    fig, ax = campbell_file.plot(legend_loc='lower right')

    plt.show(block=True)
