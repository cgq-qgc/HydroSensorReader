# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © HydroSensorReader Project Contributors
# https://github.com/cgq-qgc/HydroSensorReader
#
# This file is part of HydroSensorReader.
# Licensed under the terms of the MIT License.
# -----------------------------------------------------------------------------

# ---- Standard imports
import os
import os.path as osp

# ---- Third party imports
import matplotlib.pyplot as plt
import pytest
from pandas import Timestamp
import pandas as pd

# ---- Local imports
import hydsensread as hsr


# ---- Fixtures
@pytest.fixture(scope="module")
def test_files_dir():
    return osp.join(osp.dirname(__file__), 'files')


# ---- Tests
@pytest.mark.parametrize(
    'testfile',
    ["2XXXXXX_solinst_levelogger_edge.csv",
     "2XXXXXX_solinst_levelogger_edge.xle",
     ])

def test_solinst_levelogger_edge(test_files_dir, testfile):
    """Test reading Solinst Edge Levelogger files."""
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "2010143"
    assert sites.project_name == "03040018"
    assert sites.site_name == "Sutton_PO22B"

    records = solinst_file.records
    assert len(records) == 200
    assert list(records.columns) == ["LEVEL_cm", "TEMPERATURE_degC"]

    assert records.index[0] == Timestamp('2017-05-03 13:00:00')
    assert records.iloc[0].iloc[0] == 1919.32
    assert records.iloc[0].iloc[1] == 7.849

    assert records.index[-1] == Timestamp('2017-05-05 14:45:00')
    assert records.iloc[-1].iloc[0] == 1920.85
    assert records.iloc[-1].iloc[1] == 7.872

    assert solinst_file.plot()
    plt.close('all')

@pytest.mark.parametrize(
    'testfile',
     ['LT_EDGE_m30_fw3.003.xle',
     ])

def test_solinst_levelogger_edge_m30(test_files_dir, testfile):
    """Test reading Solinst Edge Levelogger files."""
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "1234567"
    assert sites.project_name == 'Sample Project'
    assert sites.site_name == '12345'

    records = solinst_file.records
    assert len(records) == 3
    assert list(records.columns) == ["LEVEL_m", "TEMPERATURE_degC"]

    assert records.index[0] == Timestamp('2020-01-04 18:00:00')
    assert records.iloc[0].iloc[0] == 18.3972
    assert records.iloc[0].iloc[1] == +3.594

    assert records.index[-1] == Timestamp('2020-04-05 12:00:00')
    assert records.iloc[-1].iloc[0] == 18.3551
    assert records.iloc[-1].iloc[1] == 3.826
    assert solinst_file.plot()
    plt.close('all')



def test_solinst_levelogger_edge_lev(test_files_dir):
    """Test reading Solinst Edge Levelogger .lev files."""
    testfile = "2XXXXXX_solinst_levelogger_edge.lev"
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "2041929"
    assert sites.project_name == "McCully"
    assert sites.site_name == "PO-06_XM20170307"

    records = solinst_file.records
    assert len(records) == 200
    assert list(records.columns) == ["LEVEL_m", "TEMPERATURE_degC"]

    assert records.index[0] == Timestamp('2017-03-07 19:00:00')
    assert records.iloc[0].iloc[0] == 14.6861
    assert records.iloc[0].iloc[1] == 7.626

    assert records.index[-1] == Timestamp('2017-03-09 20:45:00')
    assert records.iloc[-1].iloc[0] == 14.5130
    assert records.iloc[-1].iloc[1] == 7.610

    assert solinst_file.plot()
    plt.close('all')


@pytest.mark.parametrize(
    'testfile',
    ["1XXXXXX_solinst_levelogger_gold.csv",
     "1XXXXXX_solinst_levelogger_gold.lev"])
def test_solinst_levelogger_gold(test_files_dir, testfile):
    """
    Test reading Solinst Edge Levelogger files.

    Regression test for Issue #26.
    """
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "1062280"
    assert sites.project_name == "03030012"
    assert sites.site_name == "Saint-Guillaume_P14A"
    assert sites.other_attributes['altitude'] == 42

    records = solinst_file.records
    assert len(records) == 200
    assert list(records.columns) == ["LEVEL_cm", "TEMPERATURE_degC"]

    assert records.index[0] == Timestamp('2017-05-02 13:00:00')
    assert records.iloc[0].iloc[0] == 923.561
    assert records.iloc[0].iloc[1] == 8.936

    assert records.index[-1] == Timestamp('2017-05-04 14:45:00')
    assert records.iloc[-1].iloc[0] == 934.8801
    assert records.iloc[-1].iloc[1] == 8.914

    # Test undo altitude correction.
    solinst_file.undo_altitude_correction()
    assert records.iloc[-1].iloc[0] == 934.8801 - (0.12 * 42)
    assert records.iloc[-1].iloc[0] == 934.8801 - (0.12 * 42)

    # Test undo zero point offset.
    solinst_file.undo_zero_point_offset()
    assert records.iloc[0].iloc[0] == 923.561 - (0.12 * 42) + 950
    assert records.iloc[-1].iloc[0] == 934.8801 - (0.12 * 42) + 950

    assert solinst_file.plot()
    plt.close('all')

@pytest.mark.parametrize(
    'testfile',
    [ 'LT_Gold_baro_m15_fw2006.xle'
     ])
def test_solinst_levelogger_gold_m15(test_files_dir, testfile):
    """
    Test reading Solinst LT Gold barologger files.
    """
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "7654321"
    assert sites.project_name == 'Someplace'
    assert sites.site_name =='Somewhere'
    assert sites.other_attributes['altitude'] is None

    records = solinst_file.records
    assert len(records) == 2
    assert list(records.columns) == ["LEVEL_m", "TEMPERATURE_degC"]

    assert records.index[0] == Timestamp('2021-01-03 16:00:04')
    assert records.iloc[0].iloc[0] ==-0.6523
    assert records.iloc[0].iloc[1] ==-5.329

    assert records.index[-1] == Timestamp('2021-10-16 10:00:04')
    assert records.iloc[-1].iloc[0] == -0.5228
    assert records.iloc[-1].iloc[1] == -3.501

    assert solinst_file.plot()
    plt.close('all')


@pytest.mark.parametrize(
    'testfile',
    ["XXXX_solinst_levelogger_M5.csv",
     "XXXX_solinst_levelogger_M5.lev"])
def test_solinst_levelogger_M5(test_files_dir, testfile):
    """
    Test reading Solinst Levelogger M5 files (older than the Gold series).
    """
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "5741"
    assert sites.project_name == "04040001"
    assert sites.site_name == "St-Andre-Avellin"
    assert sites.other_attributes['altitude'] == 170

    records = solinst_file.records
    assert len(records) == 200
    assert list(records.columns) == ["LEVEL_cm"]

    assert records.index[0] == Timestamp('2016-11-04 13:00:00')
    assert records.iloc[0].iloc[0] == 314.0

    assert records.index[-1] == Timestamp('2016-11-06 14:45:00')
    assert records.iloc[-1].iloc[0] == 317.5

    # Test undo altitude correction.
    solinst_file.undo_altitude_correction()
    assert records.iloc[0].iloc[0] == 314.0 - (0.12 * 170)
    assert records.iloc[-1].iloc[0] == 317.5 - (0.12 * 170)

    # Test undo zero point offset.
    solinst_file.undo_zero_point_offset()
    assert records.iloc[0].iloc[0] == 314.0 - (0.12 * 170) + 950
    assert records.iloc[-1].iloc[0] == 317.5 - (0.12 * 170) + 950

    assert solinst_file.plot()
    plt.close('all')


@pytest.mark.parametrize(
    'testfile',
    ["2XXXXXX_solinst_colon_as_decimalsep.csv",
     "2XXXXXX_solinst_colon_as_decimalsep.xle"])
def test_solinst_colon_decimalsep(test_files_dir, testfile):
    """
    Test that level data can be read correctly from the Solinst data files when
    a colon is used as decimal separator instead of the dot.

    Regression test for cgq-qgc/HydroSensorReader#33.
    """
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "2048469"
    assert sites.project_name == "03040008"
    assert sites.site_name == "Rougemont_Plus profond"

    records = solinst_file.records
    assert len(records) == 10
    assert list(records.columns) == ["LEVEL_cm", "TEMPERATURE_degC"]

    assert records.index[0] == Timestamp('2016-11-23 19:00:00')
    assert records.iloc[0].iloc[0] == 1813.03
    assert records.iloc[0].iloc[1] == 9.182

    assert records.index[-1] == Timestamp('2016-11-23 21:15:00')
    assert records.iloc[-1].iloc[0] == 1812.59
    assert records.iloc[-1].iloc[1] == 9.179

    assert solinst_file.plot()
    plt.close('all')


def test_missing_data(test_files_dir):
    """
    Test that file with missing data and empty lines are read as expected.

    Regression test for cgq-qgc/HydroSensorReader#58.
    See also cgq-qgc/HydroSensorReader#62.
    """
    testfile = 'solinst_missing_data.csv'
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    records = solinst_file.records
    assert len(records) == 10
    assert list(records.columns) == ["LEVEL_cm", "TEMPERATURE_degC"]
    assert pd.isnull(records.iloc[0]["TEMPERATURE_degC"])

    assert records.index[0] == Timestamp('2017-05-03 13:00:00')
    assert records.iat[0, 0] == 1919.32
    assert pd.isnull(records.iat[0, 1])

    assert records.index[6] == Timestamp('2017-05-03 14:30:00')
    assert pd.isnull(records.iat[6, 0])
    assert pd.isnull(records.iat[6, 1])

    assert records.index[-1] == Timestamp('2017-05-03 15:15:00')
    assert records.iat[-1, 0] == 1921.87
    assert records.iat[-1, 1] == 7.823


def test_filename_with_dot_in_path(test_files_dir):
    """
    Test that a file with a dot in its path is read without raising any error.

    Regression rest for cgq-qgc/HydroSensorReader#57
    """
    testfile = 'solinst_file_with_._in_name.csv'
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    records = solinst_file.records
    assert len(records) == 10


if __name__ == "__main__":
    pytest.main(['-x', __file__, '-v', '-rw'])
