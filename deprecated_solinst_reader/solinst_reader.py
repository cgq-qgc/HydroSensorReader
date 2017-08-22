#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2016-04-25'
__description__ = " "
__version__ = '1.0'

import datetime
import re
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from deprecated_solinst_reader.deprec_abstract_file_reader import FileReader


class SolinstXLE_Reader(FileReader):
    """
    classe permettant d'extraire des données d'un fichier .XLE de Solinst.
    les fichiers au format .xle sont en fait des fichier XML. ils sont ouvert avec
    beautifull soup pour en lire le contenu
    """
    CHANNEL_DATA_HEADER = "Ch{}_data_header"

    warnings.simplefilter("always")
    warnings.warn('class not maintained anymore', DeprecationWarning)

    def __init__(self, file_name: str = None):
        """
        :param file_name: string représentant l'emplacement/nom du fichier à ouvrir      
        """
        super(SolinstXLE_Reader, self).__init__(file_name)


    def reload(self, file_name):
        old_file_name = self._file_name
        self._file_name = file_name
        if self._validate_file():
            self._load_file()
        else:
            self._file_name = old_file_name

    def _validate_file_type(self) -> bool:
        return re.search(r".*xle$", self._file_name) is not None

    def read_file_data_header(self):
        super().read_file_data_header()

    def open_file(self):
        self.number_of_channel = 0
        self.file_data = None
        self.file_data_header.clear()
        self.file_header.clear()
        self.file_data = pd.DataFrame()
        self._file_content = BeautifulSoup(open(self._file_name), 'xml')
        print('file {} opened'.format(self._file_name))

    def read_file_header(self):
        self.get_file_info()
        self.get_instrument_info()
        self.get_instrument_info_data_header()
        self.get_channel_data_header()
        self.parametre_list = list(self.file_data_header.keys())

        print(self.file_header)
        print("num of channel: {}".format(self.number_of_channel))

    def get_file_info(self):
        self._get_header_info('File_info')

    def get_instrument_info(self):
        self._get_header_info('Instrument_info')

    def get_instrument_info_data_header(self):
        self._get_header_info('Instrument_info_data_header')

    def get_channel_data_header(self):

        for i in range(5):
            channel_name = self.CHANNEL_DATA_HEADER.format(i + 1)
            try:
                self._get_data_header_info(channel_name)
            except:
                self.file_data_header.pop(channel_name.lower())
                break
            else:
                self.number_of_channel += 1

    def _get_header_info(self, header_name: str):
        self.file_header[header_name.lower()] = {}
        xml_part_content = self._file_content.select_one(header_name)
        for data in xml_part_content:
            if data.name is not None:
                self.file_header[header_name.lower()][data.name.lower()] = data.string

    def _get_data_header_info(self, header_name:str):
        self.file_data_header[header_name.lower()] = {}
        xml_part_content = self._file_content.select_one(header_name)
        for data in xml_part_content:
            if data.name is not None:
                self.file_data_header[header_name.lower()][data.name.lower()] = data.string

    def show_data_graphics(self):
        self.file_data.plot(subplots=True)
        plt.show()

    def get_raw_data(self, xml_data_string):
        all_data = []
        for i in range(self.number_of_channel):
            all_data.append([float(d.text) for d in xml_data_string.find_all('ch{}'.format(i + 1))])

        zipped_list = []
        for row in range(len(all_data[0])):
            tuple_to_add = ()
            for col in range(len(all_data)):
                tuple_to_add = tuple_to_add + (all_data[col][row],)
            zipped_list.append(tuple_to_add)
        return zipped_list

    def read_file_data(self):

        date = None
        temps = None
        ms = None
        ch2 = None
        ch1 = None
        all_data = None
        for _data in self.xle_file.find_all('Data'):
            date = [d.text for d in _data.find_all('Date')]
            temps = [d.text for d in _data.find_all('Time')]
            ms = [d.text for d in _data.find_all('ms')]
            all_data = self.get_raw_data(_data)

        self.file_data = pd.DataFrame(
                data=np.array(all_data),
                index=[np.array(date), np.array(temps)],
                columns=self.get_column_labels())

    def get_column_labels(self) -> list:
        columns_label = []
        for channel in range(self.number_of_channel):
            parameter = self.CHANNEL_DATA_HEADER.format(channel + 1).lower()
            columns_label.append("{}({})".format(self.file_data_header[parameter]['identification'],
                                                 self.file_data_header[parameter]['unit']).lower())
        return columns_label

    @property
    def xle_file(self):
        return self._file_content

    @xle_file.setter
    def xle_file(self, value):
        self._file_content = BeautifulSoup(open(value), 'xml')

    @property
    def start_time(self):
        return datetime.datetime.strptime(self.file_header['instrument_info_data_header']['start_time'], "%Y/%m/%d %H:%M:%S")

    @property
    def stop_time(self):
        return datetime.datetime.strptime(
            "{} {}".format(self.file_header['file_info']['date'], self.file_header['file_info']['time']),
            "%Y/%m/%d %H:%M:%S")

    @property
    def instrument_info(self):
        return self.file_header['instrument_info']

    @property
    def instrument_info_data(self):
        return self.file_header['instrument_info_data_header']

    @property
    def location(self):
        return self.instrument_info_data['location']

    @property
    def sampling_rate_in_seconds(self):
        return float(self.instrument_info_data['sample_rate']) / 100

    @property
    def sampling_rate_in_minutes(self):
        return self.sampling_rate_in_seconds / 60


class SolinstLEV_Reader(FileReader):
    def __init__(self,file_name: str = None):
        super(SolinstLEV_Reader, self).__init__(file_name)

    def open_file(self):
        with open(self._file_name,'r') as t:
            self._file_content = [line.replace('\n','') for line in t]
        t.close()
        for lines in self._file_content:
            if lines == "[Data]":
                break
            else:
                print("_"*25)
                print(lines)
                line = re.split(r"[:=]",lines,maxsplit=1)
                print(line)
                print(len(line))
                try:
                    print(line[0].replace(" ",'') +": "+ line[1])
                except:
                    print(line[0].replace("[",'').replace("]",''))
        # print(self._file_content)


    def read_file_data(self):
        pass

    def _validate_file_type(self) -> bool:
        return re.search(r".*(\.lev)$") is not None



    def read_file_data_header(self):
        pass

    def read_file_header(self):
        pass


if __name__ == '__main__':
    import os
    path = os.getcwd()
    while os.path.split(path)[1] != "scientific_file_reader":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')

    teste_all = True

    if teste_all:
        file_location = os.path.join(file_loc,"2029499_F7_NordChamp_PL20150925_2015_09_25.xle")
        xle_reader = SolinstXLE_Reader(file_name=file_location)
        print(xle_reader.location)
        print(xle_reader.start_time)
        print(xle_reader.stop_time)
        print(xle_reader.sampling_rate_in_minutes)
        print(xle_reader.file_data_header)
        # file_location = file_example + "2026236_F4_20160222_2016_06_24.xle"
        # xle_reader.reload(file_location)
        # print("-" * 15)
        # print(xle_reader.location)
        # print(xle_reader.start_time)
        # print(xle_reader.stop_time)
        # print(xle_reader.sampling_rate_in_minutes)
    else:

        file_location = os.path.join(file_loc,"F2_20160223.lev")
        lev_reader = SolinstLEV_Reader(file_location)

