#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = " "
__version__ = '1.0'



from sensor_file.file_reader.abstract_file_reader import PlateformReaderFile

class CSVHannaFileReader(PlateformReaderFile):
    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)

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