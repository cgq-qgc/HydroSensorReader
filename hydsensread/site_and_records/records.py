#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-12$'
__description__ = " "
__version__ = '1.0'

import datetime
import re
import typing
import warnings
from collections import OrderedDict

import numpy as np
import pandas as pd


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
    Values are stored as a pandas.Series
    """

    def __init__(self,
                 records_date: typing.Union[list, typing.List[datetime.datetime], pd.DatetimeIndex] = None,
                 values: typing.Union[list, typing.List[int], typing.List[float], np.ndarray] = None,
                 parameter: str = None,
                 parameter_unit: str = None):
        """

        :param records_date:
        :param values:
        :param parameter:
        :param parameter_unit:
        """
        if records_date is not None and values is not None:

            super().__init__(records_date[0],
                             parameter, parameter_unit, values[0])
            self.value = pd.Series(data=values, index=records_date, name=self.parameter_as_string)
        else:
            super().__init__(records_date, parameter, parameter_unit, values)
            self.value = pd.Series(dtype=float)

    def add_value(self, _date: datetime.datetime, val):
        """
        Add a value to the self.value attribute. Duplicate values generate an error
        :param _date: date to add
        :param val: value to add
        """
        warnings.warn('deprecated method', DeprecationWarning)
        new_serie = pd.Series([val], index=_date)
        try:
            self.value.append(new_serie, verify_integrity=True)
        except ValueError as e:
            warnings.warn(str(e), ValueError)

    def reorder_values(self):
        warnings.warn('deprecated function not usefull for pd.Series objects', DeprecationWarning)
        new_dict = OrderedDict()
        for keys in sorted(self.value.keys()):
            new_dict[keys] = self.value[keys]
        self.value = new_dict

    def set_time_serie_values(self, times: typing.Union[typing.List[datetime.datetime], pd.DatetimeIndex],
                              values: typing.Union[np.ndarray, list]):
        """
        Add multiple values to the time series
        :param times: list of datetime object
        :param values: list of values
        :raise : AssertionError if Times and Values are not the same size
        """
        assert len(times) == len(values), "Times and values are not the same size"

        try:

            new_ts = pd.Series(values, index=times)
            self.value = self.value.append(new_ts, verify_integrity=True, ignore_index=False)
        except ValueError as e:
            warnings.warn(str(e), ValueError)

    def get_data_at_time(self, at_date: typing.Union[datetime.datetime, str, datetime.date]) -> pd.Series:
        """
        Return a list of an unique Record if the date match the
        Record date or a list of all the Record for the given date
        :param at_date: datetime object corresponding to the needed Record
        :raise: KeyError if date not present
        """
        return self.value[at_date]

    def get_value_at_date(self, p_date):
        warnings.warn('deprecated element', DeprecationWarning)
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

    def get_data_between(self, first_date: typing.Union[datetime.datetime, str],
                         last_date: typing.Union[datetime.datetime, str]) -> pd.Series:
        """
        method that return a list of all the Record for the given date interval selected by
        >= first_date and < last_date
        :param first_date: start datetime object corresponding to the needed Record
        :param last_date: end datetime object corresponding to the needed Record. The end date will not
        be included in the selection
        :return: pandas Series of the selected values
        """
        # convert to pandas.Timestamp object for comparision of possible string and datetime input
        f_date = pd.Timestamp(first_date)
        l_date = pd.Timestamp(last_date)
        if f_date > l_date:
            return self.value[l_date:f_date]
        else:
            return self.value[f_date:l_date]

    def get_data_before_date(self, date_before: typing.Union[datetime.datetime, str]) -> pd.Series:
        """
        Return a pandas.Series object. If date_before is inferior of self.start_date, return
        :param date_before: input date
        :return: If date_before is inferior of self.start_date, return an empty Series
        """
        return self.value[:date_before]

    def get_data_after_date(self, date_after: typing.Union[datetime.datetime, str]) -> pd.Series:
        """
        Return a pandas.Series object. If date_after is inferior of self.start_date, return
        :param date_after: input date
        :return: If date_after is superior to self.end_date, return an empty Series
        """
        return self.value[date_after:]

    @property
    def end_date(self) -> pd.Timestamp:
        return self.value.index.max()

    @property
    def start_date(self) -> pd.Timestamp:
        return self.value.index.min()

    @property
    def get_dates(self) -> np.ndarray:
        return self.value.index.values


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
