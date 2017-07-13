#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-12$'
__description__ = " "
__version__ = '1.0'

import datetime
from typing import Tuple

TimeSerieValue = Tuple[datetime.datetime, str]

class Parameter(object):
    """
    basic implementation of a parameter
    """
    def __init__(self, param_name, unit):
        self.parameter = param_name
        self.unit = unit


class Record(object):
    """
    implementation of a basic record given by any kind of data file
    """
    def __init__(self, record_date:datetime.datetime= None,
                 parameter:str= None,
                 parameter_unit:str= None,
                 value:str= None):
        self.record_date = record_date
        self.parameter = Parameter(parameter,parameter_unit)
        self.value = value

class TimeSeriesRecords(Record):
    """
    implementation of a TimeSeriesRecord. The record_date correspond to the first date of the values list.
    Values are stored as a list of tuples as : [(date1, value1),(date2, value2),...]
    """
    def __init__(self,
                 records_date: datetime.datetime = None,
                 values: TimeSerieValue = None,
                 parameter: str = None,
                 parameter_unit: str = None):
        super().__init__(records_date, parameter, parameter_unit, values)

class ChemistryRecord(Record):
    """
    implementation of a Chemistry record. The main difference is that a chemetry record have a detection limit
    """
    def __init__(self, record_date: datetime.datetime = None,
                 parameter: str = None,
                 parameter_unit: str = None,
                 value: str = None,
                 detection_limit:str = None,
                 report_date:datetime.datetime=None):
        super().__init__(record_date, parameter, parameter_unit, value)
        self.detection_limit = detection_limit
        self.report_date = report_date