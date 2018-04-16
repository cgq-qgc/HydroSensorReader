HydroSensorReader
======================

[![Build Status](https://travis-ci.org/x-malet/scientific_file_reader.svg?branch=master)](https://travis-ci.org/x-malet/scientific_file_reader)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This project aim to provide a simple way to read a scientific file provided by any
kind of probe, sensor, or anything used specificly in hydrogeology.

## Installation

You can directly install this package with the command:
` pip install HydroSensorReader`.

After the installation, you can use the package by using 
```python
import hydsensread as hsr

# File based reader
file_path = 'my_file_path'

# Files Generating Timeseries results
# =====================================

# read CR1000 files
r = hsr.DATCampbellCRFileReader(file_path)

# read Hanna multiparameter probes 
# - (model HI-9828 and HI-9829 tested)
# - Supported extension : '.xls', '.xlsx'
r = hsr.XLSHannaFileReader(file_path)

# read Solinst Levelogger and Barologger files
# - Supported extension : '.lev', '.xle', '.csv'
r = hsr.SolinstFileReader(file_path)

# Plot the results with
r.plot()

# Files Generating Generic results
# =====================================
# read Maxxam laboratory analysis files.
# - Supported extension : '.xls', '.xlsx'
r = hsr.XSLMaxxamFileReader(file_path)


# Web data scrappers 
# These data scrappers use the station name.
station = 'StationName'
r = hsr.GNBWaterQualityStation(station)


```


Dependency
----------
- [openpyxl](https://openpyxl.readthedocs.io/en/default/)
- [xlrd](http://www.python-excel.org/)
- [xlwt](http://www.python-excel.org/)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
- [requests](http://docs.python-requests.org/en/master/)
- [pandas](https://pandas.pydata.org/)



Main entry point
-----
The main entry point for this project is the `file_reader` package. You can choose between the readers available and do your work.


Main package definition
=============

`file_reader`
----
Implementation of diffenrents files readers. _Each python files contain a main laucher to the the class._

* __compagny_file_reader__
_- Reader of generated files comming from different probes or labs._
* __web_page_reader__
_- Web crawlers in charge of extracting the datas from web sites_

`file_parser`
--------

This package contain the classes responsible of the different files reading. More information abouts these package is available into them
* __abstract_file_parser.py__
    * __AbstractFileParser__
    _- Abstract class used as an interface to implement the others_
* __concrete_file_parser.py__
    * __CSVFileParser__
    * __TXTFileParser__
    * __EXCELFileParser__
    * __WEB_XMLFileParser__

`site_and_records`
------
This package contain classes defining the domain elements and carry the data describing them
* __site.py__
    * __Site__
        _- A basic site class with the site name a the visited date_
    * __SensorPlateform__
        _- A Plateform is an that can take measurement as
                                 a standalone object_
    * __Sample__
        _- Sample as an object manipulated by a laboratory_
    * __StationSite__ - Modelisation of a station object
    * __StreamFlowStation__ - This specialized class was created to store the information of the [ECCC website](http://climate.weather.gc.ca/historical_data/search_historic_data_e.html)
* __records.py__
    * __Parameter__ - Class acting as a structure to store parameter (what is observed) and its associated unit
    * __Record__ 
    _- A record must have a date, a parameter, an unit and a value._
    * __TimeSeriesRecords__ 
    _- The record_date correspond to the first date of the values list. Values are stored as a Dict as following :_
        - { date1: value1, date2: value2,...}
    * __ChemistryRecord__
    _-A chemistry record have a detection limit a report date and an analysis type and all the attributes of a __Record___
        
`file_example`
------------

You have several files examples in this folder used a tests
    
    
Work To Do
----------
-   Add a `.LAS` reader to take care of __borehole geophysics__ files
-   Add a `.LAS` reader to take care of __LiDar__ data
-   Create a Strategy class so you can input a file and the strategy class select the correct `file_reader` class
-   Continue documentation...always...

    

   