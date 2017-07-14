#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-12$'
__description__ = " "
__version__ = '1.0'
from abc import abstractmethod
import datetime
from typing import Dict,List
from collections import OrderedDict



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
                 value= None):
        self.record_date = record_date
        self._parameter = Parameter(parameter, parameter_unit)
        self.value = value

    @property
    def parameter(self):
        return self._parameter.parameter

    @parameter.setter
    def parameter(self, value:str):
        self._parameter.parameter = value

    @property
    def parameter_unit(self):
        return self._parameter.unit

    @parameter_unit.setter
    def parameter_unit(self, value:str):
        self._parameter.unit = value


class TimeSeriesRecords(Record):
    """
    implementation of a TimeSeriesRecord. The record_date correspond to the first date of the values list.
    Values are stored as an OrderedDict : [(date1, value1),(date2, value2),...]
    """
    TimeSerieValue = Dict[datetime.datetime, str]
    def __init__(self,
                 records_date: datetime.datetime = None,
                 values: TimeSerieValue = None,
                 parameter: str = None,
                 parameter_unit: str = None):
        super().__init__(records_date, parameter, parameter_unit, values)
        if self.value is None:
            self.value = OrderedDict()

    def set_time_serie_values(self,times:List[datetime.datetime], values:list):
        for date,val in zip(times,values):
            self.value[date] = val

    def get_data_at_time(self, at_date: datetime.datetime) -> list:
        """
        method that return a list of an unique Record if the date match the
        Record date or a list of all the Record for the given date
        :param at_date: datetime object corresponding to the needed Record"""
        date_val_return = []
        if at_date in  self.value.keys():

            date_val_return.append([at_date,self.value[at_date]])
        elif at_date.date() in \
            [dict_dates.date() for dict_dates in list(self.value.keys())]:

            for dates,val in self.value.items():
                if dates.date() == at_date.date():
                    date_val_return.append([dates, val])
        return date_val_return

    def get_data_between(self, first_date: datetime.datetime, last_date: datetime.datetime) -> list:
        """
        method that return a list of all the Record for the given date interval selected by
        >= first_date and < last_date
        :param first_date: start datetime object corresponding to the needed Record
        :param last_date: end datetime object corresponding to the needed Record. The end date will not
        be included in the selection
        :return: list
        """
        assert first_date <= last_date, 'The first date must be before the last date'
        returned_data = []
        try:
            first_record_date = self.get_data_at_time(first_date)[0][0]
            second_record_date = self.get_data_at_time(last_date)[0][0]

            for dates,val in self.value.items():
                if dates >= first_record_date and dates <= second_record_date:
                    returned_data.append([dates,val])
                if dates > second_record_date:
                    break
        except IndexError:
            pass
        finally:
            return returned_data

    def get_data_before_date(self,date_before:datetime.datetime)->list:
        first_date = self.start_date
        if date_before < first_date:
            first_date = date_before
        return self.get_data_between(first_date,date_before)

    def get_data_after_date(self, date_after:datetime.datetime) ->list:
        last_date = self.end_date
        if date_after > last_date:
            last_date = date_after
        return self.get_data_between(date_after,last_date)


    @property
    def end_date(self):
        return list(self.value.keys())[-1]

    @property
    def start_date(self):
        return list(self.value.keys())[0]

class ChemistryRecord(Record):
    """
    implementation of a Chemistry record. The main difference is that a chemetry record have a detection limit
    """
    def __init__(self, sampling_date: datetime.datetime = None,
                 parameter: str = None,
                 parameter_unit: str = None,
                 value: str = None,
                 detection_limit:str = None,
                 report_date:datetime.datetime=None):
        """

        :param sampling_date: date when the sample have been taken
        :param parameter: parameter analyzed
        :param parameter_unit: unit of measurement for this parameter
        :param value: obtained value
        :param detection_limit: detection limit
        :param report_date: date of the analysis or report date if not sure
        """
        super().__init__(sampling_date, parameter, parameter_unit, value)
        self.detection_limit = detection_limit
        self.report_date = report_date
    @property
    def normalized_value(self):
        """
        method returning a float value normalized
        :return:
        """


if __name__ == '__main__':
    ts = TimeSeriesRecords()
    dates = [datetime.datetime(2014,10,3,15,00),
             datetime.datetime(2014, 10, 3, 15, 30),
             datetime.datetime(2014, 10, 4, 15, 00),
             datetime.datetime(2014, 10, 5, 15, 00),
             datetime.datetime(2014, 10, 6, 15, 00),
             datetime.datetime(2014, 10, 7, 15, 00)]
    vals = list(range(len(dates)))
    for i,j in zip(dates,vals):
        print(i,j)
    ts.set_time_serie_values(dates,vals)
    print(ts.get_data_at_time(datetime.datetime(2014, 10, 3,15,30)))
    print(ts.get_data_at_time(datetime.datetime(2014, 10, 3)))