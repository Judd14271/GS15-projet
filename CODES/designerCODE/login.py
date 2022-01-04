import sys
import pandas as pd
import PyQt5.QtGui as qg
import base58
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from loginUI import Ui_login
from indexUI import Ui_MENU
from inscrirerUI import Ui_registerWidget
from creervoteUI import Ui_createVote


class MyPyQT_Login(QtWidgets.QWidget,Ui_login):

    isLogin = 0
    isAdmin = 0

    def __init__(self):
        super(MyPyQT_Login,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("../res/icon.jpg"))

    def OPEN(self):
        self.show()

    def connecter(self):
        status = 0
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        readUsers = pd.read_csv("../database/users.csv")
        users = pd.DataFrame(readUsers)

        for rows in users.itertuples():
            if getattr(rows,'username')==username and getattr(rows,'password')==password :
                status = 1
                self.isLogin = 1
                self.usernameLine.setText('')
                self.passwordLine.setText('')
                if getattr(rows,'admin')==1:
                    self.isAdmin = 1
                    QMessageBox.information(self, "Succès", 'Identité:Admin')
                else:
                    QMessageBox.information(self, "Succès", 'Identité:Électeur')
                menu.OPEN()
                self.close()
                break
        if status == 0:
            QMessageBox.information(self, "Échec", "Électeur n'existe pas \nou mot de passe incorrect")

    def inscrire(self):
        register.OPEN()
        self.close()


class MyPyQT_index(QtWidgets.QWidget, Ui_MENU):

    def __init__(self):
        super(MyPyQT_index, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("MENU")
        self.setWindowIcon(qg.QIcon("../res/icon.jpg"))

    def OPEN(self):
        self.show()

    def creerVote(self):
        if login.isAdmin == 1:
            createVote.show()
            self.close()
        else:
            QMessageBox.information(self, "Échec", 'Pas de permission!')

    def enregistrerElecteur(self):
        print()

    def enregistrerVote(self):
        if login.isLogin == 1:
            print("SUC")
        else:
            print("Fail")

    def verifierVote(self):
        print()

    def procederDepo(self):
        print()

    def logout(self):
        login.isLogin = 0
        login.isAdmin = 0
        login.OPEN()
        self.close()

class MyPyQT_register(QtWidgets.QWidget,Ui_registerWidget):
    def __init__(self):
        super(MyPyQT_register,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("S'incrire")
        self.setWindowIcon(QIcon("../res/icon.jpg"))

    def OPEN(self):
        self.show()

    def register(self):
        repeat = 0
        blanks = 0
        username = self.usernameLine.text()
        email = self.emailLine.text()
        password = self.passwordLine.text()
        if username == '' or email == '' or password =='':
            QMessageBox.information(self,'Échec','Pas de blancs autorisés!')
            blanks = 1
        df = pd.read_csv("../database/users.csv", index_col=None)
        if blanks == 0:
            for rows in df.itertuples():
                if getattr(rows, 'username') == username:
                    QMessageBox.information(self, "Échec", "L'utilisateur existe déjà!")
                    repeat = 1
                    break
        if repeat == 0 and blanks == 0:
            line = getattr(df,'ID')
            lastID =int(line[-1:] + 1)
            uuid = base58.b58encode(('1' + str(lastID) + '0')).decode()
            newUser = {'ID':lastID,'uuid':uuid,'username': username, 'password': password, 'email': email}
            df = df.append(newUser, ignore_index=True)
            df.to_csv("../database/users.csv", index=False)
            QMessageBox.information(self, "Succès", 'Inscription réussie!')
            self.usernameLine.setText('')
            self.emailLine.setText('')
            self.passwordLine.setText('')
            login.OPEN()
            self.close()

    def goback(self):
        self.usernameLine.setText('')
        self.emailLine.setText('')
        self.passwordLine.setText('')
        login.OPEN()
        self.close()

class MyPyQT_createVote(QtWidgets.QWidget,Ui_createVote):

    optionNum = 0
    options = {}

    def __init__(self):
        super(MyPyQT_createVote,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Créer un vote")
        self.setWindowIcon(QIcon("../res/icon.jpg"))
        self.displayBox.setText('')

    def OPEN(self):
        self.show()

    def goback(self):
        self.displayBox.setText('')
        self.options = {}
        menu.OPEN()
        self.close()

    def addOption(self):
        if self.optionAdder.text() == '':
            QMessageBox.information(self, "Échec", "Les options ne doivent pas être vides !")
        else:
            self.options[self.optionNum] = self.optionAdder.text()
            self.optionAdder.setText('')
            prevText = self.displayBox.toPlainText()
            if prevText == '':
                self.displayBox.setText('1) ' + self.options[self.optionNum] + '\n')
                self.optionNum += 1
            else:
                self.displayBox.setText(prevText + str(self.optionNum + 1) + ') ' + self.options[self.optionNum] + '\n')
                self.optionNum += 1

    def deleteOption(self):
        self.options.pop(self.optionNum - 1)
        prevText = self.displayBox.toPlainText()
        prevText = prevText.split('\n')
        prevText = prevText[0:-2]
        textComb = ''
        for rows in prevText:
            textComb = textComb + rows + '\n'
        self.optionNum -= 1
        self.displayBox.setText(textComb)

    def createVote(self):
        print(self.options)
        QMessageBox.information(self, "Succès", 'Vote a été créé!')
        self.close()
        menu.OPEN()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    createVote = MyPyQT_createVote()
    login = MyPyQT_Login()
    menu = MyPyQT_index()
    register = MyPyQT_register()
    login.show()
    sys.exit(app.exec_())