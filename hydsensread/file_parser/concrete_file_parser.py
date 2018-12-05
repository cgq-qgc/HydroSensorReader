#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Laptop$'
__date__ = '2017-07-11$'
__description__ = " "
__version__ = '1.0'

import csv
import re
import warnings
import xml.etree.ElementTree as ET
from collections import OrderedDict

import bs4
import openpyxl
import requests
import xlrd

from .abstract_file_parser import AbstractFileParser


class CSVFileParser(AbstractFileParser):
    def __init__(self, file_path: str = None,
                 header_length: int = 10,
                 encoding_style: str = 'iso-8859-1',
                 csv_delim_regex: str = None):
        super().__init__(file_path, header_length)
        self.encoding_style = encoding_style
        self.csv_delim_regex = csv_delim_regex

    def read_file(self):
        """Read and save the content of the csv in a list."""
        with open(self._file, 'r', encoding=self.encoding_style) as csvfile:
            if self.csv_delim_regex is None:
                delimiter = ','
            else:
                delimiter = re.search(self.csv_delim_regex,
                                      csvfile.read(),
                                      flags=re.IGNORECASE).group(1)
                csvfile.seek(0)
            self._file_content = list(
                csv.reader(csvfile, delimiter=delimiter, lineterminator='\n'))

    def read_file_header(self):
        try:
            if not re.search(r"csv", self._file[-4:].lower()):
                raise TypeError("Bad file type")
            with open(self._file, 'r') as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read())
                csvfile.seek(0)
                file_reader = csv.reader(csvfile, dialect=dialect)
                for i, row in enumerate(file_reader):
                    self._file_header_content.append(row)

                    if i > self._header_length:
                        break
        except TypeError as e:
            warnings.warn("Error occured when trying to read the current file {}".format(self._file))


class TXTFileParser(AbstractFileParser):
    def __init__(self, file_path: str = None, header_length: int = 20, encoding='utf8'):
        self._encoding = encoding
        super().__init__(file_path, header_length)

    def read_file(self):
        with open(self._file, 'r', encoding=self._encoding) as txt_file:
            self._file_content = [line.replace('\n', '') for line in txt_file.readlines()]

    def read_file_header(self):
        try:
            if re.search(r"csv|xl.*", self._file[-4:].lower()):
                raise TypeError("Bad file type")
            with open(self._file, 'r') as txt_file:
                self._file_header_content = [line.replace('\n', '')
                                             for i, line in enumerate(txt_file.readlines())
                                             if i < self._header_length]
        except TypeError as e:
            warnings.warn("Error occured when trying to read the current file {}".format(self._file))


class EXCELFileParser(AbstractFileParser):
    def __init__(self, file_path: str = None, header_length: int = None):
        super().__init__(file_path, header_length)
        self._file_content = OrderedDict()
        self._file_header_content = {}
        self.nb_sheets = 0

    def read_file(self):
        try:
            assert re.search(r".*xl.*", self._file)
            if re.search(r".*xls$", self._file):
                self.__read_xls_file()
            elif re.search(r".*xlsx$", self._file):
                self.__read_xlsx_file()
            else:
                raise TypeError("Excel file not supported.")
        except AssertionError as e:
            warnings.warn("Error: Bad file extension. This is not an Excel file")
        except TypeError as t:
            warnings.warn("Error occured when trying to read the current file {}".format(self._file))
            print(t)

    def __read_xls_file(self):
        """
        method that read an xls file and create an entry in the file content dictionnary
        having the sheet name as a key
        example: self._file_content['Sheet1'] = [ [row1],[row2],...] ]
        each row is a list of cell values as follow : row1 = [cell1.value, cell2.value,...]
        NOTE: during the xls data parsing:
        -   cells that contains date are transformed as datetime.datetime
        -   blank or empty cells or replaced by None
        :return: None
        """
        file = xlrd.open_workbook(self._file)

        for sheet in file.sheet_names():
            self.nb_sheets += 1
            current_sheet = file.sheet_by_name(sheet)
            sheet_content = []
            for row in range(current_sheet.nrows):
                current_row = []
                # transform the cells value to the appropriate type
                for cells in current_sheet.row(row):
                    # convert blank and empty cells to None
                    if cells.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                        current_row.append(None)
                    # convert xldate cells to datetime.datetime.
                    elif cells.ctype == xlrd.XL_CELL_DATE:
                        current_row.append(xlrd.xldate.xldate_as_datetime(cells.value, file.datemode))
                    else:
                        current_row.append(cells.value)
                sheet_content.append(current_row)
            self._file_content[sheet] = sheet_content
            #
            setattr(EXCELFileParser, 'sheet{}'.format(self.nb_sheets), self._file_content[sheet])

    def __read_xlsx_file(self):
        """
        method that read an xlsx file and create an entry in the file content dictionnary
        having the sheet name as a key
        example: self._file_content['Sheet1'] = [ [row1],[row2],...] ]
        each row is a list of cell values as follow : row1 = [cell1.value, cell2.value,...]
        NOTE: during the xlsx data parsing, cells that contains date are transformed as datetime.datetime
        :return: None
        """
        excel_file = openpyxl.load_workbook(filename=self._file)
        for sheet in excel_file.sheetnames:
            self.nb_sheets += 1
            current_sheet = excel_file[sheet]
            sheet_content = []
            for row in current_sheet.rows:
                current_row = []
                for cell in row:
                    current_row.append(cell.value)
                sheet_content.append(current_row)
            self._file_content[sheet] = sheet_content
            setattr(EXCELFileParser, 'sheet{}'.format(self.nb_sheets), self._file_content[sheet])

    def read_file_header(self, sheet_name) -> list:
        assert sheet_name in list(self._file_content.keys())
        header = []
        for i, row in zip(range(self._header_length), self._file_content[sheet_name]):
            header.append(row)
        return header

    @property
    def get_file_content(self):
        return self._file_content


class XMLFileParser(AbstractFileParser):
    def __init__(self, file_path: str = None, header_length: int = None,
                 encoding: str = 'iso-8859-1'):
        super().__init__(file_path, header_length)
        self._encoding = encoding
        self._file_content = ET.parse(open(
            self._file, encoding=self._encoding))

    def read_file(self):
        pass

    def read_file_header(self):
        pass

    @property
    def get_file_content(self) -> bs4.BeautifulSoup:
        return self._file_content

    @property
    def get_file_header(self):
        return self._file_header_content


class WEBFileParser(AbstractFileParser):
    def __init__(self, file_path: str = None, header_length: int = None, requests_params: dict = None):
        super().__init__(file_path, header_length)
        if 'http' in self._file:
            self.web_url = requests.get(self._file, params=requests_params)
            self._file_content = bs4.BeautifulSoup(self.web_url.text, "html.parser")
        else:
            raise AttributeError('error in file parsing')

    def read_file(self):
        pass

    def read_file_header(self):
        pass

    @property
    def get_file_content(self) -> bs4.BeautifulSoup:
        return self._file_content

    @property
    def get_file_header(self):
        return self._file_header_content

    @get_file_header.setter
    def get_file_header(self, value):
        self._file_header_content = value


if __name__ == '__main__':
    from os import path

    exemple_file_path = "C:\\Users\\laptop\\Documents\\Programmation\\scientific_file_reader\\file_example"

    # EXEMPLE AVEC UN CSV FILE
    # cs_file = CSVFileParser(path.join(exemple_file_path,"F21_logger_20160224_20160621.csv"))
    # print(cs_file.get_file_header)
    # cs_file.read_file()
    # print(cs_file.get_file_content)

    # EXEMPLE AVEC UN TXT FILE
    # txt_file = TXTFileParser(path.join(exemple_file_path,"F2_20160223.lev"))
    # txt_file.read_file()
    # print(txt_file.get_file_content)
    # for row in txt_file.get_file_content:
    #     print(row)

    # EXEMPLE AVEC UN XLS
    xls_file_name = "B653824V1-R2016-08-18_16-31-39_N001.xls"
    xls_file = EXCELFileParser(path.join(exemple_file_path, xls_file_name), header_length=11)
    xls_file.read_file()

    i = 0
    sheet_name = list(xls_file.get_file_content.keys())[0]
    for row in xls_file.read_file_header(sheet_name):
        print(row)

        # EXEMPLE AVEC UN FICHIER XLSX
        # xlsx_file_name = "maxxam_sheet.xlsx"
        # xlsx_file = EXCELFileParser(path.join(exemple_file_path,xlsx_file_name))
        # xlsx_file.read_file()
        # j=0
        # for row in xlsx_file.sheet1:
        #     j+=1
        #     print(row)
        #     if j>10:
        #         break
