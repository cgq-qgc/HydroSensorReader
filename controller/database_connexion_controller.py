#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-04-24'
__description__ = " "
__version__ = '1.0'
from controller.pyqt_connector.PostgresqlConnector import PLSQL_pyqt_thread

class DatabaseConnector(object):
    def __init__(self):
        self._connector = PLSQL_pyqt_thread()

    def connectToDatabase(self, userName, passWord):
        """
        Méthode pas forcement nécessaire. Pourrait être déplacée ailleur
        :param userName: 
        :param passWord: 
        :return: 
        """
        self._connector.setUser(userName, passWord)
        self._connector.start()
