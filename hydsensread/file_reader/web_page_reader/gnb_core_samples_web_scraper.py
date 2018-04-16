#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xmalet'
__date__ = '2017-11-09'
__description__ = " "
__version__ = '1.0'

import pprint
import re
import typing
from collections import defaultdict

import bs4

from hydsensread.file_reader.abstract_file_reader import DrillingFileReader, AbstractFileReader
from hydsensread.site_and_records import DrillingSite

_GNB_MAIN_SEARCH_URL = "http://www1.gnb.ca/0078/geosciencedatabase/"
_GNB_CORE_EXT = "core/"
_GNB_SEARCH_EXT = "search.asp"
_GNB_RESULTS_EXT = "Results-e.asp"
# -------------------- FOR CORE SAMPLES --------------
# Must add a parameter to the research as
# param_request = {'NTS1':'21H', 'NTS2'='12'}
_GNB_CORE_SAMPLES_MAIN_URL = _GNB_MAIN_SEARCH_URL + _GNB_CORE_EXT
GNB_CORE_SAMPLES_NTS_MAP_SEARCH_URL = _GNB_CORE_SAMPLES_MAIN_URL + _GNB_SEARCH_EXT
GNB_CORE_SAMPLES_LIST_URL = _GNB_CORE_SAMPLES_MAIN_URL + _GNB_RESULTS_EXT
# Must add a parameter to the research as
# param_request = {'Num':xxxx} where xxxx is a Assessment Number from GNB_WEBSITE_MAP_SEARCH_URL
# --------- CORE SAMPLES DATASHEET URL --------------
_GNB_MAIN_PUBLICATION_URL = "http://dnr-mrn.gnb.ca/ParisWeb/"
# GNB_CORE_SAMPLE_REPORT_URL
# Must add a parameter to the research URL GNB_CORE_SAMPLE_REPORT_URL as
# param_request = {'Num':xxxx} where xxxx is a Assessment Number from GNB_WEBSITE_MAP_SEARCH_URL
# This url give access to files stored in the web site.
GNB_CORE_SAMPLE_REPORT_URL = _GNB_MAIN_PUBLICATION_URL + "Assessmentreportdetails.aspx"
# GNB_CORE_FILES_REPORT_URL
# Files found at the GNB_CORE_FILES_REPORT_URL and GNB_FILES_DOWNLOADER  have an id and must be provided to the request as
# param_request = {'Id': 'id-present-in-the-html-page'}
GNB_CORE_FILES_REPORT_URL = _GNB_MAIN_PUBLICATION_URL + "PDFView.aspx"
GNB_FILES_DOWNLOADER = _GNB_MAIN_PUBLICATION_URL + "StreamFile.aspx"
# -------------------- END CORE SAMPLES URL ------------------

_GNB_OIL_GAS_MAIN_URL = _GNB_MAIN_SEARCH_URL + "borehole/"
GNB_OIL_GAS_NTS_MAP_SEARCH_URL = _GNB_OIL_GAS_MAIN_URL + _GNB_SEARCH_EXT
GNB_OIL_GAS_LIST_URL = _GNB_OIL_GAS_MAIN_URL + _GNB_RESULTS_EXT
# GNB_BOREHOLE_DETAIL_URL
# Must add a parameter to the research URL GNB_BOREHOLE_DETAIL_URL as
# param_request = {'UIN':xx} where xxxx is a UIN found at the GNB_OIL_GAS_LIST_URL
GNB_BOREHOLE_DETAIL_URL = _GNB_OIL_GAS_MAIN_URL + "Detail-e.asp"

from threading import Thread

GENERAL_INFO = 'general_info'
LOCATION = 'location'
WORK_PERFOMED = 'work_performed'
MAP_AVAILABLE = 'maps_available'


class _scrapper(Thread):
    """
    factory thread class to scrappe faster!
    """

    def __init__(self, factory_class, req_params):
        Thread.__init__(self)
        self.fact_class = factory_class
        self.req_params = req_params
        self.factory = None

    def run(self):
        print("run element")
        self.factory = self.fact_class(request_params=self.req_params)


class GNBCoreSamplesDataFactory(DrillingFileReader):
    def __init__(self, request_params: dict = None):
        self._site_of_interest = DrillingSite()
        self._content = {}
        if request_params['Num'] != '':
            super().__init__(file_path=GNB_CORE_SAMPLE_REPORT_URL, request_params=request_params, header_length=0)
            self.read_file()

    def _read_table_first_col_is_header(self, table_id) -> dict:
        r_dict = {}
        table = self.file_content.find(id=table_id)
        for rows in table.find_all('tr', ):
            cols = rows.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            r_dict[cols[0]] = cols[1]
        return r_dict

    def _read_file_header(self):
        pass

    def _read_file_data_header(self):
        pass

    def _read_file_data(self):
        self._read_general_information()
        self._read_location()
        self._read_work_performed()
        self._read_map_info()

    def _read_general_information(self):
        # table id = dlAssRptGeneral
        self._content[GENERAL_INFO] = self._read_table_first_col_is_header('dlAssRptGeneral')

    def _read_location(self):
        # table id = dlAssRptLocation
        self._content[LOCATION] = self._read_table_first_col_is_header('dlAssRptLocation')

    def _read_work_performed(self):
        # table id = dlAssRptWorkPerformed
        self._content[WORK_PERFOMED] = self._read_table_first_col_is_header('dlAssRptWorkPerformed')

    def _read_map_info(self):
        # table id = dgAssRptMaps
        r_dict = {}
        table = self.file_content.find(id='dgAssRptMaps')
        header_data = []
        for i, rows in enumerate(table.find_all('tr')):
            cols = rows.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if i == 0:
                header_data = cols
            else:
                r_dict['file-{}'.format(i)] = dict((k, v) for (k, v) in zip(header_data, cols))
        self._content[MAP_AVAILABLE] = r_dict

    def get_url_content(self) -> dict:
        return self._content


class AbstractGNBElementListWebScrapper(DrillingFileReader):
    def __init__(self, request_params: dict, file_path: str,
                 header_length: int = None, ):
        super().__init__(file_path=file_path, header_length=header_length, request_params=request_params)
        self._site_of_interest = defaultdict(dict)
        self._threads = {}
        self.read_file()

    def _read_file_data_header(self):
        """
        Get the table header
        :return:
        """
        print("Scrapping url")
        print(self.file_reader.web_url.url)

        for rows in self.file_content.find_all('tr'):
            cols = rows.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) > 1:
                self.file_reader.get_file_header = cols

    def _read_file_header(self):
        pass

    def __str__(self) -> str:
        return super().__str__() + " contains {}".format(len(self._site_of_interest))

    def get_sample_list(self):
        return self._site_of_interest.values()


class GNBCoreSamplesListWebScrapper(AbstractGNBElementListWebScrapper):
    """
    This class is going to pump all data available in the GNB_MAIN_SEARCH_URL + NTS sheet search from
    the GNBDrillCoreDatabaseWebScrapper class and go through the <table id="results"> tag.
    >>2nd row is for table header

    """

    def __init__(self, request_params: dict, file_path: str = GNB_CORE_SAMPLES_LIST_URL,
                 header_length: int = None, ):
        super().__init__(file_path=file_path, header_length=header_length, request_params=request_params)

    def _read_file_data(self):
        print("Getting data")
        for rows in self.file_content.find_all('tr'):
            cols = rows.find_all('td')
            try:
                cols = [ele.text.strip().replace('No Data', '') for ele in cols]
                dict_content = dict((k, v) for (k, v) in zip(self.file_reader.get_file_header, cols))
                if dict_content['Assessment #'] != '':
                    print("Pumping {} sample".format(dict_content['Identification #']))
                    elt = _scrapper(GNBCoreSamplesDataFactory, {'Num': dict_content['Assessment #']})
                    elt.start()
                    self._threads[dict_content['Identification #'] + "_" + dict_content['Hole Reference #']] = elt
                self._site_of_interest[
                    dict_content['Identification #'] + "_" + dict_content['Hole Reference #']] = dict_content
            except KeyError:
                pass
            except TypeError as t:
                raise t
        for t in self._threads.keys():
            self._threads[t].join()
            self._site_of_interest[t]['core_sample_data'] = self._threads[t].factory

    def __str__(self) -> str:
        return super().__str__() + " core samples"


class GNBOilAndGasWellsListWebScrapper(AbstractGNBElementListWebScrapper):
    def __init__(self, request_params: dict, file_path: str = GNB_OIL_GAS_LIST_URL, header_length: int = None):
        super().__init__(file_path=file_path, header_length=header_length, request_params=request_params)

    def _read_file_data(self):
        print("Getting data")
        for rows in self.file_content.find_all('tr'):
            cols = rows.find_all('td')
            try:
                cols = [ele.text.strip().replace('No Data', '') for ele in cols]
                dict_content = dict((k, v) for (k, v) in zip(self.file_reader.get_file_header, cols))
                self._site_of_interest[
                    dict_content['UIN']] = dict_content
            except KeyError:
                pass

    def __str__(self) -> str:
        return super().__str__() + " oil and gas boreholes"


gnb_element_list_web_scrapper = typing.Union[GNBOilAndGasWellsListWebScrapper, GNBCoreSamplesListWebScrapper]


class Abstract_GNB_NTSMapSearchWebScrapper(AbstractFileReader):
    """
    This class must look at samples available inside a requested NTS sheet located in the tab <map name="FPMap0">
    from the GNB_WEBSITE_MAP_SEARCH_URL
    """

    def __init__(self, file_path: str,
                 factory_class: gnb_element_list_web_scrapper,
                 ):
        super().__init__(file_path=file_path, header_length=0, request_params=None)

        self.factory_class = factory_class
        self._site_of_interest = dict()
        self._thread_scrapper = {}
        self.read_file()

    def _read_file_data_header(self):
        pass

    def _read_file_header(self):
        pass

    def _read_file_data(self):
        for elt in self.file_content.find('map'):
            if isinstance(elt, bs4.Tag):
                url_params = re.split(r"[?&=]", elt['href'])
                request_param = {url_params[1]: url_params[2], url_params[3]: url_params[4]}
                nts_sheet = "{}{}".format(url_params[2], url_params[4])
                # , '21H10', '21H14'
                elt = _scrapper(self.factory_class, req_params=request_param)
                if nts_sheet in ['21H11', '21H10', '21H14'] \
                        and nts_sheet not in self._site_of_interest.keys():
                    self._site_of_interest[nts_sheet] = ""
                    self._thread_scrapper[nts_sheet] = elt
                    self._thread_scrapper[nts_sheet].start()
        for ntf_values in self._thread_scrapper.keys():
            self._thread_scrapper[ntf_values].join()
            self._site_of_interest[ntf_values] = self._thread_scrapper[ntf_values].factory

        print(self._site_of_interest.items())

    @property
    def sites(self) -> typing.Dict[str, gnb_element_list_web_scrapper]:
        return self._site_of_interest


class GNBCoreSamplesNTSMapSearchWebScrapper(Abstract_GNB_NTSMapSearchWebScrapper):
    def __init__(self, file_path: str = GNB_CORE_SAMPLES_NTS_MAP_SEARCH_URL,
                 factory_class=GNBCoreSamplesListWebScrapper):
        super().__init__(file_path=file_path, factory_class=factory_class)

    def write_file(self):
        # with open('samples_location.csv','w'):
        for samp_list in self._site_of_interest.values():
            for cores in samp_list.get_sample_list():
                print("=" * 50)
                pprint.pprint(cores)
                try:
                    print("-" * 50)
                    pprint.pprint(cores['core_sample_data'].get_url_content())
                except KeyError:
                    pass


class GNBOilAndGasNTSMapSearchWebScrapper(Abstract_GNB_NTSMapSearchWebScrapper):
    def __init__(self, file_path: str = GNB_OIL_GAS_NTS_MAP_SEARCH_URL,
                 factory_class=GNBOilAndGasWellsListWebScrapper):
        super().__init__(file_path=file_path, factory_class=factory_class)


if __name__ == '__main__':
    # drill_cores = GNB_CoreSamples_NTSMapSearchWebScrapper()
    # drill_cores.write_file()
    boreholes = GNBOilAndGasNTSMapSearchWebScrapper()
    # GNBCoreSamplesWebScrapper(request_params={'NTS1': '21B', 'NTS2': '15'})
