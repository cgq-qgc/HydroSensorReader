#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = " "
__version__ = '1.0'

import datetime
import warnings
import re
from sensor_file.file_reader.abstract_file_reader import PlateformReaderFile


class SolinstFileReader(PlateformReaderFile):
    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)
        self.__main_reader = None

    def __set_reader(self):
        file_ext = self.file_extension

        if file_ext in self.CSV_FILES_TYPES:
            self.__main_reader = CSVSolinstFileReader(self._file)
        elif file_ext == 'lev':
            self.__main_reader = LEVSolinstFileReader(self._file)
        elif file_ext == 'xle':
            self.__main_reader = XLESolinstFileReader(self._file)
        else:
            warnings.warn("Unknown file extension for this compagny")
        print(self.__main_reader)
        self._site_of_interest = self.__main_reader._site_of_interest

    def read_file(self):
        self.__set_reader()
        self.__main_reader.read_file()


class LEVSolinstFileReader(PlateformReaderFile):
    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)
        self.date_times = self._get_date_list()

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        self._create_plateform()

    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        self._get_data()

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        pass

    def _create_plateform(self):
        self._site_of_interest.visit_date = self._create_visited_date()
        self._site_of_interest.site_name = self._get_site_name()
        self._site_of_interest.instrument_serial_number = self._get_serial_number()
        self._site_of_interest.project_name = self._get_project_name()
        self._site_of_interest.batterie_level = None
        self._site_of_interest.model_number = None

    def _create_visited_date(self) -> datetime:
        _date = None
        _time = None
        for lines in self.file_content[:self._header_length]:
            if re.search("^date.*",lines.lower()):
                _date = lines.split(":")[1].replace(" ","")
            if re.search(r"^time.*",lines.lower()):
                _time = lines.split(" :")[1].replace(" ","")
        self._update_header_lentgh()
        to_datetime = datetime.datetime.strptime("{} {}".format(_date,_time),'%m/%d/%y %H:%M:%S')
        return to_datetime
    def _update_header_lentgh(self):
        for i,lines in enumerate(self.file_content):
            if re.search('^.data.*',lines.lower()):
                self._header_length = i+1
                break

    def _get_instrument_info(self, regex_:str) ->str:
        str_to_find = None
        for lines in self.file_content:
            if re.search(regex_, lines):
                str_to_find = lines.split("=")[1]
                break
        return str_to_find

    def _get_site_name(self) -> str:
        return self._get_instrument_info(r".*[lL]ocation.*")

    def _get_serial_number(self):
        serial_string = self._get_instrument_info(r".*(S|s)erial.number.*")
        serial_numb = re.split(r"[ -]",serial_string)[1]
        return serial_numb

    def _get_project_name(self):
        return self._get_instrument_info(r".*(I|i)nstrument.number.*")

    def _get_number_of_channels(self) ->int:
        return int(self._get_instrument_info(r" *Channel *=.*"))


    def _get_date_list(self) -> list:
        datetime_list = []
        for lines in self.file_content[self._header_length+1:-1]:
            sep_line = lines.split(" ")
            _date_time = datetime.datetime.strptime("{} {}".format(sep_line[0],sep_line[1]),'%Y/%m/%d %H:%M:%S.%f')
            datetime_list.append(_date_time)
        return datetime_list

    def _get_data(self):
        pass


class XLESolinstFileReader(PlateformReaderFile):
    CHANNEL_DATA_HEADER = "Ch{}_data_header"

    def __init__(self, file_name: str = None, header_length: int = 10):
        super().__init__(file_name, header_length)
        self.dates_list = self._get_date_list()

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        self._create_plateform()

    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        self._get_data()

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        pass

    def _create_plateform(self):
        self._site_of_interest.visit_date = self._create_visited_date()
        self._site_of_interest.site_name = self._get_site_name()
        self._site_of_interest.instrument_serial_number = self._get_serial_number()
        self._site_of_interest.project_name = self._get_project_name()
        self._site_of_interest.batterie_level = self._get_battery_level()
        self._site_of_interest.model_number = self._get_model_number()

    def _create_visited_date(self) -> datetime:
        date_str = self.file_content.select_one('File_info').Date.string
        time_str = self.file_content.select_one('File_info').Time.string
        datetime_str = "{} {}".format(date_str, time_str)
        datetime_obj = datetime.datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
        return datetime_obj

    def _get_site_name(self) -> str:
        return self.file_content.select_one('Instrument_info_data_header').Location.string

    def _get_serial_number(self):
        return self.file_content.select_one('Instrument_info').Serial_number.string

    def _get_project_name(self):
        return self.file_content.select_one('Instrument_info_data_header').Project_ID.string

    def _get_number_of_channels(self):
        return int(self.file_content.select_one('Instrument_info').Channel.string)

    def _get_model_number(self):
        return self.file_content.select_one('Instrument_info').Model_number.string

    def _get_battery_level(self):
        return self.file_content.select_one('Instrument_info').Battery_level.string

    def _get_date_list(self) -> list:
        datetime_list = []
        for _data in self.file_content.find_all('Log'):
            date_time_add = datetime.datetime.strptime("{} {}:{}".
                                                       format(_data.Date.string,
                                                              _data.Time.string,
                                                              _data.ms.string), '%Y/%m/%d %H:%M:%S:%f')
            datetime_list.append(date_time_add)
        return datetime_list

    def _get_data(self):
        for channels in range(self._get_number_of_channels()):
            channel_name = self.CHANNEL_DATA_HEADER.format(channels + 1)
            channel_parammeter = self.file_content.select_one(channel_name).Identification.string
            channel_unit = self.file_content.select_one(channel_name).Unit.string
            ch_selector = "ch{}"
            for _data in self.file_content.find_all('Data'):
                values = [d.text for d in _data.find_all(ch_selector.format(channels + 1))]
                self._site_of_interest.\
                    create_time_serie(channel_parammeter,
                                      channel_unit,self.dates_list,
                                      values)


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


if __name__ == '__main__':
    import os

    path = os.getcwd()
    while os.path.split(path)[1] != "scientific_file_reader":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')

    teste_all = True

    if teste_all:
        # file_location = os.path.join(file_loc, "2029499_F7_NordChamp_PL20150925_2015_09_25.xle")
        file_location = os.path.join(file_loc,"2041929_PO-06_XM20170307_2017_03_07.lev")

        solinst_file = SolinstFileReader(file_location)
        solinst_file.read_file()

        # for time_serie in solinst_file.sites.records:
        #     print(str(time_serie))
