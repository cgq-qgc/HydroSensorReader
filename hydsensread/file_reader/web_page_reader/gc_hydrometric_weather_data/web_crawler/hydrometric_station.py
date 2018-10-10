#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-01-19'
__description__ = " "
__version__ = '1.0'

import bs4
import datetime
import requests
from re import search, split
from hydsensread.file_reader.web_page_reader.gc_hydrometric_weather_data.web_crawler.abstractstation import AbstractHydrometricStation


HISTORICAL_STATION_DATA = "https://eau.ec.gc.ca/report/historical_e.html"
REAL_TIME_STATION_DATA_URL = "https://eau.ec.gc.ca/report/real_time_e.html"


class HistoricalHydrometricStation(AbstractHydrometricStation):
    def __init__(self, stationNumber):
        super().__init__(stationNumber, HISTORICAL_STATION_DATA)

    def getData(self):
        self.data = self.getStationHistoricalData()

    def getAvaibleParameters(self):
        parameters = []

        r = requests.get(self.dataURL,
                         params={'stn': self.stationNumber},
                         cookies={'disclaimer': 'agree'},
                         verify=False)
        webSiteContent = bs4.BeautifulSoup(r.text, "html.parser")

        for ele in webSiteContent.find_all('select'):
            if ele.get('id') == 'selectDataType':
                for option in ele.find_all('option'):
                    parameters.append(option.attrs['value'])
        return parameters

    def getYearsForParameter(self):
        """
        Method that return a dict with

        :param stationNumber:
        :return: dict(PARAM) = [LIST_OF_YEARS_FOR_PARAM]
        """
        historic_params = self.getAvaibleParameters()
        returnDict = {}
        for params in historic_params:
            r = requests.get(self.dataURL,
                             params={
                                 'stn': self.stationNumber,
                                 'parameterType': params
                             },
                             cookies={'disclaimer': 'agree'},
                             verify=False)
            webSiteContent = bs4.BeautifulSoup(r.text, "html.parser")
            returnDict[params] = []
            for ele in webSiteContent.find_all('select'):
                if ele.get('id') == 'selectYear':
                    for option in ele.find_all('option'):
                        returnDict[params].append(option.attrs['value'])
        return returnDict

    def extractHistoricalData(self, webSiteContent: bs4.BeautifulSoup):
        """
        this method is executed for each year for each parameter
        :param webSiteContent:
        :return: dict
            dict_structure:
            [YEAR:int]
            [MONTH:int]
            [DATA:
                [date:str, value:str (when avaible : legend:str)]
        """
        # gettings parameter unit
        unit = ""
        for s in webSiteContent \
                .find('main') \
                .find('h2') \
                .find('abbr').contents:
            unit += s.string

        # Fetching parameters legend
        parameter_legend = {}
        for item in webSiteContent \
                .find('main') \
                .find('ul', {'class': 'legend'}) \
                .find_all('li'):
            params_list = item.string.split(' = ')
            parameter_legend[params_list[0]] = params_list[1]

        # extract data
        dict_historic_data = {}
        year = int(webSiteContent.find('main').find('h2').contents[0][:4])
        dict_historic_data[year] = {}
        dict_historic_data[year]['unit'] = unit
        # make empty list for each month
        for mth in range(1, 13):
            dict_historic_data[year][mth] = []
        # fetch data
        for ele in webSiteContent.find('table').find('tbody').find_all('tr'):
            day = int(ele.find('th').string.replace('\n', '').replace('\t', ''))
            for month, value in enumerate(ele.find_all('td')):
                date = ""
                try:
                    # get date first. If the day don't exist, GoTo ValueError ==> pass
                    date = datetime.date(year, month + 1, day)
                    # if the cell have a legend
                    if search(r'[A-Z]', value.string):
                        dict_historic_data[year][month + 1].append(
                            [date.strftime('%Y-%m-%d'),
                             split(r' *', value.string)[0], parameter_legend[split(r' *', value.string)[1]]])
                    else:
                        dict_historic_data[year][month + 1].append(
                            [date.strftime('%Y-%m-%d'), value.string.replace(' ', '')])
                except ValueError:
                    pass

        return dict_historic_data

    def getStationHistoricalData(self):
        historical_dict = self.getYearsForParameter()
        fetch_data = {}
        for parameter in historical_dict:
            fetch_data[parameter] = {}
            newDict = self.getRequestDict('Daily')
            newDict.update({'parameterType': parameter})
            print('FETCHING PARAMETER ' + parameter)

            for year in historical_dict[parameter]:
                newDict.update({'year': year})
                print('FETCHING YEAR ' + str(year))

                r = requests.get(HISTORICAL_STATION_DATA,
                                 params=newDict, cookies={'disclaimer': 'agree'},
                                 verify=False)
                webSiteContent = bs4.BeautifulSoup(r.text, "html.parser")
                print(r.url)
                fetch_data[parameter].update(self.extractHistoricalData(webSiteContent))
        print('END OF FETCHING')
        return fetch_data


class RealTimeHydrometricStation(AbstractHydrometricStation):
    def __init__(self, stationNumber):
        super().__init__(stationNumber, REAL_TIME_STATION_DATA_URL)

    def getData(self):
        self.data = self.getStationRealTimeData()

    def getRealTimeAvaibleParameters(self):
        parameters = {}

        r = requests.get(self.dataURL, params={'stn': self.stationNumber}, cookies={'disclaimer': 'agree'},
                         verify=False)

        webSiteContent = bs4.BeautifulSoup(r.text, "html.parser")

        for ele in webSiteContent.find_all('select'):
            if ele.get('id') == 'selectTypey1':
                for option in ele.find_all('option'):
                    parameters[option.string] = option.attrs['value']
        return parameters

    def getStationRealTimeData(self):
        stationData = {}
        # get avaible parameters for the station
        stationParameters = self.getRealTimeAvaibleParameters()
        # iterate for each station
        for params in stationParameters:
            stationData[params] = {}
            newDict = self.getRequestDict()
            newDict['prm1'] = stationParameters[params]
            print('fetching ' + params)
            # Make the request with the station parameter
            r = requests.get(self.dataURL, params=newDict, cookies={'disclaimer': 'agree'},
                             verify=False)

            stationDataInWebSite = bs4.BeautifulSoup(r.text, "html.parser")

            # get the table header
            stationData[params]['header'] = []
            for ele in stationDataInWebSite.find('table').find('thead').find('tr').find_all('th'):
                stationData[params]['header'].append(ele.contents[0].string.replace('\t', '').replace('\n', ''))
            # Get the data
            stationData[params]['data'] = []
            for data in stationDataInWebSite.find('table').find('tbody').find_all('tr'):
                stationData[params]['data'].append([rowData
                                                    for dat in data.find_all('td')
                                                    for rowData in dat])
        return stationData
