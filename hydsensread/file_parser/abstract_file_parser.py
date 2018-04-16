#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Laptop$'
__date__ = '2017-07-11$'
__description__ = " "
__version__ = '1.0'

import typing
from abc import abstractmethod, ABCMeta

import bs4


class AbstractFileParser(object, metaclass=ABCMeta):
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
    def get_file_content(self) -> typing.Union[bs4.BeautifulSoup, list]:
        return self._file_content

    @property
    def get_file_header(self) -> typing.Union[bs4.BeautifulSoup, typing.List[str]]:
        if len(self._file_header_content) > 0:
            return self._file_header_content
        else:
            return self._file_content[0: self._header_length]
