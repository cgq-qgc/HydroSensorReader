#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-12$'
__description__ = " "
__version__ = '1.0'

import datetime
import re
import typing
from collections import OrderedDict
import pandas as pd
import warnings
import numpy as np

class Parameter(object):
    """
    basic implementation of a parameter
    """
    
    def __init__(self, param_name, unit):
        self.parameter = param_name
        self.unit = unit

    def __str__(self) -> str:
        return '{}_{}'.format(self.parameter, self.unit)


class Record(object):
    """
    implementation of a basic record given by any kind of data file
    """
    
    def __init__(self, record_date: datetime.datetime = None,
                 parameter: str = None,
                 parameter_unit: str = None,
                 value=None):
        self.record_date = record_date
        self._parameter = Parameter(parameter, parameter_unit)
        self.value = value
    
    @property
    def parameter(self):
        return self._parameter.parameter
    
    @parameter.setter
    def parameter(self, value: str):
        self._parameter.parameter = value
    
    @property
    def parameter_unit(self):
        return self._parameter.unit
    
    @parameter_unit.setter
    def parameter_unit(self, value: str):
        self._parameter.unit = value

    @property
    def parameter_as_string(self):
        return self._parameter.__str__()


class TimeSeriesRecords(Record):
    """
    implementation of a TimeSeriesRecord. The record_date correspond to the first date of the values list.
    Values are stored as an OrderedDict : [(date1, value1),(date2, value2),...]
    """
    TimeSerieValue = typing.Dict[datetime.datetime, str]
    
    def __init__(self,
                 records_date: datetime.datetime = None,
                 values: TimeSerieValue = None,
                 parameter: str = None,
                 parameter_unit: str = None):
        super().__init__(records_date, parameter, parameter_unit, values)
        self.value = pd.Series()

    def add_value(self, _date: datetime.datetime, val):
        """
        Add a value to the self.value attribute. Duplicate values generate an error
        :param _date: date to add
        :param val: value to add
        """
        new_serie = pd.Series([val], index=_date)
        try:
            self.value.append(new_serie, verify_integrity=True)
        except ValueError as e:
            warnings.warn(str(e), ValueError)

    def reorder_values(self):
        warnings.warn('deprecated function not usefull for pd.Series objects',DeprecationWarning)
        new_dict = OrderedDict()
        for keys in sorted(self.value.keys()):
            new_dict[keys] = self.value[keys]
        self.value = new_dict
    
    def set_time_serie_values(self, times: typing.List[datetime.datetime], values: list):
        """
        Add multiple values to the time series
        :param times: list of datetime object
        :param values: list of values
        """
        new_serie = pd.Series(values, index=times)
        try:
            self.value.append(new_serie, verify_integrity=True)
        except ValueError as e:
            warnings.warn(str(e), ValueError)

    def get_data_at_time(self, at_date: datetime.datetime) -> pd.Series:
        """
        method that return a list of an unique Record if the date match the
        Record date or a list of all the Record for the given date
        :param at_date: datetime object corresponding to the needed Record
        :raise: KeyError if date not present
        """
        return self.value[at_date]
    
    def get_value_at_date(self, p_date):
        warnings.warn('deprecated element',DeprecationWarning)
        try:
            return self.value[p_date]
        except KeyError:
            return None
    
    def __str__(self) -> str:
        dates = self.get_dates
        return "{} ({}) :[{} ... {}]\n".format(self.parameter,
                                               self.parameter_unit,
                                               dates[:3],
                                               dates[-3:])
    
    def get_data_between(self, first_date: datetime.datetime, last_date: datetime.datetime) -> pd.Series:
        """
        method that return a list of all the Record for the given date interval selected by
        >= first_date and < last_date
        :param first_date: start datetime object corresponding to the needed Record
        :param last_date: end datetime object corresponding to the needed Record. The end date will not
        be included in the selection
        :return: list
        """
        assert first_date <= last_date, 'The first date must be before the last date'
        return self.value[first_date:last_date]

    def get_data_before_date(self, date_before: datetime.datetime) -> pd.Series:
        first_date = self.start_date
        if date_before < first_date:
            first_date = date_before
        return self.get_data_between(first_date, date_before)
    
    def get_data_after_date(self, date_after: datetime.datetime) -> pd.Series:
        last_date = self.end_date
        if date_after > last_date:
            last_date = date_after
        return self.get_data_between(date_after, last_date)
    
    @property
    def end_date(self) -> pd.Timestamp:
        return self.value.index.max()
    
    @property
    def start_date(self)-> pd.Timestamp:
        return self.value.index.min()
    
    @property
    def get_dates(self) -> np.ndarray:
        return self.value.index.to_pydatetime()


class ChemistryRecord(Record):
    """
    implementation of a Chemistry record. The main difference is that a chemetry record have a detection limit
    """
    
    def __init__(self, sampling_date: datetime.datetime = None,
                 parameter: str = None,
                 parameter_unit: str = None,
                 value: str = None,
                 detection_limit: str = None,
                 report_date: datetime.datetime = None,
                 analysis_type: str = None):
        """

        :param sampling_date: date when the sample have been taken
        :param parameter: parameter analyzed
        :param parameter_unit: unit of measurement for this parameter
        :param value: obtained value
        :param detection_limit: detection limit
        :param report_date: date of the analysis or report date if not sure
        """
        super().__init__(sampling_date, parameter, parameter_unit, value)
        self.lower_detection_limit = detection_limit
        self.report_date = report_date
        self.analysis_type = analysis_type
    
    @property
    def sampling_date(self):
        return self.record_date
    
    @sampling_date.setter
    def sampling_date(self, value):
        self.record_date = value
    
    def __str__(self) -> str:
        return "({}) -- {} : {} {}".format(self.sampling_date, self.parameter, self.value, self.parameter_unit)
    
    @property
    def normalized_value(self) -> float:
        """
        method returning a float value normalized by some business rules
        :return:
        """
        assert self.value is not None, "no value for the record"
        normal_value = float('nan')
        # transform trace, not detected, nd, n.d, ...
        # by dividing the detection limit by 2
        # if there is no detection limit, the result is NaN
        if re.search(r"^tr.*|n(.{0,1}|(ot).*)d.*|nan", self.value.lower()):
            if self.lower_detection_limit is not None:
                normal_value = float(self.lower_detection_limit) / 2.0
        # transform values like <0.5 to 0.25 by divinding the result by two
        elif re.search(r".*<.*", self.value):
            normal_value = float(re.sub(r"[< ]", '', self.value)) / 2.0
        # the result is just a result
        elif not re.search(r"^tr.*|n.d.*|.*<.*", self.value):
            normal_value = float(self.value)
        # todo : what to do with values above higher detection limit
        return normal_value




