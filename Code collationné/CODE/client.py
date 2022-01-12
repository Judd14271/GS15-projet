from socket import *
import json
import sys
import PyQt5.QtGui as qg
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from loginUI import Ui_login
from indexUI import Ui_MENU
from inscrirerUI import Ui_registerWidget
from creervoteUI import Ui_createVote
from countUI import Ui_countVote
from veriUI import Ui_verifier
from voterUI import Ui_VOTER
from hashlib import md5
from hashlib import sha256
import hmac
from encryptions import encrypt,signer

host_name = 'DESKTOP-AGULUSU' #10.182.34.64
port_num = 1200
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host_name, port_num))  #Connexion avec le protocole socket(seulement avec Seveur A)
emailV = ''
candidates = []
uuid = ''
p = 92904936882697929445726711920691941953763517081
g = 7

class MyPyQT_Login(QtWidgets.QWidget,Ui_login): # Fenêtre de login

    isAdmin = 0
    isLogin = 0 #Initialisation des permissions
    isVote = 0

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
        recvMes = json.loads(recvMes) #Soumettre le mot de passe du compte au serveur A et attendre la valeur de retour.

        if recvMes['isLogin'] == 1: #Vérifier la réussite de la connexion et le niveau de permission
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
            if recvMes['isVote'] == 1:
                self.isVote = 1
            else:
                self.isVote = 0
            menu.OPEN()
            self.close()
        else:
            QMessageBox.information(self, "Échec", "Électeur n'existe pas \nou mot de passe incorrect")

    def inscrire(self):
        register.OPEN()
        self.close()


class MyPyQT_index(QtWidgets.QWidget, Ui_MENU): # Fenêtre de menu

    def __init__(self):
        super(MyPyQT_index, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("MENU")
        self.setWindowIcon(qg.QIcon("../res/icon.jpg"))

    def OPEN(self):
        self.show()

    def creerVote(self): #Ouvrez la page Créer un vote
        if login.isAdmin == 1: #Seuls les administrateurs
            createVote.show()
            self.close()
        else:
            QMessageBox.information(self, "Échec", 'Pas de permission!')

    def enregistrerElecteur(self): # pas de fontion car deja se connecte
        print()

    def enregistrerVote(self): #Ouvrez la page de donner un bulletin
        if login.isVote == 0:
            QMessageBox.information(self, "Échec", "Pas d'élection maintenant")
        else:
            request = {'type': 'getCandidates'}  #Obtenir une liste de candidats à l'ouverture
            request = json.dumps(request)
            clientSocket.send(request.encode())
            recvMes = clientSocket.recv(1024).decode()
            recvMes = json.loads(recvMes)
            print(recvMes)
            global candidates
            candidates = recvMes
            print(f'candidates:{candidates}')
            voter.OPEN()
            self.close()



    def verifierVote(self): #Ouvrez la page de verifier un vote
        if login.isVote == 0:
            QMessageBox.information(self, "Échec", "Pas d'élection maintenant")
        else:
            verify.OPEN()
            self.close()

    def procederDepo(self): #Ouvrez la page de depouillment
        if login.isAdmin == 1:
            count.OPEN()
            self.close()
        else:
            QMessageBox.information(self, "Échec", 'Pas de permission!')


    def logout(self):
        login.isLogin = 0
        login.isAdmin = 0
        login.OPEN()
        self.close()


class MyPyQT_voter(QtWidgets.QWidget, Ui_VOTER): #page de voter

    choix = ''
    ifVeri = 0

    def OPEN(self): #Rendre la liste des candidats récupérée lors de l'ouverture de la fenêtre à l'interface
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

    def clicked(self, qModelIndex):  #Afficher les options que vous avez sélectionnées
        self.choiceDisplay.setText(self.qList[qModelIndex.row()])
        QMessageBox.information(self, 'ListWidget', 'Votre choix：' + self.qList[qModelIndex.row()])
        self.choix = self.qList[qModelIndex.row()]
        print(self.choix)

    def __init__(self):
        super(MyPyQT_voter, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Voter")
        self.setWindowIcon(qg.QIcon("../res/icon.jpg"))

    def sendVeri(self): #Envoi d'une requête au serveur pour un code de vérification
        self.ifVeri = 1
        sendMes = {'type':'sendVeri','email':emailV}
        sendMes = json.dumps(sendMes)
        clientSocket.send(sendMes.encode())

    def goback(self):
        self.ifVeri = 0
        self.choiceDisplay.setText('')
        self.cnEdit.setText('')
        self.veriEdit.setText('')
        self.candidatesList.deleteLater()
        menu.OPEN()
        self.close()

    def vote(self):  #voter
        if self.ifVeri == 0:  #Empêcher quelqu'un d'utiliser un captcha précédent
            QMessageBox.information(self, "Échec", "Vous n'avez pas envoyé de code de vérification ou vous devez le renvoyer.")
        else:
            cn = str(self.cnEdit.text())
            veri = str(self.veriEdit.text())
            if cn == '' or veri == '':
                QMessageBox.information(self, "Échec", "Veuillez entrer les codes!")
            else:
                s = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                cnIndex = ''.join([str(list(s).index(i)) for i in list(cn)])
                cnIndex = int(cnIndex) % p

                sendMes = {'type': 'startZERO'}  #Envoyer une requête pour démarrer ZKP, récupérer A = g^w
                sendMes = json.dumps(sendMes)
                clientSocket.send(sendMes.encode())
                recvMes = clientSocket.recv(1024).decode()
                recvMes = json.loads(recvMes)
                A = recvMes['A']
                w = recvMes['w']
                h = recvMes['h'] #recevoir w,A pour la ZKP de cn(credential), et aussi h pour chiffrer la vote

                print(recvMes)
                str1 = list('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
                choixText = self.choix
                print(choixText)
                choix = [str(str1.index(x)) for x in choixText]
                for x in choix:
                    if int(x) % 10 == int(x):
                        choix[choix.index(x)] = '0' + x  #S'il s'agit d'un chiffre unique, ajoutez un 0 devant lui. exemple: 9C est 0811, pas 811
                choix = int(''.join(choix))
                print(f'choix:{choix}') #transferer le choix en str a un nombre avec octets pairs (S'il s'agit d'un nombre impair, cela entraînera une ambiguïté lors du décryptage.)

                c = encrypt(h, choix) #chiffrer avec la h recu   function stored in encryptions.py
                print(f'c:{c}')
                signature, e, n = signer(c[1]) #signature de c2
                print(f'e:{e}')

                challenge = hmac.new(uuid.encode('utf-8'), str(A).encode(), digestmod=sha256).hexdigest()
                challenge = challenge.encode('utf-8')
                challenge = challenge.decode()
                challenge = int(challenge, 16) % p # calculer challenge en utilisant A=g^w de ServerurA et SHA-256

                response = int(w - cnIndex * challenge)    #cnIndex est le cn transfere a numero

                randnum = md5(veri.encode(encoding='utf-8')).hexdigest()

                sendMes = {'type': 'ZERO', 'challenge': challenge, 'response': response, 'uuid': uuid, 'veri': randnum,
                           'c': c, 'signature': signature, 'e': e, 'n': n}
                print(f'sendMes{sendMes}')
                sendMes = json.dumps(sendMes)
                clientSocket.send(sendMes.encode())   # envoyer le vote chiffre, la signature de cn et la signature de c2 (il y 2 ZKP actuellement)
                recvMes = clientSocket.recv(1024).decode()
                recvMes = json.loads(recvMes)  #recevoir le message de serveure si les elements sont verifier
                print(recvMes)
                if recvMes == 'success':
                    a = QMessageBox()
                    a.setTextInteractionFlags(Qt.TextSelectableByMouse)
                    a.setText(f'Vote réussi !\nVotre signature:{signature}\nVeuillez copier ce code et le garder en sécurité')
                    a.exec_()
                    self.candidatesList.deleteLater() #effacer les entrées restes dans la fenetre apres la reussite
                    self.choiceDisplay.setText('')
                    self.cnEdit.setText('')
                    self.veriEdit.setText('')
                    menu.OPEN()
                    self.close()
                elif recvMes == 'repeat': #return repeat si l'utilisateur a deja vote
                    QMessageBox.information(self, "Échec", "Vous avez déjà voté !")
                else: #return Échec si la vérification échoue
                    QMessageBox.information(self, "Échec", "Code secret ou captcha incorrect !")



class MyPyQT_verifier(QtWidgets.QWidget,Ui_verifier):

    def __init__(self):
        super(MyPyQT_verifier,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Vérifier")
        self.setWindowIcon(QIcon("../res/icon.jpg"))

    def OPEN(self):

        sendMes = {'type':'verify'}    #envoyer la demande de verification de vote(s'il exist dans la list de vote en utilisant la signature)
        sendMes = json.dumps(sendMes)
        clientSocket.send(sendMes.encode())
        recvMes = clientSocket.recv(1024).decode()   #recevoir la list composee par 2 columns 'time' et 'signature'(un peu longue)
        recvMes = json.loads(recvMes)
        print(f'recv{recvMes}')

        data = pd.DataFrame(columns=['time','signature'])
        for tuples in recvMes:
            print(tuples)
            line = {'time': tuples[0], 'signature': tuples[1]}
            print(line)
            data = data.append(line, ignore_index=True)
        print(f'data{data}')
        data.to_csv('../database/list.csv',index=None)
        df = pd.read_csv('../database/list.csv')  # restorer la list dans un csv local pour améliorer l'efficacité des recherches apres

        length = len(df)
        slm = QStandardItemModel()
        slm.setHorizontalHeaderLabels(['time', 'signature']) #Présentation des données du tableau à l'interface
        for rows in range(length):
            slm.appendRow([QStandardItem('%s' % (df.loc[rows,'time'])),QStandardItem('%s' % (str(df.loc[rows,'signature'])))])
        self.tableView123.setModel(slm)
        self.tableView123.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView123.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.show()

    def trouver(self):  #Vérifier s'il existe sur la base de la signature fournie.
        iffound = 0
        df = pd.read_csv('../database/list.csv')
        length = len(df)
        slm = QStandardItemModel()
        slm.setHorizontalHeaderLabels(['time', 'signature'])
        signature = self.signatureEdit.text()
        for rows in range(length): #function de recherche
            if df.loc[rows,'signature'] == signature:
                slm.appendRow([QStandardItem('%s' % (df.loc[rows, 'time'])),
                               QStandardItem('%s' % (str(df.loc[rows, 'signature'])))])
                self.tableView123.setModel(slm)
                iffound = 1
                break
        if iffound == 0:
            QMessageBox.information(self, 'Échec', "Aucun bulletin correspondant n'a été trouvé !")

    def clear(self):  #effacer les entree(Rendre également la table entière)
        df = pd.read_csv('../database/list.csv')
        length = len(df)
        self.signatureEdit.setText('')
        slm = QStandardItemModel()
        slm.setHorizontalHeaderLabels(['time', 'signature'])
        for rows in range(length):
            slm.appendRow([QStandardItem('%s' % (df.loc[rows, 'time'])),
                           QStandardItem('%s' % (str(df.loc[rows, 'signature'])))])
        self.tableView123.setModel(slm)

    def goback(self):
        self.signatureEdit.setText('')
        menu.OPEN()
        self.close()

class MyPyQT_register(QtWidgets.QWidget,Ui_registerWidget): # interface de s'inscrire
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

        if username == '' or email == '' or password =='': #Vérification locale des valeurs nulles
            QMessageBox.information(self,'Échec','Pas de blancs autorisés!')
            blanks = 1

        if blanks == 0: # envoyer la list de donne a serveur A
            registerJson = {'type': 'register', 'username': username, 'password': password, 'email': email}
            registerJson = json.dumps(registerJson)
            clientSocket.send(registerJson.encode())
            recvMes = clientSocket.recv(1024).decode() #recevoir le message si l'inscrition a reussi ou non
            recvMes = json.loads(recvMes)

            if recvMes['isRepeat'] == 1:
                QMessageBox.information(self, "Échec", "L'utilisateur existe déjà!")
            else:
                QMessageBox.information(self, "Succès", 'Inscription réussie!')
                self.usernameLine.setText('')
                self.emailLine.setText('')
                self.passwordLine.setText('') #effacer les entrees lorsque vous sortez
                login.OPEN()
                self.close()

    def goback(self):
        self.usernameLine.setText('')
        self.emailLine.setText('')
        self.passwordLine.setText('')
        login.OPEN()
        self.close()

class MyPyQT_count(QtWidgets.QWidget,Ui_countVote): #interface de depouillement

    def __init__(self):
        super(MyPyQT_count,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Dépouillement")
        self.setWindowIcon(QIcon("../res/icon.jpg"))

    def OPEN(self):   # rendre les donnes de vote initialisee a l'interface
        df = pd.read_csv('../database/resultat.csv')
        length = len(df)
        slm = QStandardItemModel()
        slm.setHorizontalHeaderLabels(['candidate', 'votes'])
        for rows in range(length):
            slm.appendRow([QStandardItem('%s' % (df.loc[rows, 'candidate'])),
                           QStandardItem('%s' % (str(df.loc[rows, 'votes'])))])
        self.resultView.setModel(slm)
        self.resultView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



        login.isVote = 0
        sendMes = {'type':'stopVote'} #Si un administrateur lance un bulletin, Le reste des utilisateurs ne peut plus voter
        sendMes = json.dumps(sendMes) #De même, les autres administrateurs qui cliquent à ce bouton ne feront qu'accéder à la page de depouillement et ne réinitialiseront pas le depouillement.
        clientSocket.send(sendMes.encode())
        recvMes = clientSocket.recv(1024).decode()
        recvMes = json.loads(recvMes)
        print(recvMes)
        self.numPri.setText(recvMes['nrest_keys']) #rendre les donnes sur l'interface (votes restes,vote comptés,cle privee restes)
        self.numCacule.setText(recvMes['ncompte_votes'])
        self.numRestant.setText(recvMes['nrest_votes'])
        self.final_2.setText(recvMes['final'])
        self.show()

    def calculate(self):  #envoyer la cle privee a  la serveurA, serveurA l'envoyer a la serveur de depouillement S
        cle = self.cleEdit.text()
        sendMes = {'type':'calculate','cle':cle}
        sendMes = json.dumps(sendMes)
        clientSocket.send(sendMes.encode())
        recvMes = clientSocket.recv(1024).decode()
        recvMes = json.loads(recvMes) #recevoir la resultat
        if recvMes == 'notfound':
            QMessageBox.information(self, 'Échec', "Cle incorrecte!")
        else:
            self.numPri.setText(recvMes['nrest_keys'])
            self.numCacule.setText(recvMes['ncompte_votes'])
            self.numRestant.setText(recvMes['nrest_votes'])
            QMessageBox.information(self, 'Échec', "success")

            df = pd.read_csv('../database/resultat.csv') #rendre les donnes recu
            length = len(df)
            slm = QStandardItemModel()
            slm.setHorizontalHeaderLabels(['candidate', 'votes'])
            for rows in range(length):
                slm.appendRow([QStandardItem('%s' % (df.loc[rows, 'candidate'])),
                               QStandardItem('%s' % (str(df.loc[rows, 'votes'])))])
            self.resultView.setModel(slm)
            self.final_2.setText(recvMes['final'])

    def goback(self):
        self.close()
        menu.OPEN()


class MyPyQT_createVote(QtWidgets.QWidget,Ui_createVote): #pour les admins seulement

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

    def addOption(self):   #ajouter les options
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

    def deleteOption(self):  #effacer les options si un erreur d'entrée accidentelle
        self.options.pop(self.optionNum - 1)
        prevText = self.displayBox.toPlainText()
        prevText = prevText.split('\n')
        prevText = prevText[0:-2]
        textComb = ''
        for rows in prevText:
            textComb = textComb + rows + '\n'
        self.optionNum -= 1
        self.displayBox.setText(textComb)

    def createVote(self):  #envoyer les choix a la serveur A
        voteJson = {'type':'cvote'}
        voteJson.update(self.options)
        voteJson = json.dumps(voteJson).encode()
        clientSocket.send(voteJson)
        QMessageBox.information(self, "Succès", 'Vote a été créé!')
        login.isVote = 1
        self.close()
        menu.OPEN()



if __name__ == '__main__':  #Instanciez ces objets
    app = QtWidgets.QApplication(sys.argv)
    createVote = MyPyQT_createVote()
    count = MyPyQT_count()
    verify = MyPyQT_verifier()
    voter = MyPyQT_voter()
    login = MyPyQT_Login()
    menu = MyPyQT_index()
    register = MyPyQT_register()
    login.show()
    sys.exit(app.exec_())