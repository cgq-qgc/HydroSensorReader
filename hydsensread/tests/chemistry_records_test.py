#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-14$'
__description__ = " "
__version__ = '1.0'

import itertools
import math
import unittest

from hydsensread.site_and_records.records import ChemistryRecord


class ChemistryRecordsTest(unittest.TestCase):
    def setUp(self):
        self.chem_rec = ChemistryRecord()

    def test_normalized_value_trace_and_nd(self):
        not_detected = ['trace','Trace','tr','tr.','Tr',
                        'nd','ND','n.d','not detected',
                        'nan','NaN']
        for result in not_detected:
            # set value
            self.chem_rec.value = result
            # must return a NaN since ChemistryRecord.lower_detection_limit is None
            self.assertTrue(math.isnan(self.chem_rec.normalized_value))
            # set ChemistryRecord.lower_detection_limit to a value
            self.chem_rec.lower_detection_limit = 0.5
            self.assertTrue(self.chem_rec.normalized_value == self.chem_rec.lower_detection_limit/2.0)
            self.chem_rec.lower_detection_limit = None

    def test_normalized_value_below_detection_limit(self):

        below_values = ['< {}','<{}',' < {}',' <{}']
        for vals in below_values:
            for j,i in zip(range(20),itertools.count(1,float(0.5))):
                self.chem_rec.value = vals.format(float(i))
                self.assertEqual(self.chem_rec.normalized_value,i/2.0)

    def test_normalized_value_juste_the_value(self):
        for i,j in zip(range(20),itertools.count(1,0.5)):
            self.chem_rec.value = str(j)
            self.assertEqual(self.chem_rec.normalized_value,j)

suite = unittest.TestLoader().loadTestsFromTestCase(ChemistryRecordsTest)
unittest.TextTestRunner(verbosity=2).run(suite)
