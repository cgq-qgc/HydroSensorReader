#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-12$'
__description__ = " "
__version__ = '1.0'

import datetime
from sensor_file.domain.records import TimeSeriesRecords
from sensor_file.domain.records import ChemistryRecord

class Site(object):
    """
    most basic site definition with a site name and a visit date
    """
    def __init__(self,site_name:str = None,
                 visit_date:datetime.datetime = None,
                 project_name: str = None):
        self.site_name = site_name
        self.visit_date = visit_date
        self.project_name = project_name
        self.records = None



class SensorPlateform(Site):
    """
    Definition of a Sensor plateform site. A plateform is an object that can take measurement as
    a standalone object.
    """

    def __init__(self, site_name: str = None,
                 visit_date: datetime.datetime = None,
                 instrument_serial_number:str = None,
                 project_name:str = None):
        """
        initialization of a sensor plateform
        :param site_name: site name or location name of the sensor
        :param visit_date: usually, when the file have been created
        :param instrument_serial_number: serial number of the sensor
        :param project_name: project name
        """
        super().__init__(site_name, visit_date, project_name)
        self.instrument_serial_number = instrument_serial_number
        self.records = [] # list(TimeSeriesRecords())
        self.batterie_level = None
        self.model_number = None
        self.longest_time_series = None
        self._datetime_not_in_longest_time_series = []

    def get_unique_dates_for_all_record(self):
        self.set_longest_time_series()
        self.all_times_series_dates_are_equals()
        all_dates = self.longest_time_series

        if len(self._datetime_not_in_longest_time_series ) != 0:
            all_dates.append(self._datetime_not_in_longest_time_series)
        dates = sorted(all_dates)
        return dates

    def create_time_serie(self,parameter,unit,dates,values):
        time_serie = TimeSeriesRecords()
        time_serie.parameter = parameter
        time_serie.parameter_unit = unit
        time_serie.set_time_serie_values(dates,values)
        self.records.append(time_serie)
        self.set_longest_time_series()

    def __str__(self) -> str:
        return "({serial}):{site} - {date}".format(serial= self.instrument_serial_number,
                                                   site=self.site_name,
                                                   date=self.visit_date)

    def set_longest_time_series(self):
        max_len = 0
        times_serie_date = None
        for ts in self.records:
            if len(ts.get_dates) > max_len:
                max_len = len(ts.get_dates)
                times_serie_date = ts.get_dates
        self.longest_time_series = times_serie_date

        self.all_times_series_dates_are_equals()


    def _is_date_in_longest_time_series(self, p_date) -> bool:
        _times_series_are_equals = True
        if p_date not in self.longest_time_series:
            if p_date not in self._datetime_not_in_longest_time_series:
                _times_series_are_equals = False
                self._datetime_not_in_longest_time_series.append(p_date)
        return _times_series_are_equals

    def all_times_series_dates_are_equals(self) -> bool:
        # get the longest time series
        if self.longest_time_series is None:
            self.set_longest_time_series()
        _times_series_are_equals = True
        for ts in self.records:
            # date list are differents
            if ts.get_dates != self.longest_time_series:
                for _dates in ts.get_dates:
                    _times_series_are_equals = self._is_date_in_longest_time_series(_dates)
                    if _times_series_are_equals == False:
                        break
        return _times_series_are_equals


class Sample(Site):
    """
    Definition of a Sample as seen as a laboratory information. This represent the minimal informations
    given to/by the lab.
    """
    def __init__(self, site_name: str = None,
                 visit_date: datetime.datetime = None,  # sampling date
                 lab_sample_name:str = None,
                 sample_type:str = None,
                 analysis_type:str = None,
                 project_name: str = None):
        """
        initialization of a sample
        :param site_name: site name
        :param visit_date: sampling date
        :param lab_sample_name: laboratory name
        :param sample_type: sample type (blank, sample, duplicate,...)
        :param analysis_type: analysis type
        :param project_name: project name
        """
        super().__init__(site_name, visit_date,project_name)
        self.lab_sample_name = lab_sample_name
        self.sample_type = sample_type
        self.records = []   #list(ChemistryRecord)
        self.analysis_type = analysis_type

    def create_new_record(self) -> ChemistryRecord:
        new_rec = ChemistryRecord()
        self.records.append(new_rec)
        return self.records[-1]

    def create_complete_record(self,samp_date,param,param_unit,value,detect_lim,report_date,ana_type):
        new_rec = ChemistryRecord(sampling_date=samp_date,
                                  parameter=param,
                                  parameter_unit=param_unit,
                                  value=value,
                                  detection_limit=detect_lim,
                                  report_date=report_date,
                                  analysis_type=ana_type)
        self.records.append(new_rec)





