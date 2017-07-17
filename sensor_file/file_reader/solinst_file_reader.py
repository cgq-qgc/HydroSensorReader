#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = " "
__version__ = '1.0'



from sensor_file.domain.site import SensorPlateform
from sensor_file.file_reader.abstract_file_reader import PlateformReaderFile
import warnings

class SolinstFileReader(PlateformReaderFile):
    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)
        self.__main_reader = self.__set_reader()

    def __set_reader(self):
        file_ext = self.file_extension

        if file_ext in self.CSV_FILES_TYPES:
            self.__main_reader = CSVSolinstFileReader()
        elif file_ext == 'lev':
            self.__main_reader = LEVSolinstFileReader()
        elif file_ext == 'xle':
            self.__main_reader = XLESolinstFileReader()
        else:
            warnings.warn("Unknown file extension for this compagny")
        self._site_of_interest = self.__main_reader._site_of_interest

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        self.__main_reader._read_file_header()

    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        self.__main_reader._read_file_data()

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        self.__main_reader._read_file_data_header()



class LEVSolinstFileReader(PlateformReaderFile):
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


class XLESolinstFileReader(PlateformReaderFile):
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


class CSVSolinstFileReader(PlateformReaderFile):
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