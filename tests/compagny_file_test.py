#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sensor_file.compagny_file import CompagnyFile
import unittest



class CompagnyFileTest(unittest.TestCase):
    def setUp(self):
        super(CompagnyFileTest, self).setUp()
        self.cmp_file = None


    def test_get_file_ext_work(self):
        file_path = "C:\\Users\\laptop\\Documents\\Programmation\\scientific_file_reader\\file_example\\2026236_F4_20160222_2016_06_24.xle"
        self.cmp_file = CompagnyFile(file_name=file_path)
        self.assertTrue(self.cmp_file.get_file_extension(),'xle')
        file_path = "C:\\Users\\laptop\\Documents\\Programmation\\scientific_file_reader\\file_example\\F2_20160223.lev"
        self.cmp_file = CompagnyFile(file_name=file_path)
        self.assertTrue(self.cmp_file.get_file_extension(),'lev')
        self.assertFalse(self.cmp_file.get_file_extension()=='xle')

    def test_get_file_ext_not_work(self):
        file_path = "C:\\Users\\laptop\\Documents\\Programmation\\scientific_file_reader\\file_example"
        self.cmp_file = CompagnyFile(file_name=file_path)

        with self.assertRaises(ValueError ) as context:
            self.cmp_file.get_file_extension()
        self.assertTrue('point to a file' in str(context.exception))

        file_path = "C:\\Users\\laptop\\Documents\\Programmation\\scientific_file_reader\\file_example.xls.pdf"
        self.cmp_file = CompagnyFile(file_name=file_path)
        with self.assertRaises(ValueError ) as context:
            self.cmp_file.get_file_extension()
        self.assertTrue('Too much file ext' in str(context.exception))

suite = unittest.TestLoader().loadTestsFromTestCase(CompagnyFileTest)
unittest.TextTestRunner(verbosity=2).run(suite)