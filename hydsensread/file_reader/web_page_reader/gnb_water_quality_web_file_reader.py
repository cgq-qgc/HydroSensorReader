#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-05-10'
__description__ = "permet d'aller pomper les données du site du nouveau brunswick concernant les" \
                  "données d'eau de surface"
__version__ = '1.0'

import datetime
import json
import warnings
from collections import defaultdict

import bs4
import requests

from hydsensread.file_reader.abstract_file_reader import TimeSeriesGeochemistryFileReader


class GNBWaterQualityStation(TimeSeriesGeochemistryFileReader):
    STATION_PARAMETER_URL_ADRESS = "http://www.elgegl.gnb.ca/WaterNB-NBEau/fr/Lieu%C3%89chantillonnage/%C3%A9chantillons/{station_name}"
    SATION_DATA_URL_ADRESS = "http://www.elgegl.gnb.ca/WaterNB-NBEau/en/SamplingLocation/SamplesData/"

    def __init__(self, station_name: str):
        warnings.warn('Class needs to be re-implemented', DeprecationWarning)

        self.station_name = str(station_name)
        web_site_name = self.STATION_PARAMETER_URL_ADRESS.format(station_name=self.station_name)
        super(GNBWaterQualityStation, self).__init__(file_path=web_site_name)
        self.station_parameters = defaultdict(dict)
        self.no_param = []
        self.get_time_series_data(self.station_name).site_name = self.station_name
        self.get_time_series_data(self.station_name).visit_date = datetime.datetime.now()

    def _read_file_data_header(self):
        self.get_avaible_parameter()

    def _read_file_data(self):
        self.get_all_parameter_data()

    def _read_file_header(self):
        pass

    @property
    def file_content(self) -> bs4.BeautifulSoup:
        return self.file_reader.get_file_content

    def get_avaible_parameter(self):
        for element in self.file_content.find_all('input'):
            if element['class'] == ['stations']:
                self.station_parameters[element['value']] = {}

    def _make_parameter_data(self,  json_file):
        """
        method that create a TimeSeriesRecord in the _sites_of_interest[TIMES_SERIES]
        :param json_file:
        :return:
        """
        # don't know if the dates ares always the same...
        dates_ = self._transform_to_datetime(json_file['data'][0])
        values = [value[1] for value in  json_file['data'][0]]
        parameter = json_file['labels'][0]
        param_unit = json_file['units'][0]
        self.get_time_series_data(self.station_name).create_time_serie(parameter, param_unit,dates_,values)

    def _transform_to_datetime(self,data:list) ->list:
        return [datetime.datetime.strptime(value[0], self.YEAR_S_MONTH_S_DAY_HM_DATE_STRING_FORMAT.replace("/","-"))
                for value in  data]

    def _attempt_request_for_parameter(self, param):
        timeout = 10
        for i in range(10):
            try:
                web_site = requests.get(self.SATION_DATA_URL_ADRESS,
                                        params={'sampleLocationId': self.station_name,
                                                'parameterIds': param,
                                                'type': 2,
                                                'chartStartDate': '1980-01-01',
                                                'chartEndDate': datetime.date.today()}
                                        , headers={'Content-Type': 'application/json'},
                                        timeout=timeout)
                json_file = json.loads(web_site.text)
                self._make_parameter_data(json_file)
            except requests.exceptions.ReadTimeout:
                timeout += 10
                print("try {}".format(timeout))
                continue
            except Exception as e:
                raise e
            else:
                break

    def get_all_parameter_data(self):
        for parameter in self.station_parameters.keys():
            try:
                self._attempt_request_for_parameter(parameter)
            except Exception as e:
                print(e.args)
                print(type(e))
                # the parameter have no results for the current station
                print("station {station_name} have no results for {param}\n".format(station_name=self.station_name,param= parameter))
                self.no_param.append(parameter)
        self._clean_parameter_list()

    def _clean_parameter_list(self):
        """
        method that remove all the parameter having no data for them
        :return:
        """
        for rem_param in self.no_param:
            self.station_parameters.pop(rem_param)
    def get_parameters_list(self)->list:
        return [self.station_parameters[param]['element']
                for param in self.station_parameters.keys()]


    def get_sampling_date(self, p_station_name = None):
        station_name = p_station_name
        if p_station_name is None:
            station_name = self.station_name
        value_for_station_by_date = {}
        for param in self.station_parameters.keys():
            data = self.station_parameters[param]['data']
            for time_data in data:
                if time_data[0] in value_for_station_by_date.keys():
                    value_for_station_by_date[time_data[0]][param] = time_data[1]
                else:
                    value_for_station_by_date[time_data[0]] = {}
                    value_for_station_by_date[time_data[0]][param] = time_data[1]

    def makes_samples_with_time_series(self, site_name=None):
        super().makes_samples_with_time_series(self.station_name)

    @TimeSeriesGeochemistryFileReader.time_series_dates.getter
    def time_series_dates(self):
        self._date_list = self._get_date_list(self.station_name)
        return self._date_list

if __name__ == '__main__':
    x = GNBWaterQualityStation('837')
    x.read_file()
    print(x.time_series_dates)

    # GNB_WaterQualityStation('20122')
    # GNB_WaterQualityStation('470')
