# -*- coding: utf8 -*-
__author__ = "Xavier"
__date__ = '2017-04-10'
__description__ = ""
__version__ = '0.0.1'
import datetime
import re

from PyQt4 import QtCore, QtGui
from gui.python_ui.om.ui_specimen import Ui_Form
from gui_controller.abstract_pyqt_controller import AbstractPyQTController


class Om_specimen_gui_controller(AbstractPyQTController, Ui_Form):
    def __init__(self, parent=None):
        super(Om_specimen_gui_controller, self).__init__(parent)
        self.setupUi(self)

    def get_specimen_material(self):
        pass
    def get_specimen_size(self):
        pass
    def make_specimen_size(self):
        pass
    def make_new_xyz_coordinate(self):
        pass

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    
    fenete = Om_specimen_gui_controller()
    fenete.show()
    sys.exit(app.exec_())