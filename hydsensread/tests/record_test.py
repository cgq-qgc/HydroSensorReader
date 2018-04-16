#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-13$'
__description__ = " "
__version__ = '1.0'

import datetime
import unittest

from hydsensread.site_and_records.records import Record


class Recordtest(unittest.TestCase):
    def setUp(self):
        self.rec = Record()

    def test_set_parameter(self):
        self.rec.parameter = 'test param'
        self.rec.parameter_unit = 'mg/L'
        self.assertEqual(self.rec.parameter, 'test param')
        self.assertEqual(self.rec.parameter_unit,'mg/L')

    def test_set_value(self):
        self.rec.value = 12
        self.assertEqual(self.rec.value,12)

    def test_set_record_date(self):
        now = datetime.datetime.now()
        self.rec.record_date = now
        self.assertEqual(self.rec.record_date, now)

suite = unittest.TestLoader().loadTestsFromTestCase(Recordtest)
unittest.TextTestRunner(verbosity=2).run(suite)
