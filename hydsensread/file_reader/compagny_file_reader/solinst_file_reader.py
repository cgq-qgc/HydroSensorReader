# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © HydroSensorReader Project Contributors
# https://github.com/cgq-qgc/HydroSensorReader
#
# This file is part of HydroSensorReader.
# Licensed under the terms of the MIT License.
# -----------------------------------------------------------------------------

# ---- Standard imports
import datetime
import re
import warnings
from collections import defaultdict
from typing import List, Tuple
import os.path as osp

# ---- Third party imports
import numpy as np
import pandas as pd

# ---- Local imports
from hydsensread.file_reader.abstract_file_reader import (
    TimeSeriesFileReader, LineDefinition)


class SolinstFileReader(object):
    """
    A reader for Solinst '.lev', '.xle', or '.csv' files.
    """

    def __new__(cls, file_path, wait_read=False):
        """
        Parameters
        ----------
        file_path : str, path object
            A valid string path or path object to a Solinst '.lev', '.xle', or
            '.csv' level or baro level data file.
        wait_read : bool
            A boolean that indicates wheter the content of the file should be
            read on instantiation of the reader. If 'False', use the
            'read_file' method of the reader to read the content of the file
            when needed.

        Returns
        -------
        TimeSeriesFileReader
            A time series file reader that can read Solinst '.lev', '.xle', or
            '.csv' level or baro logger data files.

        """
        file_path = str(file_path)
        if not osp.isfile(file_path) or not osp.exists(file_path):
            raise ValueError("The path given doesn't point to an "
                             "existing file.")

        root, ext = osp.splitext(file_path)
        ext = ext[1:]
        if ext in TimeSeriesFileReader.CSV_FILES_TYPES:
            return CSVSolinstFileReader(file_path, wait_read=wait_read)
        elif ext == 'lev':
            return LEVSolinstFileReader(file_path, wait_read=wait_read)
        elif ext == 'xle':
            return XLESolinstFileReader(file_path, wait_read=wait_read)
        else:
            warnings.warn("Unknown file extension for this compagny")


class SolinstFileReaderBase(TimeSeriesFileReader):
    """
    Base class for Solinst file readers.
    """

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    # ---- Public API
    def plot(self, other_axis=None, reformat_temperature=True,
             *args, **kwargs):
        """
        Plot function overriding the TimeSeriesFileReader method.

        Parameters
        ----------
        other_axis: list
            if other axis needs to be added to the plot, use this parameter
        reformat_temperature: bool
            if the temperature axis needs to be reformated or not.

        Returns
        -------
        plt.Figure
            A matplotlib Figure object.
        List of mpl.Axes
            A list of matplotlib Axes object.
        """
        other_axis = [] if other_axis is None else other_axis
        nparams = len(self.records.columns)

        # Setup level channel line definition.
        level_line_def = LineDefinition(
            self.records.columns[0], 'blue', make_grid=True)

        # Setup temperature channel line definition.
        if nparams >= 2:
            temp_line_def = LineDefinition(self.records.columns[1], 'red')
            temp_values = self.records[self.records.columns[1]]
            other_axis.append(temp_line_def)

        # Setup other channel line definition.
        colors = ['orange', 'green', 'purple', 'black',
                  'brown', 'darkorange', 'cyan']
        if nparams >= 3:
            for color_index, param in enumerate(self.records.columns[2:]):
                if color_index > len(colors):
                    color_index = color_index - len(colors)
                    other_axis.append(
                        LineDefinition(param, colors[color_index]))

        fig, axis = super().plot(level_line_def, other_axis, *args, **kwargs)

        # This is for barometric data.
        n = len([i for i in self.records.columns if 'kpa' in i.lower()])
        if n == 0 and reformat_temperature and nparams >= 2:
            axis[1].set_ylim(temp_values.mean() - 1, temp_values.mean() + 1)
        return fig, axis

    # ---- AbstractFileReader API
    def _read_file_header(self):
        """
        Retrieve metadata from the header and determine the lenght of the
        header.
        """
        self._update_header_lentgh()
        self._update_plateform_attributes()

    def _read_file_data_header(self):
        """Read the data header (what was recorded)."""
        pass

    def _read_file_data(self):
        """Read and classify the data columns."""
        self._date_list = self._get_date_list()
        self._get_data()
        self._format_data_units()

    # ---- Private API
    def _format_data_units(self):
        columns_map = {}
        for column in self.records.columns:
            column_split = column.split('_')
            units = column_split.pop(-1).lower()

            # We need to do this in case we got the file encoding wrong.
            # See #cgq-qgc/HydroSensorReader#66
            units = re.sub(r'[^a-zA-Z0-9°\.]', '', units)

            if units in ['°c', 'degc', 'degree_celsius', 'celsius', 'degreec']:
                columns_map[column] = '_'.join(column_split) + '_degC'
            else:
                columns_map[column] = column
        self.records.rename(columns_map, axis='columns', inplace=True)

    def undo_altitude_correction(self):
        """
        Undo the automatic compensation for elevation applied to readings made
        by level and baro loggers of the Gold series (1xxxxxx) and older.

        See cgq-qgc/HydroSensorReader#43
        """
        altitude = self.sites.other_attributes['altitude']
        serial_number = int(self.sites.instrument_serial_number)
        if altitude is not None and serial_number < 2000000:
            for column in self.records.columns:
                # When a metric unit is used, the unit of altitude is meters.
                # When feet are the level channel units, feet are the units
                # of altitude.
                #
                # See Levelogger Series User Guide - Software Version 4,
                # section 5.9 Levelogger Gold Series Setup, page 35.
                units = column.split('_')[-1]
                if units in ['m', 'ft']:
                    self.sites.records[column] = (
                        self.sites.records[column] - 0.0012 * altitude)
                elif units == 'cm':
                    self.sites.records[column] = (
                        self.sites.records[column] - 0.12 * altitude)

    def undo_zero_point_offset(self):
        """
        Undo the zero point offset applied to readings made by level and baro
        loggers of the Gold series (1xxxxxx) and older.

        See cgq-qgc/HydroSensorReader#51
        """
        serial_number = int(self.sites.instrument_serial_number)
        if serial_number < 2000000:
            for column in self.records.columns:
                units = column.split('_')[-1]
                if units == 'm':
                    self.sites.records[column] = (
                        self.sites.records[column] + 9.5)
                elif units == 'cm':
                    self.sites.records[column] = (
                        self.sites.records[column] + 950)
                elif units == 'ft':
                    self.sites.records[column] = (
                        self.sites.records[column] + 31.17)

    def _get_data(self):
        """Return the numerical data from the Solinst data file."""
        pass

    def _update_header_lentgh(self):
        pass

    def _update_plateform_attributes(self):
        """
        Update the SensorPlateform instance of this reader by setting
        its attributes.
        """
        self.sites.visit_date = self._create_visited_date()
        self.sites.site_name = self._get_site_name()
        self.sites.instrument_serial_number = self._get_serial_number()
        self.sites.project_name = self._get_project_name()
        self.sites.batterie_level = self._get_battery_level()
        self.sites.model_number = self._get_model_number()
        self.sites.instrument_type = self._get_instrument_type()

        # A value for the altitude is present in the header of data
        # files produced by Solinst level and baro loggers of the
        # Gold series (1xxxxxx) and older. This value is used to
        # correct measurements for altitude before they are saved
        # in the logger.
        self.sites.other_attributes['altitude'] = self._get_altitude()

    def _create_visited_date(self):
        pass

    def _get_site_name(self):
        """Return the site name scraped from the header of the file."""
        pass

    def _get_serial_number(self):
        """
        Return the serial number of the Solinst level or baro logger scraped
        from the header of the file.
        """
        pass

    def _get_project_name(self):
        """Return the site name scraped from the header of the file."""
        pass

    def _get_battery_level(self):
        pass

    def _get_instrument_type(self):
        pass

    def _get_model_number(self):
        pass

    def _get_altitude(self):
        """Return the altitude value scraped from the header of the file."""
        pass


class LEVSolinstFileReader(SolinstFileReaderBase):
    DATA_CHANNEL_STRING = ".*CHANNEL {} from data header.*"

    def __init__(self, file_path: str = None, header_length: int = 10,
                 wait_read: bool = False):
        super().__init__(file_path, header_length, encoding='cp1252',
                         wait_read=wait_read)

    # ---- AbstractFileReader API
    def _get_date_list(self) -> List[datetime.datetime]:
        """Retrieve the datetime data from the file content."""
        sep = self.file_content[self._header_length + 1][4]
        datetime_list = []
        for lines in self.file_content[self._header_length + 1:-1]:
            sep_line = lines.split(" ")
            try:
                _date_time = datetime.datetime.strptime(
                    "{} {}".format(sep_line[0], sep_line[1]),
                    '%Y{}%m{}%d %H:%M:%S.%f'.format(sep, sep))
            except ValueError:
                break
            datetime_list.append(_date_time)
        return datetime_list

    # ---- SolinstFileReaderBase API
    def _update_header_lentgh(self):
        for i, lines in enumerate(self.file_content):
            if re.search('^.data.*', lines.lower()):
                self._header_length = i + 1
                break
        else:
            raise TypeError("The data are not formatted correctly.")

    # ---- Private API
    def _create_visited_date(self) -> datetime:
        _date = None
        _time = None
        for lines in self.file_content[:self._header_length]:
            if re.search("^date.*", lines, re.IGNORECASE):
                _date = lines.split(":")[1].replace(" ", "")
            if re.search(r"^time.*", lines, re.IGNORECASE):
                _time = lines.split(" :")[1].replace(" ", "")
        to_datetime = datetime.datetime.strptime(
            "{} {}".format(_date, _time),
            self.MONTH_S_DAY_S_YEAR_HMS_DATE_STRING_FORMAT)
        return to_datetime

    def _get_instrument_info(self, regex_: str) -> str:
        str_to_find = None
        for i, lines in enumerate(self.file_content):
            if i == self._header_length:
                break
            if re.search(regex_, lines):
                str_to_find = lines.split("=")[1].strip()
                break
        return str_to_find

    def _get_altitude(self):
        """
        Return the altitude value scraped from the header of the file.
        """
        alt_str = self._get_instrument_info(r".*[aA]ltitude.*")
        if alt_str is not None:
            return float(re.findall(r"\d*\.\d+|\d+", alt_str)[0])
        else:
            return None
        return

    def _get_site_name(self) -> str:
        return self._get_instrument_info(r".*[lL]ocation.*")

    def _get_serial_number(self):
        serial_string = self._get_instrument_info(r".*(S|s)erial.number.*")
        serial_numb = re.findall(r'-(?:\s*)(\d*)\s*\d*', serial_string)[0]
        return serial_numb

    def _get_project_name(self):
        return self._get_instrument_info(r".*(I|i)nstrument.number.*")

    def _get_number_of_channels(self) -> int:
        return int(self._get_instrument_info(r" *Channel *=.*"))

    def _get_data(self):
        for channel_num in range(self._get_number_of_channels()):
            param = None
            param_unit = None
            for row_num, row in enumerate(
                    self.file_content[:self._header_length]):
                data_channel_string = (
                    self.DATA_CHANNEL_STRING.format(channel_num + 1))
                if re.search(data_channel_string, row):
                    next_row = self.file_content[row_num + 1].strip()
                    if re.search(r".*identification.*", next_row.lower()):
                        param = next_row.split("=")[-1].strip()
                    next_row = self.file_content[row_num + 2].strip()
                    if re.search(r".*unit.*", next_row.lower()):
                        param_unit = next_row.split("=")[-1].strip()
                    elif re.search(r".*reference.*", next_row.lower()):
                        # For Solinst loggers older than the Gold series.
                        param_unit = next_row.split("=")[-1]
                        param_unit = param_unit.split(" ")[-1].strip()

            values = []
            for lines in self.file_content[self._header_length + 1:-1]:
                sep_line = [
                    data for data in list(lines.split(" ")) if data != '']
                values.append(float(sep_line[channel_num + 2]))
            self.sites.create_time_serie(
                param, param_unit, self._date_list, values)


class XLESolinstFileReader(SolinstFileReaderBase):
    CHANNEL_DATA_HEADER = "Ch{}_data_header"

    def __init__(self, file_path: str = None, header_length: int = 10,
                 wait_read: bool = False):
        super().__init__(file_path, header_length, wait_read=wait_read)

    def read_file(self):
        """Extension of the base class abstract method."""
        self.file_root = self.file_content.getroot()
        super().read_file()

    # ---- AbstractFileReader API
    def _get_date_list(self) -> list:
        """
        get a list of timestamp present in the file
        :return:
        """
        datetime_list = [
            datetime.datetime.strptime(
                "{} {}:{}".format(
                    _data.find('Date').text,
                    _data.find('Time').text,
                    _data.find('ms').text
                    ).replace('_', '/'),
                '%Y/%m/%d %H:%M:%S:%f'
            ) for _data in self.file_root.iter('Log')]
        return datetime_list

    # ---- SolinstFileReaderBase API
    def _create_visited_date(self) -> datetime:
        """
        Create a datetime object by reading the file header.
        The visited date is equal to the creation date of the file
        """
        file_info = self.file_root.find('File_info')

        date_str = file_info.find('Date').text
        time_str = file_info.find('Time').text

        if date_str == time_str:
            # Some loggers keep a (potentially tz-aware) datetime in BOTH date
            # and time fields.
            datetime_str = date_str
        else:
            # Some models delimit date fields with "_".
            datetime_str = "{} {}".format(date_str, time_str).replace("_", "/")

        if re.search(' -[0-9]{4}$', datetime_str):
            # Timezone offset at end of datetime string on some models
            datetime_obj = datetime.datetime.strptime(
                datetime_str, self.YEAR_S_MONTH_S_DAY_HMS_Z_DATE_STRING_FORMAT)
        else:
            datetime_obj = datetime.datetime.strptime(
                datetime_str, self.YEAR_S_MONTH_S_DAY_HMS_DATE_STRING_FORMAT)
        return datetime_obj

    def _get_site_name(self) -> str:
        return self.file_root.find(
            'Instrument_info_data_header').find('Location').text

    def _get_serial_number(self):
        return self.file_root.find(
            'Instrument_info').find('Serial_number').text

    def _get_project_name(self):
        return self.file_root.find(
            'Instrument_info_data_header').find('Project_ID').text

    def _get_number_of_channels(self):
        return int(self.file_root.find(
            'Instrument_info').find('Channel').text)

    def _get_model_number(self):
        return self.file_root.find('Instrument_info').find('Model_number').text

    def _get_battery_level(self):
        try:
            return self.file_root.find(
                'Instrument_info').find('Battery_level').text
        except AttributeError:
            return "N/A"

    def _get_instrument_type(self):
        try:
            return self.file_root.find(
                'Instrument_info').find('Instrument_type').text
        except AttributeError:
            return "N/A"

    # ---- Private API
    def _get_data(self) -> None:
        """
        create time serie and update the SensorPlateform object
        :return:
        """
        for channels in range(self._get_number_of_channels()):
            channel_name = self.CHANNEL_DATA_HEADER.format(channels + 1)
            channel_parammeter = self.file_root.find(
                channel_name).find('Identification').text
            channel_unit = self.file_root.find(channel_name).find('Unit').text
            ch_selector = "ch{}".format(channels + 1)
            try:
                values = [float(d.find(ch_selector).text)
                          for d in self.file_root.iter('Log')]
            except ValueError:
                # This probably means that a coma is used as decimal separator.
                values = [float(d.find(ch_selector).text.replace(',', '.'))
                          for d in self.file_root.iter('Log')]

            self._site_of_interest.create_time_serie(
                channel_parammeter, channel_unit, self._date_list, values)


class CSVSolinstFileReader(SolinstFileReaderBase):

    def __init__(self, file_path: str = None, header_length: int = 12,
                 wait_read: bool = False):
        self._params_dict = defaultdict(dict)
        self._start_of_data_row_index = header_length
        super().__init__(file_path, header_length, wait_read=wait_read,
                         csv_delim_regex="date([;,\t])time")

    # ---- Base class abstract method implementation
    def _get_date_list(self) -> list:
        """Retrieve the datetime data from the file content."""
        data_header = self.file_content[self._start_of_data_row_index]
        istart = data_header.index('Date')
        iend = istart + 1
        fmt = "{} {}"
        if 'ms' in ''.join(data_header):
            iend += 1
            fmt += ".{}"

        # We store the line indexes corresponding to valid dates in the
        # record, so that we can retrieve the numerical data at these specific
        # indexes later in _get_data. This is required in case there is
        # blank lines or badly formatted dates in the record.
        # See cgq-qgc/HydroSensorReader#62.
        self._data_content_indexes = []
        datetimes = []
        data_content = self.file_content[self._start_of_data_row_index + 1:]
        for i, line in enumerate(data_content):
            try:
                _datetime = pd.Timestamp(fmt.format(*line[istart:iend + 1]))
            except (ValueError, IndexError):
                continue
            datetimes.append(_datetime)
            self._data_content_indexes.append(
                i + self._start_of_data_row_index + 1)
        self.sites.visit_date = datetimes[-1]
        return datetimes

    # ---- SolinstFileReaderBase API
    def _update_header_lentgh(self):
        for i, line in enumerate(self.file_content):
            line = ''.join(line).lower()
            if 'date' in line and 'time' in line:
                self._start_of_data_row_index = i
                self._header_length = i
                break
        else:
            raise TypeError("The data are not formatted correctly.")

    def _get_site_name(self):
        """Return the site name scraped from the header of the file."""
        return self._get_instrument_info(r"[lL]ocation.*")

    def _get_serial_number(self):
        """
        Return the serial number of the Solinst level or baro logger scraped
        from the header of the file.
        """
        return self._get_instrument_info(r"[sS]erial.[nN]umber.*")

    def _get_project_name(self):
        """Return the site name scraped from the header of the file."""
        return self._get_instrument_info(r"[pP]roject.[idID].*")

    def _get_battery_level(self):
        return None

    def _get_model_number(self):
        return None

    def _get_altitude(self):
        """Return the altitude value scraped from the header of the file."""
        altitude = None
        for i, line in enumerate(self.file_content):
            if i == self._header_length:
                break

            line = ''.join(line).lower()
            if re.search(r"[aA]ltitude.*", line):
                regex = r"\d*\.\d+|\d+"
                try:
                    altitude = float(re.findall(regex, line)[0])
                except IndexError:
                    # This means that the value is stored on the next line.
                    next_line = ''.join(self.file_content[i + 1])
                    altitude = float(re.findall(regex, next_line)[0])
                break
        return altitude

    # ---- Private API
    def _get_instrument_info(self, regex_: str) -> str:
        result = None
        for i, line in enumerate(self.file_content):
            if i == self._header_length:
                break
            if re.search(regex_, ''.join(line).lower()):
                try:
                    result = self.file_content[i + 1][0].strip()
                except IndexError:
                    result = ''
                break
        return result

    def _get_parameter_data(self):
        """
        Retrieve the parameters name, units, and column index from the file
        content.
        """
        data_header = self.file_content[self._start_of_data_row_index]
        params = [p for p in data_header if p
                  not in ('', 'Date', 'ms', '100 ms', 'Time')]
        for i, row in enumerate(self.file_content[:self._header_length]):
            if not len(row):
                continue

            # Some files produced for Solinst logger models older than the Gold
            # series add tabulations at the beginning of some lines in the
            # header, so we need to remove them.
            row0 = row[0].replace('\t', '')
            if row0 in params:
                self._params_dict[row0]['col_index'] = (
                    data_header.index(row0))
                if "UNIT: " in self.file_content[i + 1][0]:
                    # For Solinst Edge logger files.
                    units = self.file_content[i + 1][0].split(": ")[1]
                elif "Offset" in self.file_content[i + 1][0]:
                    # For Solinst loggers older than the Gold series.
                    units = self.file_content[i + 2][0].split(" ")[-1]
                else:
                    # For Solinst Gold logger files.
                    units = self.file_content[i + 2][0]
                self._params_dict[row0]['unit'] = units.strip()

    def _get_data(self):
        """Retrieve the numerical data from the Solinst data file."""
        self._get_parameter_data()
        data = [self.file_content[i] for i in self._data_content_indexes]

        # We go over each row of data and pad with nan values when needed
        # to make sure each row has the same length.
        # See cgq-qgc/HydroSensorReader#62.
        pad = len(max(data, key=len))
        data = np.array([row + [np.nan] * (pad - len(row)) for row in data])

        for parameter in list(self._params_dict.keys()):
            param_unit = self._params_dict[parameter]['unit']
            param_col_index = self._params_dict[parameter]['col_index']

            values = data[:, param_col_index]
            values = np.char.replace(np.char.strip(values), ',', '.')
            values[values == ''] = np.nan
            values = values.astype(float)

            self._site_of_interest.create_time_serie(
                parameter, param_unit, self._date_list, values)


if __name__ == '__main__':
    dirname = osp.join(osp.dirname(__file__), 'tests', 'files')
    filename = '1XXXXXX_solinst_levelogger_gold_testfile.csv'
    filename = '1XXXXXX_solinst_levelogger_gold_testfile.lev'
    filename = 'XXXX_solinst_levelogger_M5.csv'
    filename = 'XXXX_solinst_levelogger_M5.lev'
    filename = 'solinst_missing_data.csv'
    reader = SolinstFileReader(osp.join(dirname, filename))
    print(reader.records)
    print(reader.sites)
    print(reader.sites.instrument_serial_number)
    print(reader.records.keys())
    reader.plot()
