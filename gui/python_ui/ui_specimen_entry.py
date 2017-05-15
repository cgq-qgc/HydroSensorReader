# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'U:\Programmation\ogc_om_interface\gui\pyqt_ui\specimen_entry.ui'
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
        Form.resize(909, 500)
        Form.setMinimumSize(QtCore.QSize(800, 500))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.stackWidget_specimens = QtGui.QToolBox(Form)
        self.stackWidget_specimens.setMinimumSize(QtCore.QSize(588, 382))
        self.stackWidget_specimens.setMaximumSize(QtCore.QSize(900, 16777215))
        self.stackWidget_specimens.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.stackWidget_specimens.setAutoFillBackground(True)
        self.stackWidget_specimens.setObjectName(_fromUtf8("stackWidget_specimens"))
        self.verticalLayout.addWidget(self.stackWidget_specimens)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btn_add_spec = QtGui.QPushButton(Form)
        self.btn_add_spec.setObjectName(_fromUtf8("btn_add_spec"))
        self.gridLayout.addWidget(self.btn_add_spec, 0, 0, 1, 1)
        self.btn_delete_spec = QtGui.QPushButton(Form)
        self.btn_delete_spec.setObjectName(_fromUtf8("btn_delete_spec"))
        self.gridLayout.addWidget(self.btn_delete_spec, 1, 0, 1, 1)
        self.btn_duplicate_spec = QtGui.QPushButton(Form)
        self.btn_duplicate_spec.setObjectName(_fromUtf8("btn_duplicate_spec"))
        self.gridLayout.addWidget(self.btn_duplicate_spec, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.btn_add_spec.setText(_translate("Form", "Ajouter élément", None))
        self.btn_delete_spec.setText(_translate("Form", "Supprimer élément", None))
        self.btn_duplicate_spec.setText(_translate("Form", "Dupliquer élément", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

