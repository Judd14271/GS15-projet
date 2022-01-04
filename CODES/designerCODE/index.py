import sys
import PyQt5.QtGui as qg
from PyQt5 import QtWidgets
from indexUI import Ui_MENU

class MyPyQT_Form(QtWidgets.QWidget,Ui_MENU):

    def __init__(self):
        super(MyPyQT_Form,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("MENU")
        self.setWindowIcon(qg.QIcon("../res/icon.jpg"))

    def creerVote(self):
        print()

    def enregistrerElecteur(self):
        print()

    def enregistrerVote(self):
        print()

    def verifierVote(self):
        print()

    def procederDepo(self):
        print()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())