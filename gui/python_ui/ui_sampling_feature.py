# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'U:\Programmation\HydroHackOp\gui\pyqt_ui\om\sampling_feature.ui'
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
        Form.resize(424, 365)
        Form.setMinimumSize(QtCore.QSize(275, 365))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupbox_sampling_feature = QtGui.QGroupBox(Form)
        self.groupbox_sampling_feature.setMinimumSize(QtCore.QSize(264, 354))
        self.groupbox_sampling_feature.setObjectName(_fromUtf8("groupbox_sampling_feature"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupbox_sampling_feature)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_foi_id = QtGui.QLabel(self.groupbox_sampling_feature)
        self.label_foi_id.setMinimumSize(QtCore.QSize(0, 18))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_foi_id.setFont(font)
        self.label_foi_id.setObjectName(_fromUtf8("label_foi_id"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label_foi_id)
        self.groupBox = QtGui.QGroupBox(self.groupbox_sampling_feature)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 58))
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.CB_ref = QtGui.QComboBox(self.groupBox)
        self.CB_ref.setMinimumSize(QtCore.QSize(0, 20))
        self.CB_ref.setObjectName(_fromUtf8("CB_ref"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.CB_ref)
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.SpanningRole, self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(self.groupbox_sampling_feature)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 48))
        self.groupBox_3.setAutoFillBackground(True)
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setCheckable(True)
        self.groupBox_3.setChecked(False)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.LE_id_bd_extern = QtGui.QLineEdit(self.groupBox_3)
        self.LE_id_bd_extern.setMinimumSize(QtCore.QSize(20, 20))
        self.LE_id_bd_extern.setObjectName(_fromUtf8("LE_id_bd_extern"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.LE_id_bd_extern)
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setMinimumSize(QtCore.QSize(0, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.SpanningRole, self.groupBox_3)
        self.label_3 = QtGui.QLabel(self.groupbox_sampling_feature)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.LE_sampling_name = QtGui.QLineEdit(self.groupbox_sampling_feature)
        self.LE_sampling_name.setMinimumSize(QtCore.QSize(0, 20))
        self.LE_sampling_name.setObjectName(_fromUtf8("LE_sampling_name"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.LE_sampling_name)
        self.label_4 = QtGui.QLabel(self.groupbox_sampling_feature)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.SpanningRole, self.label_4)
        self.DTE_sampling_date = QtGui.QDateTimeEdit(self.groupbox_sampling_feature)
        self.DTE_sampling_date.setMinimumSize(QtCore.QSize(0, 20))
        self.DTE_sampling_date.setObjectName(_fromUtf8("DTE_sampling_date"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.SpanningRole, self.DTE_sampling_date)
        self.label_6 = QtGui.QLabel(self.groupbox_sampling_feature)
        self.label_6.setMinimumSize(QtCore.QSize(0, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_6)
        self.CB_interet = QtGui.QComboBox(self.groupbox_sampling_feature)
        self.CB_interet.setMinimumSize(QtCore.QSize(0, 20))
        self.CB_interet.setObjectName(_fromUtf8("CB_interet"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.CB_interet)
        self.label_7 = QtGui.QLabel(self.groupbox_sampling_feature)
        self.label_7.setMinimumSize(QtCore.QSize(0, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.SpanningRole, self.label_7)
        self.CB_process = QtGui.QComboBox(self.groupbox_sampling_feature)
        self.CB_process.setMinimumSize(QtCore.QSize(0, 20))
        self.CB_process.setObjectName(_fromUtf8("CB_process"))
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.SpanningRole, self.CB_process)
        self.horizontalLayout.addWidget(self.groupbox_sampling_feature)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupbox_sampling_feature.setTitle(_translate("Form", "Information sur l\'élément", None))
        self.label_foi_id.setText(_translate("Form", "identifiant de l\'élément :", None))
        self.groupBox.setTitle(_translate("Form", "Provenant de la donnée", None))
        self.label_2.setText(_translate("Form", "Référence", None))
        self.groupBox_3.setTitle(_translate("Form", "Provient d\'une Base de données existante?", None))
        self.label_5.setText(_translate("Form", "id de base de donnée", None))
        self.label_3.setText(_translate("Form", "Nom de l\'élément", None))
        self.label_4.setText(_translate("Form", "Date de création de l\'élément", None))
        self.label_6.setText(_translate("Form", "Type d\'élément", None))
        self.label_7.setText(_translate("Form", "Méthode utilisée pour créer l\'élément", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

