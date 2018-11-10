# -*- coding: utf-8 -*-

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
    assert len(records) == 19475

    assert records.index.tolist()[0] == Timestamp('2017-05-02 13:00:00')
    assert records.iloc[0].iloc[0] == 923.561
    assert records.iloc[0].iloc[1] == 8.936

    assert records.index.tolist()[-1] == Timestamp('2017-11-21 09:30:00')
    assert records.iloc[-1].iloc[0] == 912.308
    assert records.iloc[-1].iloc[1] == 9.204

    sites = solinst_file.sites
    assert sites.instrument_serial_number == "1062280"
    assert sites.project_name == "03030012"
    assert sites.site_name == "Saint-Guillaume_P14A"


if __name__ == "__main__":
    pytest.main(['-x', os.path.basename(__file__), '-v', '-rw'])
