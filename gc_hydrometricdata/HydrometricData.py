#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-01-23'
__description__ = " "
__version__ = '1.0'

from gc_hydrometricdata.web_crawler.abstractstation import AbstractHydrometricStation
from gc_hydrometricdata.web_crawler.hydrometric_station import HistoricalHydrometricStation, RealTimeHydrometricStation
from gc_hydrometricdata.web_crawler.station_list import *

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()



class HydrometricDataInterface(object):
    def __init__(self):
        self._historic_station = None
        self._real_time_station = None
        self._stationData = {}

    def getStationsForProvince(self, provinceName: str):
        self._historic_station = HistoricalHydrometricStationList(provinceName)
        self._real_time_station = RealTimeHydrometricStationList(provinceName)

    def _extractStationData(self, stationNumber: str):
        if self.isStationPresent(stationNumber):
            self._stationData[stationNumber] = {}
            if stationNumber in self.getStationInBoth():
                print('station have historic and real-time data')
                self._stationData[stationNumber][HISTORICAL_DATA_KEY] = HistoricalHydrometricStation(stationNumber)
                self._stationData[stationNumber][REAL_TIME_DATA_KEY] = RealTimeHydrometricStation(stationNumber)
            else:
                if stationNumber in self.historicStationList:
                    print('station have historic data only')

                    self._stationData[stationNumber][HISTORICAL_DATA_KEY] = HistoricalHydrometricStation(stationNumber)
                elif stationNumber in self.realTimeStationList:
                    print('station have real-time data only')

                    self._stationData[stationNumber][REAL_TIME_DATA_KEY] = RealTimeHydrometricStation(stationNumber)
        else:
            raise AttributeError('Station not in the station list')

    def isStationPresent(self, stationNumber) -> bool:
        return stationNumber in self.allStationList

    @property
    def historicStationList(self) -> dict:
        return self._historic_station.station_list

    @property
    def realTimeStationList(self) -> dict:
        return self._real_time_station.station_list

    def getStationInBoth(self) -> list:
        return sorted([station for station in self.historicStationList if station in self.realTimeStationList])

    @property
    def allStationList(self) -> list:
        historicStation = [station for station in self.historicStationList]
        realTimeStation = [station for station in self.realTimeStationList if station not in self.historicStationList]
        return historicStation + realTimeStation

    def getStation(self, stationNumber) -> dict:
        if stationNumber not in self._stationData.keys():
            self._extractStationData(stationNumber)

        return self._stationData[stationNumber]

    def _getDataTypeForStation(self, stationNumber, dataType) -> AbstractHydrometricStation:
        if dataType in self.getStation(stationNumber).keys():
            return self.getStation(stationNumber)[dataType]
        else:
            raise KeyError("Station doesn't have the requested data")

    def getHistoricalStation(self, stationNumber) -> AbstractHydrometricStation:
        return self._getDataTypeForStation(stationNumber, HISTORICAL_DATA_KEY)

    def getRealTimeStation(self, stationNumber) -> AbstractHydrometricStation:
        return self._getDataTypeForStation(stationNumber, REAL_TIME_DATA_KEY)

    def getStationInfo(self, stationNumber) -> dict:
        if self.isStationPresent(stationNumber):
            if stationNumber in self.historicStationList:
                return self.getHistoricalStation(stationNumber).stationInformation
            else:
                return self.getRealTimeStation(stationNumber).stationInformation
        else:
            raise AttributeError('Station not in the station list')

    def getStationCoordinates(self, stationNumber) -> tuple:
        if self.isStationPresent(stationNumber):
            if stationNumber in self.historicStationList:
                return self.getHistoricalStation(stationNumber).coordinates
            else:
                return self.getRealTimeStation(stationNumber).coordinates
        else:
            raise AttributeError('Station not in the station list')


if __name__ == '__main__':

    webStation = HydrometricDataInterface()
    webStation.getStationsForProvince('New Brunswick')

    for station in webStation.historicStationList.items():
        for name in ['pollet','apoha', 'petitco']:
            if  name in station[1].lower():
                print("="*25)
                print(station)
                print(webStation.getStationInfo(station[0]))
                break

    stationName = "01BF004"
    print("=" * 15)
    print("Example of how to use the interface")
    print("=" * 15)
    print("getting station info")
    print(webStation.getStationInfo(stationName))
    print("=" * 15)
    # print("getting station coordinates")
    # print("=" * 15)
    # print(webStation.getStationCoordinates(stationName))
    # print("=" * 15)
    # print("getting station data")
    # print("=" * 15)
    # webStation.getHistoricalStation(stationName).getData()
    # print(webStation.getHistoricalStation(stationName).data)
