# -*- coding: utf8 -*-
__author__ = "Xavier"
__date__ = '2017-04-10'
__description__ = ""
__version__ = '0.0.1'

from PyQt4 import QtCore

from controller.sampling_feature_controller import Sampling_features_controller_Singleton as SF_control
from gui.python_ui.ui_find_parent import Ui_Form
from gui_controller.abstract_pyqt_controller import AbstractPyQTController


class Om_find_parent_gui_controller(AbstractPyQTController, Ui_Form):
    def __init__(self, parent=None, p_foi_id=None):
        super(Om_find_parent_gui_controller, self).__init__(parent)
        self.setupUi(self)
        self.finded_element = {}
        self.foi_id = p_foi_id
        self.sampling_feature = SF_control().get_sampling_feature_by_foi_id(p_foi_id)

        self.connect_element()
        self.fill_relation_combo_box()

    def validateEntry(self):
        pass

    def connect_element(self):

        self.LE_text_to_search.textChanged.connect(self.find_sampling_feature)
        self.CB_finded_element.currentIndexChanged.connect(self.update_parent_foi_id)
        self.CB_relation_type.currentIndexChanged.connect(self.update_relation_type)

    def update_relation_type(self):
        self.relation_type = self.CB_relation_type.currentText().split(" - ")[0]

    def update_parent_foi_id(self):
        self.sampling_feature.sampling_context.parent_foi_id = self.finded_element[self.CB_finded_element.currentText()][0]

    def find_sampling_feature(self):
        self.CB_finded_element.currentIndexChanged.disconnect(self.update_parent_foi_id)
        self.finded_element.clear()
        self.CB_finded_element.clear()
        if len(self.LE_text_to_search.text()) >= 3:
            sample_list = []
            if int(self.CB_relation_type.currentText().split(" - ")[0] ) in (4,5):
                sample_list = SF_control().controller.find_spatial_sampling_feature_by_name(self.LE_text_to_search.text())
            else:
                sample_list = SF_control().controller.find_sampling_feature_by_name(self.LE_text_to_search.text())

            for samp_feat in sample_list:
                self.finded_element[samp_feat[1]] = samp_feat
                self.finded_sampling_feature = samp_feat[1]
        self.CB_finded_element.currentIndexChanged.connect(self.update_parent_foi_id)

    def fill_relation_combo_box(self):
        for p_type, desc, abb in SF_control().controller.get_sampling_context_relation_type():
            self.context_relation = "{} - {}".format(p_type, desc)

    @property
    def context_relation(self):
        return str(self.CB_relation_type.currentText())

    @context_relation.setter
    def context_relation(self, value):
        self.CB_relation_type.addItem(str(value))
        # Adding a line tooltip
        self.CB_relation_type.setItemData(self.CB_relation_type.count() - 1,
                                          str(value),
                                          QtCore.Qt.ToolTipRole)
        # Updating the tooltip text
        texte_tooltip = ""
        for index in range(self.CB_relation_type.count()):
            self.CB_relation_type.setCurrentIndex(index)
            texte_tooltip += self.CB_relation_type.currentText() + "\n"
        self.CB_relation_type.setToolTip(str(texte_tooltip))
        self.CB_relation_type.setCurrentIndex(0)

    @property
    def finded_sampling_feature(self):
        return str(self.CB_finded_element.currentText())

    @finded_sampling_feature.setter
    def finded_sampling_feature(self, value):
        self.CB_finded_element.addItem(str(value))
        # Adding a line tooltip
        self.CB_finded_element.setItemData(self.CB_finded_element.count() - 1,
                                           str(value),
                                           QtCore.Qt.ToolTipRole)
        # Updating the tooltip text
        texte_tooltip = ""
        for index in range(self.CB_finded_element.count()):
            self.CB_finded_element.setCurrentIndex(index)
            texte_tooltip += self.CB_finded_element.currentText() + "\n"
        self.CB_finded_element.setToolTip(str(texte_tooltip))
        self.CB_finded_element.setCurrentIndex(0)


if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    from database.database_tester.database_content_tester import dataBaseTester

    dataBaseTester()

    app = QtGui.QApplication(sys.argv)

    fenete = Om_find_parent_gui_controller()
    fenete.show()
    sys.exit(app.exec_())
