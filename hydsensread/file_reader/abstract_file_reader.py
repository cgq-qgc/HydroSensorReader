#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import warnings
from abc import abstractmethod, ABCMeta
from collections import defaultdict
from typing import Dict, List, Union, Tuple
from xml.etree import ElementTree as ET

import bs4
import matplotlib.axes as mp_axe
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from pandas import DataFrame
from pandas.plotting import register_matplotlib_converters

from hydsensread import file_parser
from hydsensread.site_and_records import (
    DrillingSite, geographical_coordinates, Sample, SensorPlateform)

register_matplotlib_converters()
sample_ana_type = Dict[str, Sample]
sample_dict = Dict[str, sample_ana_type]
date_list = List[datetime.datetime]


class LineDefinition(object):
    """
    Line definition element to pass to the plot method
    """

    def __init__(self, parameter,
                 color: str = 'blue',
                 linestyle: str = '-',
                 outward: int = 0,
                 linewidth: float = 2,
                 make_grid: bool = False) -> None:
        self.param = parameter
        self.linestyle = linestyle
        self.color = color
        self.outward = outward
        self.linewidth = linewidth
        self.make_grid = make_grid


class AbstractFileReader(object, metaclass=ABCMeta):
    """
    Interface permettant de lire un fichier provenant d'un datalogger
    quelconque classe permettant d'extraire des données d'un fichier
    quelconque.

    Un fichier de donnée est en général composé de :
    - Entete d'information sur l'environnement de prise de données
    - Entete d'information sur les colonnes de données
    - Les colonnes de données
    """
    TXT_FILE_TYPES = ['dat', 'lev', 'txt']
    XLS_FILES_TYPES = ['xls', 'xlsx']
    XML_FILES_TYPES = ['xle', 'xml']
    CSV_FILES_TYPES = ['csv']
    WEB_XML_FILES_TYPES = ['http']
    MONTH_S_DAY_S_YEAR_HMS_DATE_STRING_FORMAT = '%m/%d/%y %H:%M:%S'
    YEAR_S_MONTH_S_DAY_HM_DATE_STRING_FORMAT = '%Y/%m/%d %H:%M'
    YEAR_S_MONTH_S_DAY_HMS_DATE_STRING_FORMAT = (
        YEAR_S_MONTH_S_DAY_HM_DATE_STRING_FORMAT + ":%S")
    YEAR_S_MONTH_S_DAY_HMSMS_DATE_STRING_FORMAT = (
        YEAR_S_MONTH_S_DAY_HMS_DATE_STRING_FORMAT + ".%f")

    def __init__(self, file_path: str = None,
                 header_length: int = 10,
                 request_params: dict = None,
                 encoding='utf8',
                 wait_read=False,
                 csv_delim_regex: str = None):
        """
        :param file_path: path to the file to treat
        :param header_length: header length
        :param request_params: request parameter for web element
        :param encoding: encoding type :default = 'utf-8'
        :param wait_read: if wait_read is True, will wait to read the file
        content. This is usefull for hierarchi-class.
        :param csv_delim_regex: a regex used to determine the delimiter of
        csv files when parsing the data
        See file_reader.compagny_file_reader.solinst_file_reader.py
        for an example
        """
        self.request_params = request_params
        self._file = file_path
        self._header_length = header_length
        self._encoding = encoding
        self._csv_delim_regex = csv_delim_regex
        self._site_of_interest = None
        self.file_reader = self._set_file_reader()
        if not wait_read:
            self.file_reader.read_file()

    @property
    def sites(self):
        return self._site_of_interest

    def _set_file_reader(self) -> Union[file_parser.CSVFileParser,
                                        file_parser.EXCELFileParser,
                                        file_parser.TXTFileParser,
                                        file_parser.WEBFileParser]:
        """
        set the good file parser to open and read the provided file
        :return:
        """
        file_reader = ""
        file_ext = self.file_extension
        try:
            if file_ext in self.TXT_FILE_TYPES:
                file_reader = file_parser.TXTFileParser(
                    file_path=self._file,
                    header_length=self._header_length,
                    encoding=self._encoding)
            elif file_ext in self.XLS_FILES_TYPES:
                file_reader = file_parser.EXCELFileParser(
                    file_path=self._file,
                    header_length=self._header_length)
            elif file_ext in self.CSV_FILES_TYPES:
                file_reader = file_parser.CSVFileParser(
                    file_path=self._file,
                    header_length=self._header_length,
                    csv_delim_regex=self._csv_delim_regex)
            elif file_ext in self.WEB_XML_FILES_TYPES or 'http' in self._file:
                file_reader = file_parser.WEBFileParser(
                    file_path=self._file,
                    requests_params=self.request_params)
            elif file_ext in self.XML_FILES_TYPES:
                file_reader = file_parser.XMLFileParser(file_path=self._file)
        except ValueError as e:
            print(self._file)
            print("File ext: {}".format(file_ext))

            raise e
        else:
            return file_reader

    def read_file(self):
        self._make_site()
        self._make_data()

    @property
    def file_extension(self):
        file_list = self._file.split(".")
        if len(file_list) == 1:
            raise ValueError("The path given doesn't point to a file name")
        if len(file_list) > 2 and 'http' not in self._file:
            raise ValueError("The file name seems to be corrupted. "
                             "Too much file extension in the current name.")
        else:
            return file_list[-1].lower()

    @property
    def file_content(self) -> Union[ET.ElementTree, bs4.BeautifulSoup, list, ]:
        return self.file_reader.get_file_content

    def _make_site(self):
        """
        Create a site object by reading the file header and the data header
        to know what was recorded.
        """
        self._read_file_header()
        self._read_file_data_header()

    def _make_data(self):
        """Read and classify the data."""
        self._read_file_data()

    @abstractmethod
    def _read_file_header(self):
        """Read the file header."""
        pass

    @abstractmethod
    def _read_file_data_header(self):
        """Read the data header (what was recorded)."""
        pass

    @abstractmethod
    def _read_file_data(self):
        """Read and classify the data columns."""
        pass


class TimeSeriesFileReader(AbstractFileReader):
    def __init__(self, file_path: str = None, header_length: int = 10,
                 encoding='utf8', wait_read: bool = False,
                 csv_delim_regex: str = None):
        super().__init__(file_path, header_length, encoding=encoding,
                         wait_read=wait_read, csv_delim_regex=csv_delim_regex)
        self._site_of_interest = SensorPlateform()
        self._date_list = []
        self.header_content = {}
        if not wait_read:
            self.read_file()

    @property
    def time_series_dates(self):
        return self._date_list

    @abstractmethod
    def _get_date_list(self) -> date_list:
        pass

    @property
    def sites(self) -> SensorPlateform:
        return self._site_of_interest

    @property
    def records(self) -> DataFrame:
        return self.sites.records

    @records.setter
    def records(self, value: DataFrame):
        self._site_of_interest.records = value

    def plot(self, main_axis_def: LineDefinition, other_axis,
             legend_loc='upper left',
             *args, **kwargs) -> Tuple[plt.Figure, List[plt.Axes]]:
        """
        :param main_axis_def:
        :param other_axis:
        :param legend_loc:
        :param args:
        :param kwargs:
        :return:
        """
        fig, main_axis = plt.subplots(figsize=(20, 10))

        main_axis = self._add_first_axis(main_axis, main_axis_def)
        all_axis = [main_axis]
        for lines in other_axis:
            new_axis = self._add_axe_to_plot(main_axis, lines)
            all_axis.append(new_axis)

        self._set_date_time_plot_format(main_axis)

        fig.legend(loc=legend_loc)
        return fig, all_axis

    def remove_duplicates(self) -> DataFrame:
        self.records = self.records.drop_duplicates()
        return self.records

    def _add_axe_to_plot(self, parent_plot,
                         new_line_def: LineDefinition,
                         **kwargs) -> mp_axe.Axes:
        new_axis = parent_plot.twinx()
        new_axis.plot(self.records[new_line_def.param],
                      color=new_line_def.color, linestyle=new_line_def.linestyle,
                      linewidth=new_line_def.linewidth, **kwargs)
        new_axis.grid(new_line_def.make_grid)
        new_axis.set_ylabel(new_line_def.param, color=new_line_def.color)
        new_axis.spines["right"].set_color(new_line_def.color)
        if new_line_def.outward != 0:
            new_axis.spines["right"].set_position(
                ("outward", new_line_def.outward))

        return new_axis

    def _add_first_axis(self, main_axis: mp_axe.Axes,
                        line_def: LineDefinition, **kwargs) -> mp_axe.Axes:
        main_axis.plot(self.records[line_def.param],
                       color=line_def.color,
                       linestyle=line_def.linestyle,
                       linewidth=line_def.linewidth, **kwargs)
        main_axis.set_ylabel(line_def.param, color=line_def.color)
        main_axis.spines['left'].set_color(line_def.color)
        main_axis.set_title(self.sites.site_name +
                            " - Visit date: " +
                            str(self.sites.visit_date))
        main_axis.grid(line_def.make_grid)

        return main_axis

    @staticmethod
    def _set_date_time_plot_format(axis: mp_axe.Axes):
        myFmt = mdates.DateFormatter('(%Y-%m-%d) %H:%M')
        axis.xaxis.set_major_formatter(myFmt)
        axis.grid(True, axis='x')


class GeochemistryFileReader(AbstractFileReader):
    def __init__(self, file_path: str = None,
                 header_length: int = 10, **kwargs):
        super().__init__(file_path, header_length)
        self._site_of_interest = defaultdict(dict)  # dict of Samples
        self.project = None
        self.report_date = None
        self.analysis_methode = None

    def _read_file_header(self):
        pass

    def _read_file_data_header(self):
        pass

    def create_sample(self, sample_name: str):
        sample = Sample(site_name=sample_name)
        self._site_of_interest[sample_name] = sample
        yield self._site_of_interest[sample_name]

    def create_complete_sample(self, site_name: str = None,
                               visit_date: datetime.datetime = None,
                               lab_sample_name: str = None,
                               sample_type: str = None,
                               project_name: str = None):
        sample = Sample(site_name, visit_date, lab_sample_name, sample_type, project_name)
        self._site_of_interest[site_name] = sample


class TimeSeriesGeochemistryFileReader(TimeSeriesFileReader, GeochemistryFileReader):
    TIME_SERIES_DATA = 'timeSerie'
    GEOCHEMISTRY_DATA = 'samples'

    def __init__(self, file_path: str = None, header_length: int = 10, encoding='utf-8'):
        """
        class between TimeSeriesFileReader and GeochemistryFileReader.
        internal data structure is like:
        self._site_of_interest
            [TIMES_SERIES]
                [site_name]
                    SensorPlateform
            [GEOCHEMISTRY]
                [date : datetime.datetime]
                    [sample_name:str]
                        Sample
       """
        warnings.warn("""Deprecated class. 
                      Needs to be adapted to site.py and records.py refactoring 
                      Don't know if this class is still usefull if a pandas.Dataframe is used.
                      Maybe a MultiIndex can do the trick !
                      - 2018-04-03""", DeprecationWarning)
        # TimeSeriesFileReader.__init__(self, file_path, header_length, encoding=encoding)
        # GeochemistryFileReader.__init__(self, file_path, header_length)
        super().__init__(file_path, header_length, encoding=encoding)
        self._site_of_interest = defaultdict(dict)
        self._site_of_interest[self.TIME_SERIES_DATA] = defaultdict(SensorPlateform)
        self._site_of_interest[self.GEOCHEMISTRY_DATA] = defaultdict(dict)  # dict sorted by [samp_name][samp_date]

    def get_sample_by_date(self, p_date, p_samp_name) -> Sample:
        try:
            return self._site_of_interest[self.GEOCHEMISTRY_DATA][p_date][p_samp_name]
        except:
            return None

    def get_time_series_data(self, site_name=None) -> Union[SensorPlateform, dict]:
        """
        get all sites avaible that have a time serie OR
        get all timeseries for the given "site_name"
        with this structure:
        [TIMES_SERIES]
            [site_name]
                SensorPlateform
        :param site_name:
        :return:
        """
        if site_name is not None:
            return self._site_of_interest[self.TIME_SERIES_DATA][site_name]
        else:
            return self._site_of_interest[self.TIME_SERIES_DATA]

    def get_geochemistry_data(self) -> dict:
        """
        get the dictionnary for geochemistry in this structure:
        [GEOCHEMISTRY]
            [date : datetime.datetime]
                [sample_name:str]
                    Sample
        :return:
        """
        return self._site_of_interest[self.GEOCHEMISTRY_DATA]

    def _get_date_list(self, site_name) -> date_list:
        """
        get all dates for the given site_name. No matter the parameter
        :param site_name:
        :return:
        """
        return self.get_time_series_data(site_name).get_dates()

    @TimeSeriesFileReader.time_series_dates.getter
    def time_series_dates(self, site_name):
        """
        overide of time_series_dates property getter. Needs to have a site_name because of
        the dict structure
        :param site_name:
        :return:
        """
        self._date_list = self._get_date_list(site_name)
        return self._date_list

    def makes_samples_with_time_series(self, site_name):
        """
        make sample with all the time series for the given site_name
        :param site_name:
        :return:
        """
        sample_name = self.get_time_series_data(site_name).site_name
        project = self.get_time_series_data(site_name).project_name
        # iterate through all dates
        for dates in self._get_date_list(site_name):
            # create a sample
            samp = Sample(site_name=sample_name,
                          visit_date=dates,
                          lab_sample_name=None,
                          sample_type='automatic',
                          analysis_type=None,
                          project_name=project)
            # create and add a record to the sample
            for rec in self.get_time_series_data(site_name).get_records():
                val = rec.get_value_at_date(dates)
                param = rec.parameter
                unit = rec.parameter_unit
                if val is not None:
                    samp.create_complete_record(dates, param, unit, val, None, dates, None)
            # add the sample to the geochemistry datas
            self.get_geochemistry_data()[dates][sample_name] = samp

    def make_time_series_with_samples(self):
        """
        take all the samples in self._site_of_interest[self.GEOCHEMISTRY_DATA]
        and create a time serie for each record.
         After all timeseries are made, they are filled with all the sampling data
        :return:
        """
        self._site_of_interest[self.TIME_SERIES_DATA].clear()
        self._site_of_interest[self.TIME_SERIES_DATA] = defaultdict(SensorPlateform)
        self._create_time_series_with_samples()
        self._fill_time_series_with_samples_data()

    def _create_time_series_with_samples(self):
        """
        create time serie entry for each parameters available for each samples
        remember, geochemistry data structure is like:
        [GEOCHEMISTRY]
            [date : datetime.datetime]
                [sample_name:str]
                    Sample
        :return:
        """
        for sampled_dates in self.get_geochemistry_data().keys():
            for samples_at_date in self.get_geochemistry_data()[sampled_dates].keys():
                for records_in_sample in self.get_sample_by_date(sampled_dates, samples_at_date).get_records():
                    self._add_time_serie_value_by_geochemistry_record(records_in_sample, samples_at_date)

    def _add_time_serie_value_by_geochemistry_record(self, rec, sample_name):
        param = rec.parameter
        unit = rec.parameter_unit
        val = [rec.value]
        val_date = [rec.sampling_date]
        try:
            self.get_time_series_data(sample_name).create_time_serie(param, unit, val_date, val)
        except:
            pass

    def _fill_time_series_with_samples_data(self):
        """
        fill the time series for the given parameter with all the values avaible
        :return:
        """
        for site in self.get_time_series_data():
            for ts in self.get_time_series_data(site).get_records():
                for _dates in self.get_geochemistry_data():
                    rec = self.get_sample_by_date(_dates, site).get_record_by_parameter(ts.parameter)
                    try:
                        ts.add_value(rec.sampling_date, rec.value)
                    except KeyError as k:
                        continue
                    except AttributeError as a:
                        pass
                    except Exception as e:
                        print(type(e))
                        print(e)
                ts.reorder_values()


class DrillingFileReader(AbstractFileReader):
    def __init__(self, file_path: str = None, header_length: int = None, request_params: dict = None):
        super().__init__(file_path, header_length, request_params)
        self._site_of_interest = defaultdict(dict)

    def create_drilling_site(self, site_name: str):
        self.create_complete_drilling_site(site_name=site_name)
        yield self._site_of_interest[site_name]

    def create_complete_drilling_site(self, site_name: str, visit_date: datetime.datetime = None,
                                      project_name: str = None,
                                      other_identifier: str = None,
                                      coordinates_x_y_z: geographical_coordinates = None,
                                      drilling_depth: float = 0.0,
                                      drill_dip: float = 0.0,
                                      drill_azimut: float = 0.0,
                                      drilling_diameter: float = 0.0):
        drilling_site = DrillingSite(site_name=site_name,
                                     visit_date=visit_date,
                                     project_name=project_name,
                                     other_identifier=other_identifier,
                                     coordinates_x_y_z=coordinates_x_y_z,
                                     drill_azimut=drill_azimut,
                                     drill_dip=drill_dip,
                                     drilling_depth=drilling_depth,
                                     drilling_diameter=drilling_diameter)
        self._site_of_interest[site_name] = drilling_site
        return self._site_of_interest[site_name]
