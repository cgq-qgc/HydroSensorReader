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
                 last_recording:datetime.datetime = None,
                 project_name:str = None):
        super().__init__(site_name, visit_date, project_name)
        self.instrument_serial_number = instrument_serial_number
        self.last_recording = last_recording
        self.records = TimeSeriesRecords()

class Sample(Site):
    """
    Definition of a Sample as seen as a laboratory information. This represent the minimal informations
    given to/by the lab.
    """
    def __init__(self, site_name: str = None,
                 visit_date: datetime.datetime = None,
                 lab_sample_name:str = None,
                 sample_type:str = None,
                 project_name: str = None):
        super().__init__(site_name, visit_date,project_name)
        self.lab_sample_name = lab_sample_name
        self.sample_type = sample_type
        self.records = []

    def create_new_record(self) -> ChemistryRecord:
        new_rec = ChemistryRecord()
        self.records.append(new_rec)
        return self.records[-1]



