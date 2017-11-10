#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = "Permet de lire des fichiers provenant de l'interface" \
                  " WHAT : https://github.com/jnsebgosselin/what.git"
__version__ = '1.0'
from abc import abstractmethod

import datetime
from typing import Union

from site_and_records import StationSite, geographical_coordinates, StreamFlowStation
from file_reader.abstract_file_reader import TimeSeriesFileReader, date_list

WHAT_METEO_FILES_HEADER_LENGTH = 10
WHAT_WATER_LEVEL_FILES_HEADER_LENGTH = 8
WHAT_STREAM_FLOW_STATION_HEADER_LENGTH = 19

station_possible = Union[StationSite, StreamFlowStation]


class AbstractWhatFileReader(TimeSeriesFileReader):
    def __init__(self, file_name: str = None, header_length: int = WHAT_METEO_FILES_HEADER_LENGTH,
                 station_type: station_possible=None):
        # if file_name is None:
        #     pass
        # else:
        super().__init__(file_name, header_length)
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
                    datas.append(row[index + start_data_column])
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
            if what_to_search in data[0]:
                self._site_of_interest.__dict__[attribute] = data[1]
                break

    def _make_station_id(self, what_to_search):
        self._set_station_attribute('site_name', what_to_search)

    def _make_station_other_name(self, what_to_search):
        self._set_station_attribute('other_identifier', what_to_search)


class WhatMeteorologicalDataFileReader(AbstractWhatFileReader):
    def __init__(self, file_name: str = None):
        super().__init__(file_name, WHAT_METEO_FILES_HEADER_LENGTH,StationSite())

    def _read_file_data_header(self):
        self._make_station_coordinates_from_file()
        self._make_station_id('Climate Identifier')
        self._make_station_other_name('Station Name')

    def _get_date_list(self) -> date_list:
        return self._make_date_list()

    def _read_file_data(self, start_data_column: int = 3):
        super()._read_file_data(start_data_column)


class WhatWaterLevelDataFileReader(AbstractWhatFileReader):
    def __init__(self, file_name: str = None):
        super().__init__(file_name, WHAT_WATER_LEVEL_FILES_HEADER_LENGTH,station_type=StationSite())

    def _read_file_data(self, start_data_column: int = 4):
        super()._read_file_data(start_data_column)

    def _read_file_data_header(self):
        self._make_station_coordinates_from_file()
        self._make_station_id('Well ID')
        self._make_station_other_name('Well Name')

    def _get_date_list(self) -> date_list:
        return self._make_date_list(1, 2, 3)


class WhatStreamAndLevelDataFileReader(AbstractWhatFileReader):
    def __init__(self, file_name: str = None,
                 header_length: int = WHAT_STREAM_FLOW_STATION_HEADER_LENGTH):
        super().__init__(file_name, header_length, StreamFlowStation())

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


if __name__ == '__main__':
    import os

    name = os.getcwd()
    path = os.path.split(os.getcwd())[0]
    while name != 'qc_serie_temporelle':
        path = os.path.split(path)[0]
        name = os.path.basename(path)

    # POUR LES STATIONS PIEZOMETRIQUE

    # path = os.path.join(path, 'input_files', 'Waterlvl', 'Barraute (08070001).csv')
    # level = WhatWaterLevelDataFileReader(file_path)

    # POUR LES STATION HYDROMETRIQUE
    files = "051502_1967-2017.csv"
    file_path = os.path.join(path, 'input_files', 'Streamflow and Level', files)
    level = WhatStreamAndLevelDataFileReader(file_path)
    print(level.sites.site_name)

    params = [t.parameter for t in level.sites.get_records()]
    print(params)
    print(level.sites.get_time_serie_by_param(params[1]))
