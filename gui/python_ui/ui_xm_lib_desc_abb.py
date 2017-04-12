# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'U:\Programmation\HydroHackOp\gui\pyqt_ui\om\xm_lib_desc_abb.ui'
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
        Form.resize(300, 171)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_lib = QtGui.QGroupBox(Form)
        self.groupBox_lib.setObjectName(_fromUtf8("groupBox_lib"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_lib)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_desc = QtGui.QLabel(self.groupBox_lib)
        self.label_desc.setMinimumSize(QtCore.QSize(0, 20))
        self.label_desc.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_desc.setObjectName(_fromUtf8("label_desc"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label_desc)
        self.LE_samp_type_desc = QtGui.QLineEdit(self.groupBox_lib)
        self.LE_samp_type_desc.setObjectName(_fromUtf8("LE_samp_type_desc"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.LE_samp_type_desc)
        self.label_abb = QtGui.QLabel(self.groupBox_lib)
        self.label_abb.setObjectName(_fromUtf8("label_abb"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.label_abb)
        self.LE_samp_type_abb = QtGui.QLineEdit(self.groupBox_lib)
        self.LE_samp_type_abb.setObjectName(_fromUtf8("LE_samp_type_abb"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.LE_samp_type_abb)
        self.btn_box_ok_cancel = QtGui.QDialogButtonBox(self.groupBox_lib)
        self.btn_box_ok_cancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btn_box_ok_cancel.setObjectName(_fromUtf8("btn_box_ok_cancel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.btn_box_ok_cancel)
        self.verticalLayout_2.addWidget(self.groupBox_lib)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox_lib.setTitle(_translate("Form", "Créer un nouveau type", None))
        self.label_desc.setText(_translate("Form", "Description du type  (0/250 caract)", None))
        self.label_abb.setText(_translate("Form", "Abbreviation utilisée (0/15 caract)", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

