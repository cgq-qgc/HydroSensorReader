#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-14$'
__description__ = " "
__version__ = '1.0'

import unittest
import datetime

class ChemistryRecordsTest(unittest.TestCase):
    def setUp(self):
        super(ChemistryRecordsTest, self).setUp()

    def test_something(self):
        self.assertEqual(True, False)

suite = unittest.TestLoader().loadTestsFromTestCase(ChemistryRecordsTest)
unittest.TextTestRunner(verbosity=2).run(suite)
