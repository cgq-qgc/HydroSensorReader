# ---- Standard imports
import os
import os.path as osp
from pathlib import Path

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
@pytest.mark.parametrize('testfile',
[#'2XXXXXX_solinst_colon_as_decimalsep.xle',
'2XXXXXX_solinst_levelogger_edge.xle',
'LT_EDGE_m30_fw3.003.xle',
'LT_Gold_baro_m15_fw2006.xle'])

def test_load_xle(test_files_dir, testfile):
    p = Path(test_files_dir) / testfile
    r = hsr.SolinstFileReader(str(p))
    assert r
   
if __name__ == "__main__":
    pytest.main(['-x', __file__, '-v', '-rw'])