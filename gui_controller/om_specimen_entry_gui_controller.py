# -*- coding: utf8 -*-
__author__ = "Xavier"
__date__ = '2017-04-10'
__description__ = ""
__version__ = '0.0.1'
import datetime
import re

from PyQt4 import QtCore, QtGui
from gui.python_ui.om.ui_specimen_entry import Ui_Form
from gui_controller.abstract_pyqt_controller import AbstractPyQTController

from gui_controller.om.om_sampling_feature_gui_controller import Om_sampling_feature_gui_controller
from gui_controller.om.om_specimen_controller import Om_specimen_gui_controller

from om_observation_data_transfert.controller.sampling_feature_controller import SamplingFeaturesSingleton as SF_control
from gui_controller.om.om_find_parent_gui_controller import Om_find_parent_gui_controller

class Om_specimen_entry_gui_controller(AbstractPyQTController, Ui_Form):
    def __init__(self, parent=None):
        super(Om_specimen_entry_gui_controller, self).__init__(parent)
        self.setupUi(self)
        # self.make_new_specimen_entry()
        self.sample_type = None
        self.sample_type_id = None
        self.connect_element()
    def connect_element(self):
        self.btn_add_spec.clicked.connect(self.make_new_specimen_entry)

    def validateEntry(self):
        pass

    def get_sample_type(self) -> int:
        try:
            dial = dialog_get_sample_type(self)
            dial.exec_()
            self.sample_type = dial.texte[1]
            self.sample_type_id = dial.texte[0]
            return True
        except:
            return False

    def make_new_specimen_entry(self):

        # create elements
        frame = QtGui.QFrame()
        vbox = QtGui.QHBoxLayout(frame)
        new_sampling_feat = Om_sampling_feature_gui_controller()
        new_specimen = Om_specimen_gui_controller()
        vbox.addWidget(new_sampling_feat)
        vbox.addWidget(new_specimen)
        # set element
        for i in range(new_sampling_feat.CB_interet.count()):
            new_sampling_feat.CB_interet.setCurrentIndex(i)
            if new_sampling_feat.CB_interet.currentText().split(" - ")[0] == '11':
                new_sampling_feat.CB_interet.setEnabled(False)
                break


    def create_new_specimen(self):
        if self.get_sample_type():

            self.make_new_specimen_entry()


    def get_parent(self,sample_type):
        print(sample_type)
        if int(sample_type) == 5:
            dial = QtGui.QDialog(self)
            print("show")
            parent_finder = Om_find_parent_gui_controller(dial)
            for i in range(parent_finder.CB_relation_type.count()):
                parent_finder.CB_relation_type.setCurrentIndex(i)
                if parent_finder.CB_relation_type.currentText().split(" - ")[0] == sample_type:
                    parent_finder.CB_relation_type.setEnabled(False)
                    break

            dial.exec_()


class dialog_get_sample_type(QtGui.QDialog):
    def __init__(self,parent):
        super(dialog_get_sample_type, self).__init__(parent)
        self.texte = ""
        self.radio_list = []
        layout = QtGui.QVBoxLayout(self)
        for p_type,desc,abb in SF_control().get_sampling_context_relation_type_for_specimen():
            btn = QtGui.QRadioButton("{} - {}".format(p_type,desc))
            self.radio_list.append(btn)

        for btn in self.radio_list:
            layout.addWidget(btn)
            btn.clicked.connect(self.setText)



    def setText(self):
        for radio in self.radio_list:
            if radio.isChecked() == True:
                self.texte = radio.text().split(" - ")
                self.close()

if __name__ == '__main__':
    
    import sys
    from PyQt4 import QtGui
    from database.database_tester.database_content_tester import dataBaseTester

    dataBaseTester()
    
    app = QtGui.QApplication(sys.argv)
    
    fenete = Om_specimen_entry_gui_controller()
    fenete.show()
    fenete.btn_add_spec.click()
    sys.exit(app.exec_())