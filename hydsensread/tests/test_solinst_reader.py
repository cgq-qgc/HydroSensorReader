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


if __name__ == "__main__":
    pytest.main(['-x', os.path.basename(__file__), '-v', '-rw'])
