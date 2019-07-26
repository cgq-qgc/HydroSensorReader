import unittest
from hydsensread.site_and_records import SensorPlateform, TimeSeriesRecords
import numpy as np

PARAM_1 = "param1"
PARAM_2 = "param2"

DATES_1 = np.arange('2016-05-01', '2017-01', dtype='datetime64')
DATES_2 = np.arange('2014-05-01', '2015-01', dtype='datetime64')

class TimeSeriesTestCase(unittest.TestCase):
    """
    Test class for testing merging of different SensorPlateform datas
    """

    def setUp(self) -> None:
        # Create plateforms
        self.plateform = SensorPlateform('teste1')
        self.other_plateform = SensorPlateform('teste2')
        # Create dates and values
        self.values_1 = np.random.standard_exponential(len(DATES_1))
        self.values_2 = np.random.uniform(0, 10, len(DATES_1))
        # Add timeseries to plateform
        self.plateform.create_time_serie(PARAM_1, 'teste', DATES_1, self.values_1)
        self.plateform.create_time_serie(PARAM_2, 'teste', DATES_1, self.values_2)

    def test_same_ts_same_dates(self):
        """
        Merge timeSeries with the same parameter and units and same date interval. the merging must:
        - Add column with suffixe "_2" added at the end
        - time index must be the same
        :return:
        """
        pass

    def test_same_ts_diff_dates(self):
        """
        Merge timeSeries with the same parameter and units and different date interval. the merging must:
        - Not add new column
        - Add values at the appropriate place
        :return:
        """
        pass

    def test_diff_ts_same_dates(self):
        """
        Merge timeSeries with different parameter and same date interval. the merging must:
        - Add new column
        - Add values at the appropriate place
        - time index must be the same
        :return:
        """
        pass

    def test_diff_ts_diff_dates(self):
        """
        Merge timeSeries with different parameter and same date interval. the merging must:
        - Add new column
        - Add values at the appropriate place
        :return:
        """
        pass


if __name__ == '__main__':
    unittest.main()
