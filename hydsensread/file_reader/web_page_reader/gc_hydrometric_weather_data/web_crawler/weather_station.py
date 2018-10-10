#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-01-19'
__description__ = " "
__version__ = '1.0'

import bs4
import requests

# WIP

WEATHER_STATION_DATA_URL = "http://climate.weather.gc.ca/climate_data/daily_data_e.html"


dict = """
hlyRange:%7C
dlyRange:1998-02-01%7C2007-11-30
mlyRange:1998-04-01%7C2007-11-01
StationID:10700
Prov:AB
urlExtension:_e.html
searchType:stnProv
optLimit:yearRange
StartYear:1840
EndYear:2017
selRowPerPage:100
Line:0
Month:11
Day:23
lstProvince:
timeframe:2
Year:2007
"""

r1 = requests.get("http://climate.weather.gc.ca/climate_data/daily_data_e.html?&StationID=5309&Year=1973")
bsFile = bs4.BeautifulSoup(r1.text, 'html.parser')
for data in bsFile.find('select', {'id': 'Year1'}):
    if isinstance(data, bs4.element.Tag):
        print(data['value'])

        r = requests.get(
            "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=5309&timeframe=2&Year={}".format(
                data['value']))
        for line in r.text.split('\n'):
            if line.replace('"', '').split(",")[0] == 'Date/Time':
                print("=" * 15)
                print(len(line.replace('"', '').split(",")))
                print("=" * 15)
            else:
                print(len(line.replace('"', '').split(",")))
            print(line.replace('"', '').split(","))