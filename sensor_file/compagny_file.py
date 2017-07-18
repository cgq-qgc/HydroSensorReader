#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-07$'
__description__ = " "
__version__ = '1.0'

class CompagnyFile(object):
    def __init__(self, compagny_name = None, file_name:str = None):
        self.compagny_name = compagny_name
        self.file_name = file_name
        self.file_reader = None

    def open_file_and_set_reader(self):
        with open(self.file_name) as file:
            buf = file.readline()
            i = 0
            while i < 10:
                i += 1
                print(buf)
                buf = file.readline()

    def get_file_extension(self):
        file_list = self.file_name.split(".")
        if len(file_list)== 1:
            raise ValueError("The path given doesn't point to a file name")
        if len(file_list) > 2:
            raise ValueError("The file name seems to be corrupted. Too much file extension in the current name")
        else:
            return file_list[len(file_list)-1]


if __name__ == '__main__':
    file_path = "C:\\Users\\laptop\\Documents\\Programmation\\scientific_file_reader\\file_example\\2026236_F4_20160222_2016_06_24.xle"
    cmp = CompagnyFile(file_name=file_path)
    cmp.open_file_and_set_reader()