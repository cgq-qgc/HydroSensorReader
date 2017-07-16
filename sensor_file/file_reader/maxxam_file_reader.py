#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = " "
__version__ = '1.0'



import datetime
from sensor_file.domain.site import Sample
from sensor_file.file_reader.abstract_file_reader import AbstractFileReader

class MaxxamFileReader(AbstractFileReader):
    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)
        self._site_of_interest = [] #list of Samples


    def create_sample(self):
        sample = Sample()
        self._site_of_interest.append(sample)
        yield self._site_of_interest[-1]

    def create_complete_sample(self,site_name: str = None,
                 visit_date: datetime.datetime = None,
                 lab_sample_name:str = None,
                 sample_type:str = None,
                 project_name: str = None):
        sample = Sample(site_name,visit_date,lab_sample_name,sample_type,project_name)
        self._site_of_interest.append(sample)
        yield self._site_of_interest[-1]

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        pass

    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        pass

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        pass