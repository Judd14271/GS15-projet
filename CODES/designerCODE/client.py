#
# clientSocket = socket(AF_INET,SOCK_STREAM)
# clientSocket.connect((host_name,port_num))
#
# message = input('enter message:')
# clientSocket.send(message.encode())
# clientSocket.send((message+'123').encode())
#
# receipt1 = clientSocket.recv(1024).decode()
# print("r1:"+receipt1)
# receipt2 = clientSocket.recv(1024).decode()
# print("r2:"+receipt2)
# clientSocket.close()

from socket import *
import json
import sys
import PyQt5.QtGui as qg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from loginUI import Ui_login
from indexUI import Ui_MENU
from inscrirerUI import Ui_registerWidget
from creervoteUI import Ui_createVote
from voterUI import Ui_VOTER
from hashlib import md5
from hashlib import sha256
import hmac

host_name = 'DESKTOP-AGULUSU' #10.182.34.64
port_num = 1200
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host_name, port_num)) #与服务器A建立连接
emailV = ''
candidates = []
uuid = ''
p = 92904936882697929445726711920691941953763517081
g = 7

class MyPyQT_Login(QtWidgets.QWidget,Ui_login): #登录页面

    isAdmin = 0
    isLogin = 0 #初始化权限

    def __init__(self):
        super(MyPyQT_Login,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("../res/icon.jpg"))


    def OPEN(self):
        self.show()

    def connecter(self):

        email = self.emailLine.text()
        password = self.passwordLine.text()
        loginJson = {'type':'login','email':email, 'password':password}
        loginJson = json.dumps(loginJson)
        clientSocket.send(loginJson.encode())
        recvMes = clientSocket.recv(1024).decode()
        recvMes = json.loads(recvMes) #向服务器A提交表单并等待返回值

        if recvMes['isLogin'] == 1: #检查是否登陆成功以及权限等级
            self.isLogin = 1
            self.emailLine.setText('')
            self.passwordLine.setText('')
            global uuid
            uuid = recvMes['uuid']
            print(uuid)
            global emailV
            emailV = email
            print(emailV)
            if recvMes['isAdmin'] == 1:
                QMessageBox.information(self, "Succès", 'Identité:Admin')
                self.isAdmin = 1
            else:
                QMessageBox.information(self, "Succès", 'Identité:Électeur')
            menu.OPEN()
            self.close()
        else:
            QMessageBox.information(self, "Échec", "Électeur n'existe pas \nou mot de passe incorrect")

    def inscrire(self):
        register.OPEN()
        self.close()


class MyPyQT_index(QtWidgets.QWidget, Ui_MENU): #菜单页面

    def __init__(self):
        super(MyPyQT_index, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("MENU")
        self.setWindowIcon(qg.QIcon("../res/icon.jpg"))

    def OPEN(self):
        self.show()

    def creerVote(self): #管理员才能开启投票
        if login.isAdmin == 1:
            createVote.show()
            self.close()
        else:
            QMessageBox.information(self, "Échec", 'Pas de permission!')

    def enregistrerElecteur(self):
        print()

    def enregistrerVote(self):
        request = {'type': 'getCandidates'}
        request = json.dumps(request)
        clientSocket.send(request.encode())
        recvMes = clientSocket.recv(1024).decode()
        recvMes = json.loads(recvMes)
        print(recvMes)
        if recvMes != 'noVote':
            global candidates
            candidates = recvMes
            print(f'candidates:{candidates}')
            voter.OPEN()
            self.close()
        else:
            QMessageBox.information(self, "Échec", "Pas d'élection maintenant")



    def verifierVote(self):
        print()

    def procederDepo(self):
        print()

    def logout(self):
        login.isLogin = 0
        login.isAdmin = 0
        login.OPEN()
        self.close()


class MyPyQT_voter(QtWidgets.QWidget, Ui_VOTER): #菜单页面


    def OPEN(self):
        self.candidatesList = QtWidgets.QListView(self.widget)
        slm = QStringListModel()
        self.qList = candidates
        slm.setStringList(self.qList)
        self.candidatesList.setModel(slm)
        self.candidatesList.clicked.connect(self.clicked)
        print(self.qList)
        print(candidates)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setFamily("Calibri")
        self.candidatesList.setFont(font)
        self.candidatesList.setObjectName("candidatesList")
        self.verticalLayout.addWidget(self.candidatesList)
        self.verticalLayout.addWidget(self.candidatesList)
        self.show()

    def clicked(self, qModelIndex):
        # 提示信息弹窗，你选择的信息
        self.choiceDisplay.setText(self.qList[qModelIndex.row()])
        QMessageBox.information(self, 'ListWidget', 'Votre choix：' + self.qList[qModelIndex.row()])

    def __init__(self):
        super(MyPyQT_voter, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Voter")
        self.setWindowIcon(qg.QIcon("../res/icon.jpg"))

    def sendVeri(self):
        sendMes = {'type':'sendVeri','email':emailV}
        sendMes = json.dumps(sendMes)
        clientSocket.send(sendMes.encode())

    def goback(self):
        self.choiceDisplay.setText('')
        self.cnEdit.setText('')
        self.veriEdit.setText('')
        self.candidatesList.deleteLater()
        menu.OPEN()
        self.close()

    def vote(self):
        cn = str(self.cnEdit.text())
        veri = str(self.veriEdit.text())
        if cn == '' or veri == '':
            QMessageBox.information(self, "Échec", "Veuillez entrer les codes!")
        else:
            s = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
            cnIndex = ''.join([str(list(s).index(i)) for i in list(cn)])
            cnIndex = int(cnIndex) % p
            sendMes = {'type': 'startZERO'}
            sendMes = json.dumps(sendMes)
            clientSocket.send(sendMes.encode())
            recvMes = clientSocket.recv(1024).decode()
            recvMes = json.loads(recvMes)
            A = recvMes['A']
            w = recvMes['w']

            challenge = hmac.new(uuid.encode('utf-8'), str(A).encode(), digestmod=sha256).hexdigest()
            challenge = challenge.encode('utf-8')
            challenge = challenge.decode()
            challenge = int(challenge, 16) % p

            response = int(w - cnIndex * challenge)

            randnum = md5(veri.encode(encoding='utf-8')).hexdigest()

            sendMes = {'type': 'ZERO', 'challenge': challenge, 'response': response, 'uuid': uuid, 'veri': randnum}
            sendMes = json.dumps(sendMes)
            clientSocket.send(sendMes.encode())
            recvMes = clientSocket.recv(1024).decode()
            recvMes = json.loads(recvMes)
            print(recvMes)
            if recvMes == 'success':
                QMessageBox.information(self, "Succès", 'Vote réussi !')
                self.candidatesList.deleteLater()
                self.choiceDisplay.setText('')
                self.cnEdit.setText('')
                self.veriEdit.setText('')
                menu.OPEN()
                self.close()
            else:
                QMessageBox.information(self, "Échec", "Code secret ou captcha incorrect !")




class MyPyQT_register(QtWidgets.QWidget,Ui_registerWidget): #注册页面
    def __init__(self):
        super(MyPyQT_register,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("S'incrire")
        self.setWindowIcon(QIcon("../res/icon.jpg"))

    def OPEN(self):
        self.show()

    def register(self):

        blanks = 0
        username = self.usernameLine.text()
        email = self.emailLine.text()
        password = self.passwordLine.text()

        if username == '' or email == '' or password =='': #本地检查是否有空值
            QMessageBox.information(self,'Échec','Pas de blancs autorisés!')
            blanks = 1

        if blanks == 0: #向服务器A提交表单并等待回应
            registerJson = {'type': 'register', 'username': username, 'password': password, 'email': email}
            registerJson = json.dumps(registerJson)
            clientSocket.send(registerJson.encode())
            recvMes = clientSocket.recv(1024).decode()
            recvMes = json.loads(recvMes)

            if recvMes['isRepeat'] == 1: #检查是否注册成功
                QMessageBox.information(self, "Échec", "L'utilisateur existe déjà!")
            else:
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
        voteJson = {'type':'vote'}
        voteJson.update(self.options)
        voteJson = json.dumps(voteJson).encode()
        clientSocket.send(voteJson)
        QMessageBox.information(self, "Succès", 'Vote a été créé!')
        self.close()
        menu.OPEN()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    createVote = MyPyQT_createVote()
    voter = MyPyQT_voter()
    login = MyPyQT_Login()
    menu = MyPyQT_index()
    register = MyPyQT_register()
    login.show()
    sys.exit(app.exec_())