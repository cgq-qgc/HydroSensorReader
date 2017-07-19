#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = " "
__version__ = '1.0'

import re

from sensor_file.domain.site import Sample
from sensor_file.file_reader.abstract_file_reader import GeochemistryFileReader
import datetime

class XSLMaxxamFileReader(GeochemistryFileReader):
    IGNORE_CONTENT = ["LDR = Limite de détection rapportée",
                      "Lot CQ = Lot contrôle qualité",
                      "N/A = Non Applicable",
                      "Les résultats ne se rapportent qu’aux échantillons soumis pour analyse",
                      "Duplicata de laboratoire"]

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
        self.get_analysis_type()


    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        pass

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        for sheets in self.get_results_sheet():
            self._update_sample_name_row_index(sheets)
            self._create_samples_sites(sheets)

    def get_results_sheet(self):
        return [sheet for sheet in self.file_content.keys() if re.search(r"result.*", sheet.lower())]

    def create_analysis_for_sample(self, sample_name:str,
                                   analysis_type:str,
                                   sampling_date:datetime.datetime,
                                   maxxam_name:str,
                                   samp_type:str=None):

        sample = Sample(site_name=sample_name,
                        visit_date=sampling_date,
                        lab_sample_name=maxxam_name,
                        sample_type=samp_type,
                        analysis_type=analysis_type, project_name=self.project)

        self._site_of_interest[sample_name][analysis_type] = sample

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


    def _update_sample_name_row_index(self, sheet_name):
        assert sheet_name in self.file_content
        for id, row in enumerate(self.file_content[sheet_name][0:12]):
            if type(row[1]) == str and re.search(r"[uU]nit.*", str(row[1])):
                self._sample_name_row_index = id

    def _create_samples_sites(self, sheet_name):
        # search for the current sheet
        for col_ind, cells in enumerate(
                self.file_content[sheet_name][self._sample_name_row_index]):
            cells_content = str(cells).lower()
            # line header indicates this column contain quality Control samples name
            if re.search(r"lot.*[cq]{2}.*", cells_content):
                self._add_lot_qc_sample(sheet_name, col_ind)
            # else, treat header as a sample name
            elif not re.search(r"(ldr|lot.*|unit.*|none)",cells_content):
                samp_type = 'ech'
                sampling_date = self.file_content[sheet_name][self._sample_name_row_index-2][col_ind]
                maxxam_name = self.file_content[sheet_name][self._sample_name_row_index-3][col_ind]
                # Internal maxxam duplicate
                if re.search(r".*dup.*de.*lab.*",cells_content):
                    samp_type = 'dup de laboratoire'
                # for the current sheet, take the analysis method used for the samples
                for row in self.file_content[sheet_name][self._sample_name_row_index+1:]:
                    if row[0] in self.analysis_methode:
                        self.create_analysis_for_sample(sample_name=cells ,
                                                        analysis_type=row[0] ,
                                                        sampling_date=sampling_date,
                                                        maxxam_name=maxxam_name ,samp_type=samp_type)


    def _add_lot_qc_sample(self, sheet_name, column_index):
        # for each row for the column at column_index, create a sample for the quality control made by maxxam.
        for lines in self.file_content[sheet_name][self._sample_name_row_index:]:
            if lines[column_index] is not None and not re.search('lot.*cq.*',lines[column_index].lower()):
                self.create_complete_sample(site_name=lines[column_index],
                                            visit_date=self.report_date,sample_type='lot qc',
                                            lab_sample_name='maxxam', project_name=self.project)


if __name__ == '__main__':
    import os

    file_loc = os.path.join(os.path.split(os.path.split(os.getcwd())[0])[0], 'file_example')
    print(file_loc)
    # file_name = "B656097V1-R2016-08-31_16-20-01_N001.xls"
    file_name = "B653824V1-R2016-08-18_16-31-39_N001.xls"

    max_file = XSLMaxxamFileReader(file_name=os.path.join(file_loc, file_name))
    max_file.read_file()
    for samp in list(max_file.sites.keys()):
        print("--"+samp)
        try:
            print(list(max_file.sites[samp].keys()))
        except:
            pass
    # for result_sheets in max_file.get_results_sheet():
    #     for row in max_file.file_reader.read_file_header(result_sheets):
    #         print([None for i in range(len(row)-1)])
    #         print(type(row[0]) == str and row[1:] == [None for i in range(len(row)-1)])
    #         print(list(row))
    #     break
