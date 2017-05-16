# -*- coding: utf8 -*-
__author__ = "Xavier"
__date__ = '2017-04-10'
__description__ = ""
__version__ = '0.0.1'
import datetime
import re

from PyQt4 import QtCore

from controller.sampling_feature_controller import Sampling_features_controller_Singleton as SF_Control
from gui.python_ui.ui_sampling_feature_toolbox import Ui_Form
from gui_controller.abstract_pyqt_controller import AbstractPyQTController


class Om_sampling_feature_gui_controller(AbstractPyQTController, Ui_Form):
    def __init__(self, parent=None):
        super(Om_sampling_feature_gui_controller, self).__init__(parent)
        self.sampling_feature = None
        self.fill_all_combo()
        self.set_date()
        self.groupbox_specimen.setMaximumHeight(20)
        self.finded_element = {}
        self.fill_relation_combo_box()

    def connect_element(self):
        self.setupUi(self)
        self.groupbox_specimen.clicked.connect(self.set_groupbox_specimen)
        self.LE_text_to_search.textChanged.connect(self.find_sampling_feature)
        self.LE_text_to_search.returnPressed.connect(self.line_edit_find_sampling_feature)
        self.CB_finded_element.currentIndexChanged.connect(self.update_parent_foi_id)
        self.CB_relation_type.currentIndexChanged.connect(self.update_relation_type)

    def set_groupbox_specimen(self):
        if self.LE_text_to_search.isEnabled():
            self.groupbox_specimen.setMaximumHeight(16574)
            self.radio_relative_loc.setEnabled(True)
            self.radio_geographique_loc.setChecked(False)
        else:
            self.groupbox_specimen.setMaximumHeight(20)
            self.radio_geographique_loc.setChecked(True)
            self.radio_relative_loc.setEnabled(False)

    def fill_all_combo(self):
        self.fill_process_type()
        self.fill_reference()
        self.fill_sample_feature_type()

    def validateEntry(self):
        return self.validate_sampling_name() == True and \
               self.validate_id_bd_extern() == True and \
               self.validate_combo_box() == True

    def validate_id_bd_extern(self):
        return self.gb_id_bd_extern.isChecked() == True and self.LE_id_bd_extern.text() not in ['', ' ', None]

    def validate_sampling_name(self):
        return self.get_sampling_name() not in ['', ' ', None] and \
               len(self.get_sampling_name()) > 0 and \
               len(self.get_sampling_name().replace(' ', '')) > 0 and \
               re.search(r"^\S*", self.get_sampling_name()) != None

    def validate_date(self):
        return self.get_date() <= datetime.datetime.now()

    def validate_combo_box(self):
        return self.references != " -- " and self.sample_interet != " -- "

    def fill_reference(self):
        references = SF_Control().get_references_for_user()
        self.references = " -- "
        for ref in references:
            self.references = "{} - {}".format(ref.ref_id, ref.ref_titre)

    def fill_sample_feature_type(self):
        self.CB_interet.clear()
        self.sample_interet = " -- "
        interets = SF_Control().get_sample_interet()
        for interet in interets:
            self.sample_interet = "{} - {}".format(interet.interet_id, interet.interet_desc)

    def fill_process_type(self):
        try:
            self.CB_process_type.currentIndexChanged.disconnect(self.update_process_desc)
        except:
            pass
        self.CB_process_type.clear()
        self.process_type = " -- "
        for process in SF_Control().get_process_type():
            self.process_type = process

        self.CB_process_type.currentIndexChanged.connect(self.update_process_desc)
        self.update_process_desc()

    def update_process_desc(self):
        self.label_proces_desc.setWordWrap(True)
        process_type = self.process_type
        if process_type != " -- ":
            try:
                self.CB_process.currentIndexChanged.disconnect(self.update_process_label)
            except:
                pass
            self.CB_process.clear()
            self.process_description = " -- "
            print(process_type)
            for process in SF_Control().get_process_by_categorie(process_type):
                self.process_description = "{} - {}".format(process[0], process[1].split("\\n")[0])
            self.CB_process.currentIndexChanged.connect(self.update_process_label)
        self.update_process_label()

    def update_process_label(self):
        if self.process_description != " -- " and self.process_description != '':
            process_desc = SF_Control().get_process_description_by_process_id_and_category(self.process_type,
                                                                                           self.get_process_id())
            self.label_proces_desc.setText(process_desc.replace("\\n", "\n"))
        else:
            self.label_proces_desc.setText("")

    def set_date(self):
        self.DTE_sampling_date.setDateTime(datetime.datetime.now())

    def get_date(self):
        return datetime.datetime.strptime(self.DTE_sampling_date.text(), '%Y-%m-%d %H:%M:%S')

    def get_sampling_name(self):
        return self.LE_sampling_name.text()

    def get_process_id(self):
        if self.process_description != " -- " and self.process_description != '':
            return int(self.process_description.split(" - ")[0])
        else:
            return None

    def update_sampling_feature(self):
        if self.validateEntry() == True:
            pass

    @property
    def process_type(self):
        return str(self.CB_process_type.currentText())

    @process_type.setter
    def process_type(self, value):
        self.CB_process_type.addItem(str(value))
        # Adding a line tooltip
        self.CB_process_type.setItemData(self.CB_process_type.count() - 1,
                                         str(value),
                                         QtCore.Qt.ToolTipRole)
        # Updating the tooltip text
        texte_tooltip = ""
        for index in range(self.CB_process_type.count()):
            self.CB_process_type.setCurrentIndex(index)
            texte_tooltip += self.CB_process_type.currentText() + "\n"
        self.CB_process_type.setToolTip(str(texte_tooltip))
        self.CB_process_type.setCurrentIndex(0)

    @property
    def process_description(self):
        return str(self.CB_process.currentText())

    @process_description.setter
    def process_description(self, value):
        self.CB_process.addItem(str(value))
        # Adding a line tooltip
        self.CB_process.setItemData(self.CB_process.count() - 1,
                                    str(value),
                                    QtCore.Qt.ToolTipRole)
        # Updating the tooltip text
        texte_tooltip = ""
        for index in range(self.CB_process.count()):
            self.CB_process.setCurrentIndex(index)
            texte_tooltip += self.CB_process.currentText() + "\n"
        self.CB_process.setToolTip(str(texte_tooltip))
        self.CB_process.setCurrentIndex(0)

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

    def update_relation_type(self):
        self.relation_type = self.CB_relation_type.currentText().split(" - ")[0]

    def update_parent_foi_id(self):
        print(self.finded_element[self.CB_finded_element.currentText()][0])
        self.sampling_feature.sampling_context.parent_foi_id = \
            self.finded_element[self.CB_finded_element.currentText()][0]

    def find_sampling_feature(self):
        if len(self.LE_text_to_search.text()) >= 4:
            self.line_edit_find_sampling_feature()

    def line_edit_find_sampling_feature(self):
        self.CB_finded_element.currentIndexChanged.disconnect(self.update_parent_foi_id)
        self.finded_element.clear()
        self.CB_finded_element.clear()
        sample_list = SF_Control().get_sampling_feature_by_name(self.LE_text_to_search.text())
        for samp_feat in sample_list:
            self.finded_element[samp_feat[1]] = samp_feat
            self.finded_sampling_feature = samp_feat[1]
        self.CB_finded_element.currentIndexChanged.connect(self.update_parent_foi_id)

    def fill_relation_combo_box(self):
        for p_type, desc, abb in SF_Control().get_sampling_context_relation_type_for_specimen():
            self.context_relation = "{} - {}".format(p_type, desc)
        for i in range(self.CB_relation_type.count()):
            self.CB_relation_type.setCurrentIndex(i)
            if self.context_relation.split(" - ")[0] == str(5):
                break

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
    from database.database_tester.database_content_tester import DataBaseTesterSingleton

    DataBaseTesterSingleton()

    app = QtGui.QApplication(sys.argv)

    fenete = Om_sampling_feature_gui_controller()

    fenete.show()
    sys.exit(app.exec_())
