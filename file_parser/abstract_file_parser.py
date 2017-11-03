#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-11$'
__description__ = " "
__version__ = '1.0'

from abc import abstractmethod


class AbstractFileParser(object):
    def __init__(self, file_path: str = None, header_length: int = None):
        self._file = file_path
        self._header_length = header_length
        self._file_content = []
        self._file_header_content = []

    @abstractmethod
    def read_file_header(self):
        pass

    @abstractmethod
    def read_file(self):
        pass

    @property
    def get_file_content(self):
        return self._file_content

    @property
    def get_file_header(self):
        return self._file_header_content
