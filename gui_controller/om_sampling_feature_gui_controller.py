# -*- coding: utf8 -*-
__author__ = "Xavier"
__date__ = '2017-04-10'
__description__ = ""
__version__ = '0.0.1'
import datetime
import re

from PyQt4 import QtCore, QtGui

from gui.python_ui.om.ui_sampling_feature import Ui_Form
from gui_controller.abstract_pyqt_controller import AbstractPyQTController
from database.db_acces_layer.main_access import MainControllerSingleton as MainControl
from om_observation_data_transfert.controller.sampling_feature_db_controller  import SamplingFeaturesSingleton as SF_Control

class Om_sampling_feature_gui_controller(AbstractPyQTController, Ui_Form):
    def __init__(self, parent=None):
        super(Om_sampling_feature_gui_controller, self).__init__(parent)
        self.setupUi(self)
        self.sampling_feature = None
        self.fill_reference()
        self.fill_sample_feature_type()
        self.set_date()

    def fill_reference(self):
        references = MainControl().getReferencesForCurrentProject().fetchall()
        for ref in references:
            self.references = "{} - {}".format(ref.ref_id, ref.ref_titre)

    def fill_sample_feature_type(self):
        self.CB_interet.clear()
        interets = SF_Control().get_sample_interet()
        for interet in interets:
            self.sample_interet = "{} - {}".format(interet.interet_id, interet.interet_desc)

    def set_date(self):
        self.DTE_sampling_date.setDateTime(datetime.datetime.now())

    @property
    def sample_interet(self):
        return str(self.CB_interet.currentText())
    @sample_interet.setter
    def sample_interet(self, value):
        self.CB_interet.addItem(str(value))
        # Adding a line tooltip
        self.CB_interet.setItemData(self.CB_interet.count() - 1,
                                      str(value),
                                      QtCore.Qt.ToolTipRole)
        # Updating the tooltip text
        texte_tooltip = ""
        for index in range(self.CB_interet.count()):
            self.CB_interet.setCurrentIndex(index)
            texte_tooltip += self.CB_interet.currentText() + "\n"
        self.CB_interet.setToolTip(str(texte_tooltip))
        self.CB_interet.setCurrentIndex(0)



    @property
    def references(self):
        return str(self.CB_ref.currentText())


    @references.setter
    def references(self, value):
        self.CB_ref.addItem(str(value))
        # Adding a line tooltip
        self.CB_ref.setItemData(self.CB_ref.count() - 1,
                                      str(value),
                                      QtCore.Qt.ToolTipRole)
        # Updating the tooltip text
        texte_tooltip = ""
        for index in range(self.CB_ref.count()):
            self.CB_ref.setCurrentIndex(index)
            texte_tooltip += self.CB_ref.currentText() + "\n"
        self.CB_ref.setToolTip(str(texte_tooltip))
        self.CB_ref.setCurrentIndex(0)




if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    from database.database_tester.database_content_tester import dataBaseTester

    dataBaseTester()
    
    app = QtGui.QApplication(sys.argv)
    
    fenete = Om_sampling_feature_gui_controller()
    fenete.show()
    sys.exit(app.exec_())
