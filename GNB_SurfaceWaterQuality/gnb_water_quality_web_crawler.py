#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-05-10'
__description__ = "permet d'aller pomper les données du site du nouveau brunswick concernant les" \
                  "données d'eau de surface"
__version__ = '1.0'

import datetime
import json

import bs4
import requests


class GNB_WaterQualityStation(object):
    STATION_PARAMETER_URL_ADRESS = "http://www.elgegl.gnb.ca/WaterNB-NBEau/fr/Lieu%C3%89chantillonnage/%C3%A9chantillons/{station_name}"
    SATION_DATA_URL_ADRESS = "http://www.elgegl.gnb.ca/WaterNB-NBEau/en/SamplingLocation/SamplesData/"

    def __init__(self, station_name: str):
        self.station_name = str(station_name)
        self.station_url_adress = self.STATION_PARAMETER_URL_ADRESS.format(station_name=self.station_name)
        self.station_parameters = {}
        self.no_param = []
        self.get_avaible_parameter()
        self.get_all_parameter_data()

    def get_avaible_parameter(self):
        web_site = requests.get(self.station_url_adress, params={'type': 2})
        webSiteContent = bs4.BeautifulSoup(web_site.text, "html.parser")
        # print(webSiteContent)
        for element in webSiteContent.find_all('input'):
            if element['class'] == ['stations']:
                self.station_parameters[element['value']] = {}

    def _make_parameter_data(self, parameter, json_file):
        self.station_parameters[parameter]['data'] = json_file['data'][0]
        self.station_parameters[parameter]['element'] = json_file['labels'][0]
        self.station_parameters[parameter]['unit'] = json_file['units'][0]
        self.station_parameters[parameter]['minVal'] = json_file['minVal']
        self.station_parameters[parameter]['maxVal'] = json_file['maxVal']
        self.station_parameters[parameter]['qaDone'] = json_file['qaDone']
        self.station_parameters[parameter]['unitDescriptions'] = json_file['unitDescriptions'][0]

    def get_all_parameter_data(self):
        for parameter in self.station_parameters.keys():
            web_site = requests.get(self.SATION_DATA_URL_ADRESS,
                                    params={'sampleLocationId': self.station_name,
                                            'parameterIds': parameter,
                                            'type': 2,
                                            'chartStartDate': '1980-01-01',
                                            'chartEndDate': datetime.date.today()}
                                    , headers={'Content-Type': 'application/json'})
            try:
                json_file = json.loads(web_site.text)
                self._make_parameter_data(parameter, json_file)
            except:
                self.no_param.append(parameter)
        self._clean_parameter_list()

    def _clean_parameter_list(self):
        for rem_param in self.no_param:
            self.station_parameters.pop(rem_param)

    def get_parameters_list(self)->list:
        param_list = []
        for param in self.station_parameters.keys():
            param_list.append(self.station_parameters[param]['element'])
        return param_list

    def get_sampling_date(self):
        value_for_station_by_date = {}
        for param in self.station_parameters.keys():
            data = self.station_parameters[param]['data']
            for time_data in data:
                if time_data[0] in value_for_station_by_date.keys():
                    value_for_station_by_date[time_data[0]][param] = time_data[1]
                else:
                    value_for_station_by_date[time_data[0]] = {}
                    value_for_station_by_date[time_data[0]][param] = time_data[1]
        for date in value_for_station_by_date.keys():
            print(value_for_station_by_date[date].keys())




if __name__ == '__main__':
    x = GNB_WaterQualityStation('470')
    x.get_sampling_date()
    # GNB_WaterQualityStation('20122')
    # GNB_WaterQualityStation('837')
