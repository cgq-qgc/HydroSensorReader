#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-11-09'
__description__ = " "
__version__ = '1.0'

import bs4

from file_reader.abstract_file_reader import DrillingFileReader, AbstractFileReader

GNB_MAIN_SEARCH_URL = "http://www1.gnb.ca/0078/geosciencedatabase/core/"
GNB_MAIN_CORE_URL = "http://dnr-mrn.gnb.ca/ParisWeb/"

# Must add a parameter to the research as
# param_request = {'NTS1':'21H', 'NTS2'='12'}
GNB_WEBSITE_MAP_SEARCH_URL = GNB_MAIN_SEARCH_URL + "search.asp"
# Must add a parameter to the research as
# param_request = {'Num':xxxx} where xxxx is a Assessment Number from GNB_WEBSITE_MAP_SEARCH_URL
GNB_CORE_SAMPLE_REPORT_URL = GNB_MAIN_CORE_URL + "Assessmentreportdetails.aspx"

# Must add a parameter to the research as
# param_request = {'Num':xxxx} where xxxx is a Assessment Number from GNB_WEBSITE_MAP_SEARCH_URL
# This url give access to files stored in the web site.
GNB_CORE_FILES_REPORT_URL = GNB_MAIN_CORE_URL + "PDFView.aspx"

# Files found at the GNB_CORE_FILES_REPORT_URL have an id and must be provided to the request as
# param_request = {'Id': 'id-present-in-the-html-page'}
GNB_FILES_DOWNLOADER = GNB_MAIN_CORE_URL + "StreamFile.aspx"


class GNBDrillCoreDatabaseWebScrapper(AbstractFileReader):
    """
    This class must look at samples available inside a requested NTS sheet located in the tab <map name="FPMap0">
    from the GNB_WEBSITE_MAP_SEARCH_URL
    """

    def __init__(self, request_params: dict = None, file_name: str = GNB_WEBSITE_MAP_SEARCH_URL,
                 header_length: int = 10):
        super().__init__(file_name=file_name, header_length=header_length, request_params=request_params)
        self.read_file()

    def _read_file_data_header(self):
        pass

    def _read_file_header(self):
        pass

    def _read_file_data(self):
        for elt in self.file_content.find('map'):
            if isinstance(elt, bs4.Tag):
                print(GNB_MAIN_SEARCH_URL + elt['href'])
                # TODO : Add the GNBCoreSamplesWebScrapper here


class GNBCoreSamplesWebScrapper(DrillingFileReader):
    """
    This class is going to pump all data available in the GNB_MAIN_SEARCH_URL + NTS sheet search from
    the GNBDrillCoreDatabaseWebScrapper class and go through the <table id="results"> tag.
    >>2nd row is for table header

    """
    def __init__(self, request_params: dict, file_name: str = GNB_CORE_SAMPLE_REPORT_URL,
                 header_length: int = None, ):
        super().__init__(file_name=file_name, header_length=header_length, request_params=request_params)

    def _read_file_data_header(self):
        super()._read_file_data_header()
        # read 2nd row of table

    def _read_file_data(self):
        """
        for each row:
            create input in dict
                key = identification [col 0] and hole ref [col 1]
                value = dict
        :return:
        """
        super()._read_file_data()


class GNBCoresFilesWebScrapper(AbstractFileReader):
    pass


if __name__ == '__main__':
    GNBDrillCoreDatabaseWebScrapper()
