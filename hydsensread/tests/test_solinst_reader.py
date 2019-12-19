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
import pytest
from pandas import Timestamp

# ---- Local imports
import hydsensread as hsr


# ---- Fixtures
@pytest.fixture(scope="module")
def test_files_dir():
    return osp.join(osp.dirname(__file__), 'files')


# ---- Tests
@pytest.mark.parametrize(
    'testfile',
    ["2XXXXXX_solinst_levelogger_edge_testfile.csv",
     "2XXXXXX_solinst_levelogger_edge_testfile.xle"])
def test_solinst_levelogger_edge(test_files_dir, testfile):
    """Test reading Solinst Edge Levelogger files."""
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    records = solinst_file.records
    assert len(records) == 19484

    assert records.index.tolist()[0] == Timestamp('2017-05-03 13:00:00')
    assert records.iloc[0].iloc[0] == 1919.32
    assert records.iloc[0].iloc[1] == 7.849

    assert records.index.tolist()[-1] == Timestamp('2017-11-22 11:45:00')
    assert records.iloc[-1].iloc[0] == 1906.33
    assert records.iloc[-1].iloc[1] == 8.275

    assert list(records.columns) == ["LEVEL_cm", "TEMPERATURE_°C"]

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "2010143"
    assert sites.project_name == "03040018"
    assert sites.site_name == "Sutton_PO22B"


def test_solinst_levelogger_edge_lev(test_files_dir):
    """Test reading Solinst Edge Levelogger .lev files."""
    testfile = "2XXXXXX_solinst_levelogger_edge_testfile.lev"
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    records = solinst_file.records
    assert len(records) == 10258

    assert records.index.tolist()[0] == Timestamp('2017-03-07 19:00:00')
    assert records.iloc[0].iloc[0] == 14.6861
    assert records.iloc[0].iloc[1] == 7.626

    assert records.index.tolist()[-1] == Timestamp('2017-06-22 15:15:00')
    assert records.iloc[-1].iloc[0] == 10.1788
    assert records.iloc[-1].iloc[1] == 11.844

    assert list(records.columns) == ["LEVEL_m", "TEMPERATURE_°C"]

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "2041929"
    assert sites.project_name == "McCully"
    assert sites.site_name == "PO-06_XM20170307"


@pytest.mark.parametrize(
    'testfile',
    ["1XXXXXX_solinst_levelogger_gold_testfile.csv",
     "1XXXXXX_solinst_levelogger_gold_testfile.lev"])
def test_solinst_levelogger_gold(test_files_dir, testfile):
    """
    Test reading Solinst Edge Levelogger files.

    Regression test for Issue #26.
    """
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    records = solinst_file.records
    assert len(records) == 200

    assert records.index[0] == Timestamp('2017-05-02 13:00:00')
    assert records.iloc[0].iloc[0] == 923.561
    assert records.iloc[0].iloc[1] == 8.936

    assert records.index[-1] == Timestamp('2017-05-04 14:45:00')
    assert records.iloc[-1].iloc[0] == 934.8801
    assert records.iloc[-1].iloc[1] == 8.914

    assert list(records.columns) == ["LEVEL_cm", "TEMPERATURE_Deg C"]

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "1062280"
    assert sites.project_name == "03030012"
    assert sites.site_name == "Saint-Guillaume_P14A"
    assert sites.other_attributes['altitude'] == 42


@pytest.mark.parametrize(
    'testfile',
    ["2XXXXXX_solinst_colon_as_decimalsep.csv",
     "2XXXXXX_solinst_colon_as_decimalsep.xle"])
def test_solinst_colon_decimalsep(test_files_dir, testfile):
    """
    Test that level data can be read correctly from the Solinst data files when
    a colon is used as decimal separator instead of the dot.

    Regression test for Issue #33.
    """
    solinst_file = hsr.SolinstFileReader(osp.join(test_files_dir, testfile))

    records = solinst_file.records
    assert len(records) == 10

    assert records.index.tolist()[0] == Timestamp('2016-11-23 19:00:00')
    assert records.iloc[0].iloc[0] == 1813.03
    assert records.iloc[0].iloc[1] == 9.182

    assert records.index.tolist()[-1] == Timestamp('2016-11-23 21:15:00')
    assert records.iloc[-1].iloc[0] == 1812.59
    assert records.iloc[-1].iloc[1] == 9.179

    assert list(records.columns) == ["LEVEL_cm", "TEMPERATURE_°C"]

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "2048469"
    assert sites.project_name == "03040008"
    assert sites.site_name == "Rougemont_Plus profond"


if __name__ == "__main__":
    pytest.main(['-x', os.path.basename(__file__), '-v', '-rw'])
