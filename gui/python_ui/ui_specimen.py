# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'U:\Programmation\HydroHackOp\gui\pyqt_ui\om\specimen.ui'
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
        Form.resize(330, 385)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupbox_specimen = QtGui.QGroupBox(Form)
        self.groupbox_specimen.setObjectName(_fromUtf8("groupbox_specimen"))
        self.formLayout = QtGui.QFormLayout(self.groupbox_specimen)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupbox_specimen)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label)
        self.CB_spe_material = QtGui.QComboBox(self.groupbox_specimen)
        self.CB_spe_material.setObjectName(_fromUtf8("CB_spe_material"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.CB_spe_material)
        self.label_2 = QtGui.QLabel(self.groupbox_specimen)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.label_2)
        self.LE_current_loc = QtGui.QLineEdit(self.groupbox_specimen)
        self.LE_current_loc.setObjectName(_fromUtf8("LE_current_loc"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.LE_current_loc)
        self.label_3 = QtGui.QLabel(self.groupbox_specimen)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.label_3)
        self.LE_Size_qt = QtGui.QLineEdit(self.groupbox_specimen)
        self.LE_Size_qt.setObjectName(_fromUtf8("LE_Size_qt"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.LE_Size_qt)
        self.CB_size_unit = QtGui.QComboBox(self.groupbox_specimen)
        self.CB_size_unit.setObjectName(_fromUtf8("CB_size_unit"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.CB_size_unit)
        self.label_4 = QtGui.QLabel(self.groupbox_specimen)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_4)
        self.CB_sample_type = QtGui.QComboBox(self.groupbox_specimen)
        self.CB_sample_type.setObjectName(_fromUtf8("CB_sample_type"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.SpanningRole, self.CB_sample_type)
        self.GB_spe_loc = QtGui.QGroupBox(self.groupbox_specimen)
        self.GB_spe_loc.setMinimumSize(QtCore.QSize(0, 125))
        self.GB_spe_loc.setCheckable(True)
        self.GB_spe_loc.setObjectName(_fromUtf8("GB_spe_loc"))
        self.formLayout_2 = QtGui.QFormLayout(self.GB_spe_loc)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_5 = QtGui.QLabel(self.GB_spe_loc)
        self.label_5.setMinimumSize(QtCore.QSize(0, 18))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.GB_spe_loc)
        self.label_6.setMinimumSize(QtCore.QSize(0, 18))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_6)
        self.LE_spe_from = QtGui.QLineEdit(self.GB_spe_loc)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LE_spe_from.sizePolicy().hasHeightForWidth())
        self.LE_spe_from.setSizePolicy(sizePolicy)
        self.LE_spe_from.setMinimumSize(QtCore.QSize(0, 18))
        self.LE_spe_from.setSizeIncrement(QtCore.QSize(4, 0))
        self.LE_spe_from.setObjectName(_fromUtf8("LE_spe_from"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.LE_spe_from)
        self.LE_spe_to = QtGui.QLineEdit(self.GB_spe_loc)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LE_spe_to.sizePolicy().hasHeightForWidth())
        self.LE_spe_to.setSizePolicy(sizePolicy)
        self.LE_spe_to.setMinimumSize(QtCore.QSize(0, 18))
        self.LE_spe_to.setSizeIncrement(QtCore.QSize(0, 0))
        self.LE_spe_to.setObjectName(_fromUtf8("LE_spe_to"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.LE_spe_to)
        self.radioButton = QtGui.QRadioButton(self.GB_spe_loc)
        self.radioButton.setMinimumSize(QtCore.QSize(0, 18))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.SpanningRole, self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.GB_spe_loc)
        self.radioButton_2.setMinimumSize(QtCore.QSize(0, 18))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.SpanningRole, self.radioButton_2)
        self.formLayout.setWidget(9, QtGui.QFormLayout.SpanningRole, self.GB_spe_loc)
        self.btn_create_samp_type = QtGui.QPushButton(self.groupbox_specimen)
        self.btn_create_samp_type.setObjectName(_fromUtf8("btn_create_samp_type"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.SpanningRole, self.btn_create_samp_type)
        self.horizontalLayout.addWidget(self.groupbox_specimen)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupbox_specimen.setTitle(_translate("Form", "Information sur l\'échantillonnage", None))
        self.label.setText(_translate("Form", "Matériel de l\'échantillon", None))
        self.label_2.setText(_translate("Form", "Emplacement courant de l\'échantillon", None))
        self.label_3.setText(_translate("Form", "Taille de l\'échantillon", None))
        self.label_4.setText(_translate("Form", "Type d\'échantillon", None))
        self.GB_spe_loc.setTitle(_translate("Form", "Entrer une localisation spécifique de l\'échantillon", None))
        self.label_5.setText(_translate("Form", "De - (m)", None))
        self.label_6.setText(_translate("Form", "A - (m)", None))
        self.radioButton.setText(_translate("Form", "position de - a", None))
        self.radioButton_2.setText(_translate("Form", "Coordonnée géographique propre", None))
        self.btn_create_samp_type.setText(_translate("Form", "Le type d\'échantillon n\'existe pas", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

