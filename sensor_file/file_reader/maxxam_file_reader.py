#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = " "
__version__ = '1.0'

from sensor_file.file_reader.abstract_file_reader import GeochemistryFileReader

import re


class XSLMaxxamFileReader(GeochemistryFileReader):
    IGNORE_CONTENT = ["LDR = Limite de détection rapportée",
                      "Lot CQ = Lot contrôle qualité",
                      "N/A = Non Applicable",
                      "Les résultats ne se rapportent qu’aux échantillons soumis pour analyse"]

    def __init__(self, file_name: str = None, header_length: int = 12):
        super().__init__(file_name, header_length)
        self.maxxam_file = None
        self.command_number = None
        assert self.file_extension in self.XLS_FILES_TYPES, "Bad file type"
        self._unit_column_index = 1
        self._first_sample_column_index = 2
        self._sample_name_row_index = 0
        self.analysis_methode = []

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

    def get_results_sheet(self):
        return [sheet for sheet in self.file_content.keys() if re.search(r"result.*", sheet.lower())]

    def _add_analysis_type_in_txt_database(self, analysis_type):
        with open('maxxam_analysis_type.txt', 'r+', encoding='utf-8') as _file:
            in_file = False
            for line in _file:
                if analysis_type in line:
                    in_file = True
                    break
            if in_file == False and analysis_type not in self.IGNORE_CONTENT:
                _file.writelines(analysis_type + "\n")

    def get_analysis_type(self):
        for result_sheets in self.get_results_sheet():
            for row in self.file_content[result_sheets][11:]:
                if type(row[0]) == str and \
                                row[1:] == [None for i in range(len(row) - 1)]:
                    self._add_analysis_type_in_txt_database(row[0])
                    if row[0] not in self.IGNORE_CONTENT and row[0] not in self.analysis_methode:
                        self.analysis_methode.append(row[0])
        self._update_sample_name_row_index('Result (1)')
        return self.analysis_methode

    def _update_sample_name_row_index(self, sheet_name):
        assert sheet_name in self.file_content
        for id,row in enumerate(self.file_content[sheet_name][0:11]):
            print("{} {}".format(id,row))
            if type(row[1]) == str and re.search(r"unit.*",str(row[1]).lower()):
                self._sample_name_row_index = id


if __name__ == '__main__':
    import os

    file_loc = "C:\\Users\\laptop\\Documents\\Programmation\\scientific_file_reader\\file_example"
    file_name = "B656097V1-R2016-08-31_16-20-01_N001.xls"

    max_file = XSLMaxxamFileReader(file_name=os.path.join(file_loc, file_name))
    print(max_file.file_content)
    print(max_file.get_analysis_type())
    # for result_sheets in max_file.get_results_sheet():
    #     for row in max_file.file_reader.read_file_header(result_sheets):
    #         print([None for i in range(len(row)-1)])
    #         print(type(row[0]) == str and row[1:] == [None for i in range(len(row)-1)])
    #         print(list(row))
    #     break
