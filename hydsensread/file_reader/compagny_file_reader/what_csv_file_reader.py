#!/usr/bin/env python
# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt

__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = "Permet de lire des fichiers provenant de l'interface" \
                  " WHAT : https://github.com/jnsebgosselin/what.git"
__version__ = '1.0'
import datetime
from abc import abstractmethod
from typing import Union, List, Tuple

# ---- Local imports
from hydsensread.site_and_records import (
    geographical_coordinates, StationSite, StreamFlowStation)
from hydsensread.file_reader.abstract_file_reader import (
    TimeSeriesFileReader, date_list, LineDefinition)

WHAT_METEO_FILES_HEADER_LENGTH = 10
WHAT_WATER_LEVEL_FILES_HEADER_LENGTH = 10
WHAT_STREAM_FLOW_STATION_HEADER_LENGTH = 19

station_possible = Union[StationSite, StreamFlowStation]


class AbstractWhatFileReader(TimeSeriesFileReader):
    def __init__(self, file_path: str = None, header_length: int = WHAT_METEO_FILES_HEADER_LENGTH,
                 station_type: station_possible = None):
        # if file_name is None:
        #     pass
        # else:
        super().__init__(file_path, header_length)
        self._site_of_interest = station_type
        self.read_file()

    def _read_file_header(self):
        for i, data in zip(range(self._header_length), self.file_content):
            if len(data) > 0:
                self.file_reader.get_file_header.append(data)

    @abstractmethod
    def _read_file_data(self, start_data_column: int = 0):
        """
        permet de lire les données provenant des fichiers
        :param start_data_column: offset permettant de lire uniquement les données
            - c'est à dire, sans les colonnes de date.
        :return:
        """
        for index, elt in zip(range(len(self.file_content[self._header_length][start_data_column:])),
                              self.file_content[self._header_length][start_data_column:]):
            parameter = elt.split(' (')[0]
            try:
                unit = elt.split(' (')[1].split(')')[0]
            except IndexError as i:
                print(str(i))
                print(elt)
            else:
                datas = []
                for row in self.file_content[self._header_length + 1:]:
                    datas.append(float(row[index + start_data_column]))
                self._site_of_interest.create_time_serie(parameter, unit, self._get_date_list(), datas)

    @property
    def sites(self) -> Union[StreamFlowStation, StationSite]:
        return self._site_of_interest

    @abstractmethod
    def _read_file_data_header(self):
        pass

    def _make_station_coordinates_from_file(self) -> None:
        geo_coordinates = [0, 0, 0]
        for data in self.file_reader.get_file_header:
            if len(data) == 2:
                if 'Longitude' in data[0]:
                    geo_coordinates[0] = float(data[1])
                if 'Latitude' in data[0]:
                    geo_coordinates[1] = float(data[1])
                if 'Elevation' in data[0]:
                    try:
                        geo_coordinates[2] = float(data[1])
                    except:
                        geo_coordinates[2] = data[1]
        self._site_of_interest.coordinates_x_y_z = geographical_coordinates(*geo_coordinates)

    @abstractmethod
    def _get_date_list(self) -> date_list:
        pass

    def _make_date_list(self, year_column_index: int = 0,
                        month_column_index: int = 1,
                        day_column_index: int = 2):
        if len(self._date_list) == 0:
            for row in self.file_content[self._header_length + 1:]:
                year = int(row[year_column_index].split(".")[0])
                month = int(row[month_column_index].split(".")[0])
                day = int(row[day_column_index].split(".")[0])
                self._date_list.append(datetime.datetime(year, month, day))
        return self._date_list

    def _set_station_attribute(self, attribute, what_to_search):
        for data in self.file_reader.get_file_header:
            try:
                if what_to_search in data[0]:
                    self._site_of_interest.__dict__[attribute] = data[1]
                    break
            except IndexError:
                pass

    def _make_station_id(self, what_to_search):
        self._set_station_attribute('site_name', what_to_search)

    def _make_station_other_name(self, what_to_search):
        self._set_station_attribute('other_identifier', what_to_search)


class WhatMeteorologicalDataFileReader(AbstractWhatFileReader):
    def __init__(self, file_path: str = None):
        super().__init__(file_path, WHAT_METEO_FILES_HEADER_LENGTH, StationSite())

    def _read_file_data_header(self):
        self._make_station_coordinates_from_file()
        self._make_station_id('Climate Identifier')
        self._make_station_other_name('Station Name')

    def _get_date_list(self) -> date_list:
        return self._make_date_list()

    def _read_file_data(self, start_data_column: int = 3):
        super()._read_file_data(start_data_column)


class WhatWaterLevelDataFileReader(AbstractWhatFileReader):
    def __init__(self, file_path: str = None):
        super().__init__(file_path, WHAT_WATER_LEVEL_FILES_HEADER_LENGTH, station_type=StationSite())

    def _read_file_data(self, start_data_column: int = 4):
        super()._read_file_data(start_data_column)

    def _read_file_data_header(self):
        self._make_station_coordinates_from_file()
        self._make_station_id('Well ID')
        self._make_station_other_name('Well Name')

    def _get_date_list(self) -> date_list:
        return self._make_date_list(1, 2, 3)

    def plot(self, *args, **kwargs) -> Tuple[
        plt.Figure, List[plt.Axes]]:
        water_level_line_def = LineDefinition('Water level_masl', make_grid=True)
        water_temp_line_def = LineDefinition('Water temperature_degC', 'red')
        return super().plot(water_level_line_def, [water_temp_line_def], *args, **kwargs)


class WhatStreamAndLevelDataFileReader(AbstractWhatFileReader):
    def __init__(self, file_path: str = None,
                 header_length: int = WHAT_STREAM_FLOW_STATION_HEADER_LENGTH):
        super().__init__(file_path, header_length, StreamFlowStation())

    def _read_file_data(self, start_data_column: int = 4):
        super()._read_file_data(start_data_column)

    def _read_file_data_header(self):
        # On change le type de station

        self._make_station_coordinates_from_file()
        self._make_station_id('Station ID')
        self._make_station_other_name('Station Name')
        self._set_station_attribute('site_description', 'Description')
        self._set_station_attribute('station_activity_status', 'Status')
        self._set_station_attribute('active_period', 'Active period')
        self._set_station_attribute('municipality', 'Municipality')
        self._set_station_attribute('administrative_region', 'Administrative Region')
        self._set_station_attribute('stream_name', 'Stream Name')
        self._set_station_attribute('hydrographic_region', 'Hydrographic Region')
        self._set_station_attribute('drain_area', 'Drainage Area')
        self._set_station_attribute('flow_regime', 'Flow Regime')
        self._set_station_attribute('federal_id', 'Federal ID')
        self._set_station_attribute('province', 'Province')

    def _get_date_list(self) -> date_list:
        return self._make_date_list(1, 2, 3)

    def plot(self, *args, **kwargs) -> Tuple[
        plt.Figure, List[plt.Axes]]:
        level_line_def = LineDefinition('Level_m', make_grid=True)
        flow_line_def = LineDefinition('Flow_m3/s', 'red')

        return super().plot(level_line_def, [flow_line_def], *args, **kwargs)


if __name__ == '__main__':
    import os
    import matplotlib.pyplot as plt

    path = os.getcwd()
    #while os.path.split(path)[1] != "hydsensread":
    #    path = os.path.split(path)[0]
    #file_loc = os.path.join(path, 'file_example')
    file_loc = "C:\\Users\\Laptop\\PycharmProjects\\qc_serie_temporelle\\input_files\\Waterlvl"
    # POUR LES STATIONS PIEZOMETRIQUE
    files = "Elgin (03090019).csv"
    # POUR LES STATION HYDROMETRIQUE
    # files = "011704_1972-1974.csv"

    file_location = os.path.join(file_loc, files)
    print(file_location)
    # level = WhatStreamAndLevelDataFileReader(file_location)
    level = WhatWaterLevelDataFileReader(file_location)

    print(level.sites.site_name)
    print(level.sites.other_identifier)
    #params = [t for t in level.sites.get_records]
    #print(params)
    #for date, val in zip(level.sites.records['Water level_masl'].index, level.sites.get_time_serie_by_param('Water level_masl')):
    #    print(date, val)
    #print(level.records.describe())
    #level.plot(dpi=300)
    #plt.show(block=True)
