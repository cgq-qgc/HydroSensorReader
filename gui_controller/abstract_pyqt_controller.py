# -*- coding: utf8 -*-
__author__ = "Xavier"
__date__ = '2017-04-10'
__description__ = ""
__version__ = '0.0.1'

from PyQt4 import QtCore, QtGui
from abc import abstractmethod

class AbstractPyQTController(QtGui.QWidget):
    def __init__(self, parent):
        super(AbstractPyQTController, self).__init__(parent)
    @abstractmethod
    def connect_element(self):
        pass
    @abstractmethod
    def validateEntry(self):
        pass
    
    def closeEvent(self, event):
        return QtGui.QWidget.closeEvent(self, event)
    



        