# -*- coding: utf8 -*-
__author__ = "Xavier"
__date__ = '2017-04-10'
__description__ = ""
__version__ = '0.0.1'
import datetime
import re

from PyQt4 import QtCore, QtGui
from gui.python_ui.om.ui_spatial_sampling_feature import Ui_Form
from gui_controller.abstract_pyqt_controller import AbstractPyQTController


class Om_spatial_sampling_feature_Controller(AbstractPyQTController, Ui_Form):
    def __init__(self, parent=None):
        super(Om_spatial_sampling_feature_Controller, self).__init__(parent)
        self.setupUi(self)



if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    
    fenete = Om_spatial_sampling_feature_Controller()
    fenete.show()
    sys.exit(app.exec_())