Scientific File Reader
======================

This project aim to provide a simple way to read a scientific file provided by any
kind of probe, sensor, or anything used specificly in hydrogeology.

Dependency
----------
- [openpyxl](https://openpyxl.readthedocs.io/en/default/)
- [xlrd](http://www.python-excel.org/)
- [bs4](https://www.crummy.com/software/BeautifulSoup/)
- [requests](http://docs.python-requests.org/en/master/)



Main entry point
-----
The main entry point for this project is the `file_reader` package. You can choose between the readers available and do your work.

Work To Do
----------
-   Add a `.LAS` reader to take care of __borehole geophysics__ files
-   Add a `.LAS` reader to take care of __LiDar__ data
-   Create a Strategy class so you can input a file and the strategy class select the correct `file_reader` class
-   Continue documentation...always...


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
    
    

   