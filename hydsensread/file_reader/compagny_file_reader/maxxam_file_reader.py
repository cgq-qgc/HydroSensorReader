#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-16$'
__description__ = " "
__version__ = '1.0'

import datetime
import re
import warnings

from hydsensread.file_reader.abstract_file_reader import GeochemistryFileReader, Sample


class XSLMaxxamFileReader(GeochemistryFileReader):
    IGNORE_CONTENT = ["LDR = Limite de détection rapportée",
                      "Lot CQ = Lot contrôle qualité",
                      "N/A = Non Applicable",
                      "Les résultats ne se rapportent qu’aux échantillons soumis pour analyse",
                      "Duplicata de laboratoire"]

    def __init__(self, file_path: str = None, header_length: int = 12):
        super().__init__(file_path, header_length)
        self.maxxam_file = None
        self.command_number = None
        assert self.file_extension in self.XLS_FILES_TYPES, "Bad file type"
        self._unit_column_index = 1
        self._detection_limit_column_index = 0
        self._first_sample_column_index = 2
        self._sample_name_row_index = 0
        self.analysis_methode = []

    def _read_file_header(self):
        """
        implementation of the base class abstract method
        """
        self._get_analysis_type()

    def _read_file_data(self):
        """
        implementation of the base class abstract method
        """
        for sheets in self.get_results_sheet():
            self._update_sheet_data(sheets)
            self._enter_results(sheets)

    def _read_file_data_header(self):
        """
        implementation of the base class abstract method
        """
        for sheets in self.get_results_sheet():
            self._update_sheet_data(sheets)
            self._create_samples_sites(sheets)

    def _update_sheet_data(self, sheet_name):
        self._update_data_header_indexes(sheet_name)
        self._get_report_date(sheet_name)

    def get_results_sheet(self):
        return [sheet for sheet in self.file_content.keys() if re.search(r"result.*", sheet.lower())]

    def create_analysis_for_sample(self, sample_name: str,
                                   analysis_type: str,
                                   sampling_date: datetime.datetime,
                                   maxxam_name: str,
                                   samp_type: str = None):

        sample = Sample(site_name=sample_name,
                        visit_date=sampling_date,
                        lab_sample_name=maxxam_name,
                        sample_type=samp_type,
                        analysis_type=analysis_type, project_name=self.project)

        self._site_of_interest[sample_name][analysis_type] = sample

    def _add_analysis_type_in_txt_database(self, analysis_type: str):
        try:
            with open('maxxam_analysis_type.txt', 'r+', encoding='utf-8') as _file:
                in_file = False
                for line in _file:
                    if analysis_type in line:
                        in_file = True
                        break
                if in_file == False and analysis_type not in self.IGNORE_CONTENT:
                    _file.writelines(analysis_type + "\n")
        except FileNotFoundError:
            f = open('maxxam_analysis_type.txt', 'w')
            f.close()
            self._add_analysis_type_in_txt_database(analysis_type)

    def _get_analysis_type(self):
        for result_sheets in self.get_results_sheet():
            for row in self.file_content[result_sheets][11:]:
                if type(row[0]) == str and \
                                row[1:] == [None for i in range(len(row) - 1)]:
                    self._add_analysis_type_in_txt_database(row[0])
                    if row[0] not in self.IGNORE_CONTENT and row[0] not in self.analysis_methode:
                        self.analysis_methode.append(row[0])

    def _get_report_date(self, sheet_name):
        for row in self.file_content[sheet_name][0:9]:
            cells_content = str(row[0]).lower()
            if re.search("date.*rapport.*", cells_content):
                report_date = cells_content.split(":")[1].replace(" ", "")
                self.report_date = datetime.datetime.strptime(report_date, "%Y/%m/%d")

    def _update_data_header_indexes(self, sheet_name):
        assert sheet_name in self.file_content
        for id, row in enumerate(self.file_content[sheet_name][0:12]):
            if type(row[1]) == str:
                for cell_num, cells in enumerate(row):
                    if re.search(r"[uU]nit.*", str(cells)):
                        self._sample_name_row_index = id
                        self._unit_column_index = cell_num
                    if re.search(r"(ldr|l.*d.*r).*", str(cells).lower()):
                        self._detection_limit_column_index = cell_num
                        break

    def _create_samples_sites(self, sheet_name):
        # search for the current sheet
        for col_ind, cells in enumerate(
                self.file_content[sheet_name][self._sample_name_row_index]):
            cells_content = str(cells).lower()
            # line header indicates this column contain quality Control samples name
            if re.search(r"lot.*[cq]{2}.*", cells_content):
                # Ligne enlevé le 2017-07-20 car G.Bordeleau a dit que ce n'était pas nécessaire dans une BD.
                # L'information présenté par les QAQC n'est pas quelque chose d'important car on estime que le
                # lab sait ce qu'il fait!
                # self._add_lot_qc_sample(sheet_name, col_ind)
                pass
            # else, treat header as a sample name
            elif not re.search(r"(ldr|lot.*|unit.*|none)", cells_content):
                samp_type = 'echantillon'
                sampling_date = self.file_content[sheet_name][self._sample_name_row_index - 2][col_ind]
                maxxam_name = self.file_content[sheet_name][self._sample_name_row_index - 3][col_ind]
                # Internal maxxam duplicate
                if re.search(r".*dup.*de.*lab.*", cells_content):
                    samp_type = 'dup de laboratoire'
                # for the current sheet, take the analysis method used for the samples
                for row in self.file_content[sheet_name][self._sample_name_row_index + 1:]:
                    if row[0] in self.analysis_methode:
                        self.create_analysis_for_sample(sample_name=cells,
                                                        analysis_type=row[0],
                                                        sampling_date=sampling_date,
                                                        maxxam_name=maxxam_name, samp_type=samp_type)

    def _enter_results(self, sheet_name):
        # pour chaque échantillon créé
        for samp in list(self._site_of_interest.keys()):
            samp_col_index = self._get_sample_column_index(sheet_name, samp)
            ana_type = None
            # pour chaque feuilles de résultats
            for row in self.file_content[sheet_name][self._sample_name_row_index + 1:]:
                # la ligne est l'entête du type d'analyse
                if row[0] in self.analysis_methode:
                    ana_type = row[0]
                # c'est la fin
                elif row[0] is None and row[1] is None:
                    break
                # ce sont des résultats
                else:
                    # the sample is present in the current sheet
                    if samp_col_index is not None:
                        parameter = row[0]
                        param_unit = row[self._unit_column_index]
                        detect_limit = row[self._detection_limit_column_index]
                        value = row[samp_col_index]
                        sampling_date = self.get_sample_object_by_name_and_analysis(samp, ana_type).visit_date
                        report_date = self.report_date
                        self.get_sample_object_by_name_and_analysis(samp, ana_type). \
                            create_complete_record(sampling_date, parameter, param_unit, value, detect_limit,
                                                   report_date, ana_type)

    def get_sample_object_by_name_and_analysis(self, sample_name, ana_method) -> Sample:
        return self._site_of_interest[sample_name][ana_method]

    def _get_sample_column_index(self, sheet_name, samp_name) ->int:
        for col, cells in enumerate(self.file_content[sheet_name][self._sample_name_row_index]):
            if cells == samp_name:
                return col

    def _add_lot_qc_sample(self, sheet_name, column_index):
        """
        deprecated method left because it can be usefull...
        It was supposed to make an entry in the _sites_of_interest dict for the quality control samples made by
        the lab.
        :param sheet_name:
        :param column_index:
        :return:
        """
        warnings.warn('deprecated',DeprecationWarning)
        # for each row for the column at column_index, create a sample for the quality control made by maxxam.
        for lines in self.file_content[sheet_name][self._sample_name_row_index:]:
            if lines[column_index] is not None and not re.search('lot.*cq.*', lines[column_index].lower()):
                self.create_complete_sample(site_name=lines[column_index],
                                            visit_date=self.report_date, sample_type='lot qc',
                                            lab_sample_name='maxxam', project_name=self.project)


if __name__ == '__main__':
    import os

    path = os.getcwd()
    while os.path.split(path)[1] != "hydsensread":
        path = os.path.split(path)[0]
    file_loc = os.path.join(path, 'file_example')

    # file_name = "B656097V1-R2016-08-31_16-20-01_N001.xls"
    file_name = "B653824V1-R2016-08-18_16-31-39_N001.xls"

    max_file = XSLMaxxamFileReader(file_path=os.path.join(file_loc, file_name))
    max_file.read_file()
    for samp in list(max_file.sites.keys()):
        print(samp)
        try:
            for samp_method in list(max_file.sites[samp].keys()):
                print("\t" + samp_method)

                for records in max_file.get_sample_object_by_name_and_analysis(samp, samp_method).records:
                    print("\t\t" + str(records))
                    print("\t\t\trecord report date: " + str(records.report_date))
                    print("\t\t\t\tanalysis delay: " + str(records.report_date - records.record_date))
        except Exception as e:
            print(str(e))
