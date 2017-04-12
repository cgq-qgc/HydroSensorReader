#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-04-11'
__description__ = " "
__version__ = '1.0'

from PyQt4 import QtGui

from elem_controller.sampling_feature_controller import Sampling_features_controller_Singleton
from gui_controller.om.om_sampling_feature_gui_controller import Om_sampling_feature_gui_controller
from gui_controller.om.om_specimen_gui_controller import Om_specimen_gui_controller


class WidgetSpecimenAndSamplingFeature(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WidgetSpecimenAndSamplingFeature, self).__init__(parent)
        self.gui_specimen = Om_specimen_gui_controller(self)
        self.gui_sampling_feature = Om_sampling_feature_gui_controller(self)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.gui_sampling_feature)
        hbox.addWidget(self.gui_specimen)
        self.setLayout(hbox)
        self.gui_sampling_feature.setMaximumWidth(self.width() / 2)
        self.specimen_foi_id = Sampling_features_controller_Singleton().create_specimen()
        self.specimen = Sampling_features_controller_Singleton().get_sampling_feature_by_foi_id(self.specimen_foi_id)
        self.gui_sampling_feature.label_foi_id.setText(
            self.gui_sampling_feature.label_foi_id + str(self.specimen_foi_id))


if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    from database.database_tester.database_content_tester import dataBaseTester

    dataBaseTester()

    app = QtGui.QApplication(sys.argv)

    fenete = WidgetSpecimenAndSamplingFeature()
    fenete.show()
    sys.exit(app.exec_())
