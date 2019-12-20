#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'X-Malet'
__date__ = '2017-07-12'
__description__ = " "
__version__ = '1.0'

import datetime
from collections import namedtuple
from typing import List

import numpy as np

from pandas import DataFrame, Series

from .records import ChemistryRecord
from .records import TimeSeriesRecords

geographical_coordinates = namedtuple('XYZPoint', ['x', 'y', 'z'])


class Site(object):
    """
    Most basic site definition with a site name and a visit date.
    """

    def __init__(self, site_name: str = None,
                 visit_date: datetime.datetime = None,
                 project_name: str = None):
        self.site_name = site_name
        self.visit_date = visit_date
        self.project_name = project_name
        self._records = None
        self.other_attributes = {}

    def get_records(self):
        return self._records


class SensorPlateform(Site):
    """
    Definition of a Sensor plateform site.

    A plateform is an object that can take measurement as a standalone object.
    """

    def __init__(self, site_name: str = None,
                 visit_date: datetime.datetime = None,
                 instrument_serial_number: str = None,
                 project_name: str = None):
        """
        initialization of a sensor plateform
        :param site_name: site name or location name of the sensor
        :param visit_date: usually, when the file have been created
        :param instrument_serial_number: serial number of the sensor
        :param project_name: project name
        """
        super().__init__(site_name, visit_date, project_name)
        self.instrument_serial_number = instrument_serial_number
        self.records = DataFrame()
        self.batterie_level = None
        self.model_number = None
        self.longest_time_series = None
        self._datetime_not_in_longest_time_series = []

    @property
    def get_records(self) -> DataFrame:
        return self.records

    def get_time_serie_by_param(self, p_parameter) -> Series:
        if p_parameter in self.records.columns.values:
            return self.records[p_parameter]

    @property
    def get_dates(self) -> np.ndarray:
        return self.records.index.values

    def create_time_serie(self, parameter, unit, dates: List[datetime.datetime], values: list):
        """
        Create a new TimeSerie and add id to the self.records DataFrame
        :param parameter: observed parameter
        :param unit: parameter's unit
        :param dates: list of datetime objects
        :param values: list of values
        :return:
        """
        if parameter in self.records.keys():
            raise ValueError('time serie with the same parameter allready exist')

        time_serie = TimeSeriesRecords(dates, values, parameter, unit)

        if len(self.records.index) == 0:
            # create a new dataframe
            self.records = DataFrame(data=time_serie.value, index=time_serie.get_dates,
                                        columns=[time_serie.parameter_as_string])
        elif False in (time_serie.get_dates == self.records.index):
            # If dates differs
            self.resample_records(new_time_serie=time_serie)
        else:
            # same dates and dataframe exist
            self.records[time_serie.parameter_as_string] = time_serie.value

    def resample_records(self, new_time_serie: TimeSeriesRecords):
        """
        Create a new dataframe by appending a new TimeSeriesRecords
        :param new_time_serie: TimeSeriesRecords to append
        """
        new_data_frame = DataFrame(data=new_time_serie.value,
                                      index=new_time_serie.get_dates,
                                      columns=[new_time_serie.parameter_as_string])

        new_time_delta = new_data_frame.index[1] - new_data_frame.index[0]
        old_time_delta = self.records.index[1] - self.records.index[0]
        # The timeDelta of the new TimeSeriesRecords is lower
        if old_time_delta > new_time_delta:
            self.records = new_data_frame.combine_first(self.records)
        else:
            self.records = self.records.combine_first(new_data_frame)

    def __str__(self) -> str:
        return "({serial}):{site} - {date}".format(serial=self.instrument_serial_number,
                                                   site=self.site_name,
                                                   date=self.visit_date)


class Sample(Site):
    """
    Definition of a Sample as seen as a laboratory information. This represent the minimal informations
    given to/by the lab.
    """

    def __init__(self, site_name: str = None,
                 visit_date: datetime.datetime = None,  # sampling date
                 lab_sample_name: str = None,
                 sample_type: str = None,
                 analysis_type: str = None,
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
        super().__init__(site_name, visit_date, project_name)
        self.lab_sample_name = lab_sample_name
        self.sample_type = sample_type
        self.records = []  # list(ChemistryRecord)
        self.analysis_type = analysis_type

    def get_records(self) -> List[ChemistryRecord]:
        return self.records

    def create_new_record(self) -> ChemistryRecord:
        new_rec = ChemistryRecord()
        self.records.append(new_rec)
        return self.records[-1]

    def create_complete_record(self, samp_date, param, param_unit, value, detect_lim, report_date, ana_type):
        new_rec = ChemistryRecord(sampling_date=samp_date,
                                  parameter=param,
                                  parameter_unit=param_unit,
                                  value=value,
                                  detection_limit=detect_lim,
                                  report_date=report_date,
                                  analysis_type=ana_type)
        self.records.append(new_rec)

    def get_record_by_parameter(self, p_parameter) -> ChemistryRecord:
        record = None
        for rec in self.get_records():
            if rec.parameter == p_parameter:
                record = rec
                break
        return record

    def __str__(self) -> str:
        str_sample = "sample name:{} at date:{}\n".format(self.site_name, self.visit_date)
        for rec in self.records:
            str_sample += "\t" + str(rec) + "\n"

        return str_sample


class StationSite(SensorPlateform):
    def __init__(self, site_name: str = None,
                 visit_date: datetime.datetime = None,
                 project_name: str = None,
                 other_identifier: str = None,
                 coordinates_x_y_z: geographical_coordinates = None):
        super().__init__(site_name, visit_date, project_name)
        self.other_identifier = other_identifier
        self.coordinates_x_y_z = coordinates_x_y_z

    def __str__(self) -> str:
        return "({other_name}):{site} - {coordinates}". \
            format(other_name=self.other_identifier,
                   site=self.site_name,
                   coordinates=self.coordinates_x_y_z)


class StreamFlowStation(StationSite):
    def __init__(self, site_name: str = None,
                 visit_date: datetime.datetime = None,
                 project_name: str = None,
                 other_identifier: str = None,
                 coordinates_x_y_z: geographical_coordinates = None,
                 site_description: str = None,
                 station_activity_status: str = None,
                 active_period: str = None,
                 municipality: str = None,
                 administrative_region: str = None,
                 stream_name: str = None,
                 hydrographic_region: str = None,
                 drain_area: str = None,
                 flow_regime: str = None,
                 federal_id: str = None,
                 province: str = None):
        super().__init__(site_name, visit_date, project_name, other_identifier, coordinates_x_y_z)
        self.site_description = site_description
        self.station_activity_status = station_activity_status
        self.active_period = active_period
        self.municipality = municipality
        self.administrative_region = administrative_region
        self.stream_name = stream_name
        self.hydrographic_region = hydrographic_region
        self.drain_area = drain_area
        self.flow_regime = flow_regime
        self.federal_id = federal_id
        self.province = province

    def __str__(self) -> str:
        return "({other_name}):{site} - {coordinates}". \
            format(other_name=self.other_identifier,
                   site=self.site_name,
                   coordinates=self.coordinates_x_y_z)


class DrillingSite(StationSite):
    def __init__(self,
                 site_name: str = None,
                 visit_date: datetime.datetime = None,
                 project_name: str = None,
                 other_identifier: str = None,
                 coordinates_x_y_z: geographical_coordinates = None,
                 drilling_depth: float = 0.0,
                 drill_dip: float = 0.0,
                 drill_azimut: float = 0.0,
                 drilling_diameter: float = 0.0):
        super().__init__(site_name, visit_date, project_name, other_identifier, coordinates_x_y_z)
        self.drilling_depth = drilling_depth
        self.drill_dip = drill_dip
        self.drill_azimut = drill_azimut
        self.drilling_diameter = drilling_diameter

    def __str__(self) -> str:
        return "{coordinates} - {site_name} ({depth} deep) made in {date}".format(coordinates=self.coordinates_x_y_z,
                                                                                  site_name=self.site_name,
                                                                                  depth=self.drilling_depth,
                                                                                  date=self.visit_date)
