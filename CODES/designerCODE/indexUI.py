# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'indexUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MENU(object):
    def setupUi(self, MENU):
        MENU.setObjectName("MENU")
        MENU.resize(912, 636)
        self.label = QtWidgets.QLabel(MENU)
        self.label.setGeometry(QtCore.QRect(170, 60, 571, 131))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(48)
        self.label.setFont(font)
        self.label.setLocale(QtCore.QLocale(QtCore.QLocale.French, QtCore.QLocale.France))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(MENU)
        self.layoutWidget.setGeometry(QtCore.QRect(310, 230, 282, 331))
        self.layoutWidget.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(231, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(231, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(231, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(231, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(231, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.disconnectButton = QtWidgets.QPushButton(MENU)
        self.disconnectButton.setGeometry(QtCore.QRect(730, 560, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.disconnectButton.setFont(font)
        self.disconnectButton.setObjectName("disconnectButton")

        self.retranslateUi(MENU)
        self.pushButton_3.clicked.connect(MENU.creerVote)
        self.pushButton_5.clicked.connect(MENU.enregistrerElecteur)
        self.pushButton_2.clicked.connect(MENU.enregistrerVote)
        self.pushButton_4.clicked.connect(MENU.verifierVote)
        self.pushButton.clicked.connect(MENU.procederDepo)
        self.disconnectButton.clicked.connect(MENU.logout)
        QtCore.QMetaObject.connectSlotsByName(MENU)

    def retranslateUi(self, MENU):
        _translate = QtCore.QCoreApplication.translate
        MENU.setWindowTitle(_translate("MENU", "Form"))
        self.label.setText(_translate("MENU", "Système de vote"))
        self.pushButton_3.setText(_translate("MENU", " Créer un vote"))
        self.pushButton_5.setText(_translate("MENU", "Enregistrer un électeur"))
        self.pushButton_2.setText(_translate("MENU", "Enregistrer un vote"))
        self.pushButton_4.setText(_translate("MENU", "Vérifier un vote"))
        self.pushButton.setText(_translate("MENU", "Procéder au dépouillement"))
        self.disconnectButton.setText(_translate("MENU", "Déconnexion"))