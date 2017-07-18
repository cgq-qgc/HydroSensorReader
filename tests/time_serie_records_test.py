#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from sensor_file.domain.records import TimeSeriesRecords
import datetime

class TimeSeriesRecordsTest(unittest.TestCase):
    def setUp(self):
        self.ts = TimeSeriesRecords()
        self.dates = [datetime.datetime(2014, 10, 3, 15, 00),
                 datetime.datetime(2014, 10, 3, 15, 30),
                 datetime.datetime(2014, 10, 4, 15, 00),
                 datetime.datetime(2014, 10, 5, 15, 00),
                 datetime.datetime(2014, 10, 6, 15, 00),
                 datetime.datetime(2014, 10, 7, 15, 00)]
        self.vals = list(range(len(self.dates)))
        self.ts.set_time_serie_values(self.dates, self.vals)
    def test_get_one_record_by_date(self):
        self.assertEqual(len(self.ts.get_data_at_time(datetime.datetime(2014, 10, 3,15,30))), 1)
        self.assertEqual(self.ts.get_data_at_time(datetime.datetime(2014, 10, 3,15,30)),
                         [[datetime.datetime(2014, 10, 3,15,30),1]])

    def test_get_multiple_record_by_date(self):
        multiple_record = self.ts.get_data_at_time(datetime.datetime(2014, 10, 3))
        anticipated_response = [[datetime.datetime(2014, 10, 3,15,00),0],
                                [datetime.datetime(2014, 10, 3,15,30),1]]
        self.assertEqual(multiple_record,anticipated_response)

    def test_get_datas_between(self):
        d_from = 2
        d_to = 4

        getted_record = self.ts.get_data_between(self.dates[d_from],self.dates[d_to])
        anticipated_values = [[date,val] for date,val in zip(self.dates[d_from:d_to+1],self.vals[d_from:d_to+1])]
        self.assertEqual(getted_record,anticipated_values)

    def test_get_data_after(self):
        d_after = 3
        getted_records = self.ts.get_data_after_date(self.dates[3])
        anticipated_values = [[date,val] for date,val in zip(self.dates[d_after:],self.vals[d_after:])]
        self.assertEqual(getted_records,anticipated_values)

    def test_get_data_before(self):
        d_before = 3
        getted_records = self.ts.get_data_before_date(self.dates[3])
        anticipated_values = [[date, val] for date, val in zip(self.dates[:d_before+1], self.vals[:d_before+1])]
        self.assertEqual(getted_records, anticipated_values)

    def test_get_data_between_bad_interval(self):
        d_from = 4
        d_to = 2
        with self.assertRaises(AssertionError) as context:
            self.ts.get_data_between(self.dates[d_from], self.dates[d_to])
            self.assertTrue("The first date must be before the last date" in str(context.msg))

    def test_get_data_before_not_in_values(self):
        date_before = self.dates[0]
        date_before = datetime.datetime(date_before.year-1,date_before.month,date_before.day)
        getted_dates = self.ts.get_data_before_date(date_before)
        self.assertTrue(len(getted_dates) == 0)

    def test_get_data_after_not_in_values(self):
        date_after = self.dates[-1]
        date_after = datetime.datetime(date_after.year+1,date_after.month, date_after.day)
        getted_dates = self.ts.get_data_after_date(date_after)
        self.assertTrue(len(getted_dates) == 0)

suite = unittest.TestLoader().loadTestsFromTestCase(TimeSeriesRecordsTest)
unittest.TextTestRunner(verbosity=2).run(suite)

