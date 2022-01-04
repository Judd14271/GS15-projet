import sys
import PyQt5.QtGui as qg
from PyQt5 import QtWidgets
from XXX import Ui_XXX

class MyPyQT_Form(QtWidgets.QWidget,Ui_XXX):
    def __init__(self):
        super(MyPyQT_Form,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("XXX")
        self.setWindowIcon(qg.QIcon("../res/icon.jpg"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())