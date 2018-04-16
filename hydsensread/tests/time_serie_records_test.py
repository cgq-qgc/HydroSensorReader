#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import unittest

import numpy as np
import pandas as pd

from hydsensread.site_and_records.records import TimeSeriesRecords


class TimeSeriesRecordsTest(unittest.TestCase):
    def setUp(self):
        self.dates = pd.date_range('2011-02-01', periods=50, freq='H')
        self.vals = np.random.randn(len(self.dates))
        self.ts = TimeSeriesRecords(self.dates, self.vals)

    def test_init_empty_serie(self):
        new_serie = TimeSeriesRecords()
        new_serie.set_time_serie_values(self.dates, self.vals)
        self.assertEqual(new_serie.value.all(), self.ts.value.all())

    def test_get_one_record_by_date(self):
        self.assertEqual(len([self.ts.get_data_at_time(datetime.datetime(2011, 2, 2))]), 1)
        with self.assertRaises(KeyError) as context:
            self.ts.get_data_at_time(datetime.datetime(2014, 10, 3, 15, 30))
            self.assertTrue('2014-10-03 15:30:00' in str(context.msg))

    def test_get_multiple_record_by_date(self):
        multiple_record = self.ts.get_data_at_time(datetime.datetime(2011, 2, 2).date())
        anticipated_response = self.ts.value['2011-02-02']
        self.assertEqual(multiple_record.all(), anticipated_response.all())

    def test_get_datas_between(self):
        d_from = 2
        d_to = 4

        getted_record = self.ts.get_data_between(self.dates[d_from], self.dates[d_to])
        anticipated_values = pd.Series(self.vals[d_from:d_to + 1], self.dates[d_from:d_to + 1])
        self.assertEqual(getted_record.all(), anticipated_values.all())

    def test_get_data_after(self):
        d_after = 3
        getted_records = self.ts.get_data_after_date(self.dates[d_after])
        anticipated_values = pd.Series(self.vals[d_after:], self.dates[d_after:])
        self.assertEqual(getted_records.all(), anticipated_values.all())

    def test_get_data_before(self):
        d_before = 3
        getted_records = self.ts.get_data_before_date(self.dates[d_before])
        anticipated_values = pd.Series(self.vals[:d_before + 1], self.dates[:d_before + 1])
        self.assertEqual(getted_records.all(), anticipated_values.all())

    def test_get_data_between_bad_interval(self):
        d_from = 4
        d_to = 2
        first_date = self.dates[d_from]
        last_date = self.dates[d_to]
        ts = self.ts.get_data_between(first_date, last_date)
        self.assertTrue(ts.all() == pd.Series(self.vals[d_to:d_from], index=self.dates[d_to:d_from]).all())



    def test_get_data_before_not_in_values(self):
        date_before = self.dates[0]
        date_before = datetime.datetime(date_before.year - 1, date_before.month, date_before.day)
        getted_dates = self.ts.get_data_before_date(date_before)
        self.assertTrue(len(getted_dates) == 0)

    def test_get_data_after_not_in_values(self):
        date_after = self.dates[-1]
        date_after = datetime.datetime(date_after.year+1,date_after.month, date_after.day)
        getted_dates = self.ts.get_data_after_date(date_after)
        self.assertTrue(len(getted_dates) == 0)


suite = unittest.TestLoader().loadTestsFromTestCase(TimeSeriesRecordsTest)
unittest.TextTestRunner(verbosity=2).run(suite)

