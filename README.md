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

Main package definition
=============

file_example
------------

You have several files examples in this folder used a tests

sensor_file
-----------

This is the main package of the project.

* __sensor_file__

    * __domain__
        _- the base classes that will define and carry the data_
        * __site.py__
            * __Site__
                _- A basic site class with the site name a the visited date_
            * __SensorPlateform__
                _- A Plateform is an that can take measurement as
                                         a standalone object_
            * __Sample__
                _- Sample as an object manipulated by a laboratory_
                
        * __records.py__
            * __Record__ 
            _- A record must have a date, a parameter, an unit and a value._
            * __TimeSeriesRecords__ 
            _- The record_date correspond to the first date of the values list. Values are stored as a Dict as following :_
                - { date1: value1, date2: value2,...}
            * __ChemistryRecord__
            _-A chemistry record have a detection limit a report date and an analysis type and all the attributes of a __Record___
            
    * __file_parser__
    _- This package contain the classes responsible of the different files reading_
        * __abstract_file_parser.py__
            * __AbstractFileParser__
            _- Abstract class used as an interface to implement the others_
        * __concrete_file_parser.py__
            * __CSVFileParser__
            * __TXTFileParser__
            * __EXCELFileParser__
            * __WEB_XMLFileParser__
    * __file_reader__
    _- Implementation of diffenrents files readers_
    
        _Each python files contain a main laucher to the the class._

        * __compagny_file_reader__
        _- Reader of generated files comming from different probes or labs._
        * __web_page_reader__
        _- Web crawlers in charge of extracting the datas from web sites_
        
    * __compagny_file.py__ _- This is a Work in progress_
    
Work To Do
----------

I want to use the class in __compagny_file.py__ as a _StategyClass Pattern_ so you juste
have to use it to reader a file and get the data out of it... Work in "no" progress


I will add a .LAS reader someday to take care of diagraphy files...will see!            
   