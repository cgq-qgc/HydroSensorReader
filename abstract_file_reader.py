#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-05-01'
__description__ = " "
__version__ = '1.0'


from abc import ABCMeta, abstractmethod




class FileReader(metaclass=ABCMeta):
    """
    classe permettant d'extraire des données d'un fichier quelconque.
    Un fichier de donnée est en général composé de :
    - Entete d'information sur l'environnement de prise de données
    - Entete d'information sur les colonnes de données
    - Les colonnes de données
    """
    FILE_HEADER = 'file_header'
    FILE_DATA_HEADER = 'file_data_header'
    FILE_DATA = 'file_data'

    def __init__(self, file_name: str = None):
        """

        :param file_name: string représentant l'emplacement/nom du fichier à ouvrir      
        """
        self._file_name = file_name
        self._file_content = None
        self.__file_internal_data = {self.FILE_HEADER:{}, self.FILE_DATA_HEADER:{}, self.FILE_DATA:None}

        self._load_file()


    def _validate_file(self) -> bool:
        """
        Methode pemettant de valider un fichier.
        Celui-ci ne doit pas être NONE et doit contenir l'extension désirée
        :return: 
        """
        return self._file_name is not None and self._validate_file_type

    @abstractmethod
    def _validate_file_type(self) -> bool:
        pass

    def _load_file(self):
        """
        Méthode permettant d'ouvrir un fichier et de mettre à jour l'information de la classe
        :return: None
        """
        if self._validate_file():
            self.open_file()
            self.read_file_header()
            self.read_file_data_header()
            self.read_file_data()

    @abstractmethod
    def open_file(self):
        """
        Methode permettant d'ouvrir le fichier selon une méthode appropriée. Le fichier peut être en txt, xml ou autre,
        cette methode doit servir à ouvrir celui-ci et de stocker l'information contenu dans l'attibut 
        self._file_content
        :return: None
        """
        pass

    @abstractmethod
    def read_file_header(self):
        """
        Methode permettant de lire l'entete du fichier
        :return: 
        """
        pass

    @abstractmethod
    def read_file_data_header(self):
        """
        Methode permettant de lire l'entete des colonnes de donnees
        :return: 
        """
        pass


    @abstractmethod
    def read_file_data(self):
        """
        Methode pour ne recupérer que les donnees du fichier
        :return: 
        """
        pass


    @property
    def file_header(self):
        return self.__file_internal_data[self.FILE_HEADER]

    @file_header.setter
    def file_header(self, value):
        self.__file_internal_data[self.FILE_HEADER] = value

    @property
    def file_data_header(self):
        return self.__file_internal_data[self.FILE_DATA_HEADER]

    @file_data_header.setter
    def file_data_header(self, value):
        self.__file_internal_data[self.FILE_DATA_HEADER] = value

    @property
    def file_data(self):
        return self.__file_internal_data[self.FILE_DATA]

    @file_data.setter
    def file_data(self, value):
        self.__file_internal_data[self.FILE_DATA] = value

