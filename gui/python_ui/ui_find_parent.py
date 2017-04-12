# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'U:\Programmation\ogc_om_interface\gui\pyqt_ui\find_parent.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(251, 233)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupbox_sampling_context = QtGui.QGroupBox(Form)
        self.groupbox_sampling_context.setMinimumSize(QtCore.QSize(0, 215))
        self.groupbox_sampling_context.setCheckable(False)
        self.groupbox_sampling_context.setObjectName(_fromUtf8("groupbox_sampling_context"))
        self.formLayout = QtGui.QFormLayout(self.groupbox_sampling_context)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupbox_sampling_context)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.LE_text_to_search = QtGui.QLineEdit(self.groupbox_sampling_context)
        self.LE_text_to_search.setMinimumSize(QtCore.QSize(0, 20))
        self.LE_text_to_search.setText(_fromUtf8(""))
        self.LE_text_to_search.setObjectName(_fromUtf8("LE_text_to_search"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.LE_text_to_search)
        self.CB_finded_element = QtGui.QComboBox(self.groupbox_sampling_context)
        self.CB_finded_element.setMinimumSize(QtCore.QSize(0, 20))
        self.CB_finded_element.setObjectName(_fromUtf8("CB_finded_element"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.CB_finded_element)
        self.label_2 = QtGui.QLabel(self.groupbox_sampling_context)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.groupbox_sampling_context)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.CB_relation_type = QtGui.QComboBox(self.groupbox_sampling_context)
        self.CB_relation_type.setMinimumSize(QtCore.QSize(0, 20))
        self.CB_relation_type.setObjectName(_fromUtf8("CB_relation_type"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.CB_relation_type)
        self.btn_box_ok_cancel = QtGui.QDialogButtonBox(self.groupbox_sampling_context)
        self.btn_box_ok_cancel.setMinimumSize(QtCore.QSize(0, 20))
        self.btn_box_ok_cancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btn_box_ok_cancel.setObjectName(_fromUtf8("btn_box_ok_cancel"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.btn_box_ok_cancel)
        self.horizontalLayout.addWidget(self.groupbox_sampling_context)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupbox_sampling_context.setTitle(_translate("Form", "Est associé à un autre élément?", None))
        self.label.setText(_translate("Form", "Rechercher élément", None))
        self.LE_text_to_search.setPlaceholderText(_translate("Form", "saisir nom", None))
        self.label_2.setText(_translate("Form", "Éléments trouvés", None))
        self.label_3.setText(_translate("Form", "Type de relation", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

