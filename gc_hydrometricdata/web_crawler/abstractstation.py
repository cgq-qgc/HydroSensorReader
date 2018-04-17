#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-01-19'
__description__ = " "
__version__ = '1.0'

import bs4
import datetime
import requests
from abc import abstractmethod, abstractproperty, ABCMeta
from re import search, split


class AbstractStation(metaclass=ABCMeta):
    def __init__(self, stationNumber, dataURL):
        self.stationNumber = stationNumber
        self.dataURL = dataURL
        self.stationInformation = None
        self.data = None

    @abstractmethod
    def getData(self, *arg, **kwargs):
        pass

    @abstractmethod
    def getRequestDict(self, *arg, **kwargs) -> dict:
        pass

    @abstractmethod
    def getStationInfo(self):
        pass


class AbstractHydrometricStation(AbstractStation, metaclass=ABCMeta):
    def __init__(self, stationNumber, dataURL):
        super(AbstractHydrometricStation, self).__init__(stationNumber, dataURL)
        self.getStationInfo()

    def getStationInfo(self):
        if self.dataURL == None:
            raise AttributeError('invalid dataURL')
        r = requests.get(self.dataURL,
                         params={'stn': self.stationNumber},
                         cookies={'disclaimer': 'agree'},
                         verify=False)
        stationDataInWebSite = bs4.BeautifulSoup(r.text, "html.parser")

        station_information = {}
        currentWebID = ""
        for ele in stationDataInWebSite.find('div', {'class': 'metadata'}) \
                .find_all('div', {'class': 'col-md-6 col-sm-6 col-xs-6'}):
            try:
                # get the row id
                currentWebID = ele['id']
            except KeyError:
                # if no ID on the row, take the data
                if ele['aria-labelledby'] == currentWebID:
                    # transform location data from deg, min,sec to deg
                    if len(ele.contents) > 2:
                        station_information[currentWebID] = float(ele.contents[0]) + \
                                                            float(ele.contents[2].string) / 60 + \
                                                            float(ele.contents[4].string) / 3600
                    else:
                        station_information[currentWebID] = ele.contents[0].string
        self.stationInformation = station_information

    @property
    def coordinates(self):
        return (self.stationInformation['latitude'], self.stationInformation['longitude'])

    def getRequestDict(self, dataType='Real-Time'):
        delta = datetime.datetime(2017, 1, 19) - datetime.datetime(2015, 7, 19)

        if dataType != 'Real-Time':
            returnDict = {
                'stn': self.stationNumber,
                'dataType': dataType,
                'mode': 'Table',
                'y1Max': 1, 'y1Min': 1,
                'results_type': 'historical',
                'type': "h2oArc"
            }
        else:
            returnDict = {
                'endDate': datetime.datetime.now().strftime('%Y-%m-%d'),
                'startDate': (datetime.datetime.now() - delta).strftime('%Y-%m-%d'),
                'stn': self.stationNumber,
                'dataType': dataType,
                'mode': 'Table',
                'y1Max': 1, 'y1Min': 1
            }
        return returnDict


WEATHER_STATION_LIST_URL = "http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html"


class AbstractWeatherStation(AbstractStation, metaclass=ABCMeta):
    def __init__(self, stationNumber, dataURL):
        super().__init__(stationNumber, dataURL)

    def getRequestDict(self, *arg, **kwargs) -> dict:
        return super().getRequestDict(*arg, **kwargs)


if __name__ == '__main__':
    print(str(datetime.datetime.now().year))
    print(str(datetime.datetime.now().month))
    print(str(datetime.datetime.now().day))
