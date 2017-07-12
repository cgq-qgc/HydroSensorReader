#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-11$'
__description__ = " "
__version__ = '1.0'


from sensor_file.file_reader.file_parser.abstract_file_parser import AbstractFileParser
import csv
import xlrd
import openpyxl
import warnings
import re
from collections import defaultdict


class CSVFileParser(AbstractFileParser):

    def __init__(self, file_path: str = None, header_length:int = 10):
        super().__init__(file_path, header_length)

        self.read_file_header()

    def read_file(self):
        with open(self._file, 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            file_reader = csv.reader(csvfile,dialect=dialect)
            for row in file_reader:
                self._file_content.append(row)

    def read_file_header(self):
        try:
            if not re.search(r"csv",self._file[-4:].lower()):
                raise TypeError("Bad file type")
            with open(self._file, 'r') as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read())
                csvfile.seek(0)
                file_reader = csv.reader(csvfile,dialect=dialect)
                for i,row in enumerate(file_reader):
                    self._file_header_content.append(row)

                    if i > self._header_length:
                        break
        except TypeError as e :
            warnings.warn("Error occured when trying to read the current file {}".format(self._file))

class TXTFileParser(AbstractFileParser):
    def __init__(self, file_path: str = None, header_length: int = 20):
        super().__init__(file_path, header_length)
        self.read_file_header()


    def read_file(self):
        with open(self._file, 'r') as txt_file:
            self._file_content = [line.replace('\n', '') for  line in txt_file.readlines()]

    def read_file_header(self):
        try:
            if re.search(r"csv|xl.*",self._file[-4:].lower()):
                raise TypeError("Bad file type")
            with open(self._file,'r') as txt_file:
                self._file_header_content = [line.replace('\n','')
                                             for i, line in enumerate(txt_file.readlines())
                                             if i < self._header_length]
        except TypeError as e :
            warnings.warn("Error occured when trying to read the current file {}".format(self._file))


class EXCELFileParser(AbstractFileParser):
    def __init__(self, file_path: str = None, header_length: int = None):
        super().__init__(file_path, header_length)
        self._file_content = defaultdict(list)
        self._file_header_content = {}
        self.nb_sheets = 0
    def read_file(self):
        try:
            assert re.search(r".*xl.*",self._file)
            if re.search(r".*xls$",self._file):
                self.__read_xls_file()
            elif re.search(r".*xlsx$",self._file):
                self.__read_xlsx_file()
            else:
                raise TypeError("Excel file not supported.")
        except AssertionError as e :
            warnings.warn("Error: Bad file extension. This is not an Excel file")
        except TypeError as t:
            warnings.warn("Error occured when trying to read the current file {}".format(self._file))

    def _get_file_content_by_sheet_name(self, sheet_name):
        return self._file_content[sheet_name]

    def __read_xls_file(self):

        file = xlrd.open_workbook(self._file)
        for sheets in file.sheet_names():
            self.nb_sheets += 1
            current_sheet = file.sheet_by_name(sheets)
            sheet_content = []
            for row in range(current_sheet.nrows):
                current_row = []
                for cells in current_sheet.row(row):
                    if cells.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                        current_row.append('')
                    else:
                        current_row.append(cells)
                sheet_content.append(current_row)
            self._file_content[sheets] = sheet_content
            setattr(EXCELFileParser, 'sheet{}'.format(self.nb_sheets), self._get_file_content_by_sheet_name(sheets))


    def __read_xlsx_file(self):
        print("read xlsx file")
        file = openpyxl.load_workbook(filename= self._file)


    def read_file_header(self):
        super().read_file_header()

    @property
    def get_file_content(self):
        return self._file_content


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
    # print(txt_file.get_file_header)
    # txt_file.read_file()
    # for row in txt_file.get_file_content:
    #     print(row)

    # EXEMPLE AVEC UN XLS et XLSX FILE
    file_name = "B653824V1-R2016-08-18_16-31-39_N001.xls"
    xls_file = EXCELFileParser(path.join(exemple_file_path,file_name))
    xls_file.read_file()
    print(xls_file.nb_sheets)
    for row in xls_file.sheet1:
        print(row)