import json
import random
import time
import re
from socket import *
from sendEmail import mailVeri
import pandas as pd
import base58
from hashlib import md5
from Montgomery import Montgomery
from encryptions import generateKey,decrypt

socketA2Client = socket(AF_INET, SOCK_STREAM)
socketA2Client.bind((gethostname(), 1200)) # le port utilise par serveurA

socketA2E = socket(AF_INET, SOCK_STREAM)
socketA2E.connect((gethostname(), 1100)) # connecter a la serveur E  (on peut appliquer les serveur a l'internet facilement)

socketA2S = socket(AF_INET, SOCK_STREAM)
socketA2S.connect((gethostname(), 1300)) # connecter a la serveur S

socketA2Client.listen(2) #ecoute les requestes de la client

print('Server Ready')
connectionA2Client, address = socketA2Client.accept()
print('已建立一个连接：',address) #reussi
str1 = list('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
p = 92904936882697929445726711920691941953763517081
g = 7
randnum = 1
s = 0
cle_privee = 0

while True:  #la serveur ecoute toujour les message de client

    recvMes = connectionA2Client.recv(1024).decode()
    recvMes = json.loads(recvMes)
    sendMes = {} #decoder les message recevoir de json.decode

    if recvMes['type'] == 'login':  #c'est une manière tout à fait originale de vérifier le type de requête
        df = pd.read_csv('../database/candidates.csv') #Nous avons découvert plus tard que c'était similaire à l'application réelle courante.
        if df.loc[0,'isVote'] == 1:
            sendMes['isVote'] = 1
        else:
            sendMes['isVote'] = 0
        readUsers = pd.read_csv("../database/users.csv")
        users = pd.DataFrame(readUsers)
        email = recvMes['email']
        password = recvMes['password']

        for rows in users.itertuples():
            if getattr(rows, 'email') == email and getattr(rows, 'password') == password:
                if getattr(rows, 'admin') == 1:
                    sendMes['isAdmin'] = 1
                sendMes['isLogin'] = 1 #verifier le permission
                sendMes['uuid'] = getattr(rows,'uuid')
                break
            else:
                sendMes['isAdmin'],sendMes['isLogin'] = 0,0
        connectionA2Client.send((json.dumps(sendMes)).encode()) #envoyer le resultat a client

    elif recvMes['type'] == 'register': # request de s'inscrire

        username = recvMes['username']
        email = recvMes['email']
        password = recvMes['password']
        df = pd.read_csv("../database/users.csv", index_col=None)
        sendMes['isRepeat'] = 0

        for rows in df.itertuples(): #deja s'inscrire
            if getattr(rows, 'username') == username or getattr(rows, 'email') == email:
                sendMes['isRepeat'] = 1
                break

        if sendMes['isRepeat'] == 0:
            line = getattr(df, 'ID')
            lastID = int(line[-1:] + 1)
            uuid = base58.b58encode(('1' + str(lastID) + '0')).decode()
            newUser = {'ID': lastID, 'uuid': uuid, 'username': username, 'password': password, 'email': email}

            usersE = {'type':'update','uuid':uuid,'email':email}
            usersE = json.dumps(usersE)
            socketA2E.send(usersE.encode()) #envoyer le nouvel utilisateur a serveurE, serveur E va envoyer les cn(credential) a eux par email (cool!)

            df = df.append(newUser, ignore_index=True)
            df.to_csv("../database/users.csv", index=False)

        connectionA2Client.send((json.dumps(sendMes)).encode()) #envoyer le resultat a client

    elif recvMes['type'] == 'cvote':  # creer un vote

        startVote = {'type':'cvote'}  #va recevoir la list des candidates d'un admin
        startVote = json.dumps(startVote)
        socketA2E.send(startVote.encode())
        del recvMes['type']
        recvMes = list(recvMes.values())
        df = pd.DataFrame(columns=['candidates','isVote'])
        df['candidates'] = recvMes
        df.iat[0,1] = 1
        df.loc[0,'isBegin'] = 0
        df.to_csv('../database/candidates.csv',index=False)

        d = pd.DataFrame(columns=['candidate','votes'])
        for i in range(len(recvMes)):
            d = d.append({'candidate':recvMes[i],'votes':0},ignore_index=True)
        d.to_csv('../database/resultat.csv',index=False)


        recvMes = socketA2E.recv(1024).decode()
        recvMes = json.loads(recvMes)
        print(recvMes)
        df = pd.read_csv('../database/users.csv',index_col='uuid')
        for items in recvMes:
            df.loc[items[0],'pcn'] = items[1]
        df.to_csv('../database/users.csv')

        num_keys = int(len(df)/10)+1  #Générer une paire de clés secrètes Elgama pour chaque 10 utilisateurs (Une clé secrète peut décrypter plusieurs bulletins de vote)
        df = pd.read_csv('../database/cleElgama.csv',index_col=None)
        for i in range(num_keys):
            key = generateKey()
            cle_privee = key[0]
            h = key[1]
            newCle = {'cle':cle_privee,'h':h}
            df = df.append(newCle,ignore_index=True)
        df.to_csv('../database/cleElgama.csv',index=False)




    elif recvMes['type'] == 'getCandidates':  #si un utilisateur veut voter, le serveur va recevoir ce request et envoyer la list.

        df = pd.read_csv("../database/candidates.csv")
        candidates = list(df['candidates'])
        candidates = json.dumps(candidates)
        connectionA2Client.send(candidates.encode())

    elif recvMes['type'] == 'sendVeri': #envoyer un nombre XXXX de 4bytes a l'email de utilisateur
        receiver = recvMes['email']  #(meilleur si par SMS car c'est pas securise si 2 methode de securisation sont realisee par un meme facon)
        randnum = random.randrange(1000,9999)
        mailVeri(receiver,randnum)
        randnum = md5(str(randnum).encode(encoding='utf-8')).hexdigest()

    elif recvMes['type'] == 'startZERO': #la preparation avant la ZKP
        w = random.randrange(2,92904936882697929445726711920691941953763517081)
        A = Montgomery(g,w,p)

        df = pd.read_csv('../database/cleElgama.csv')# alea pour generer cle pour Elgama
        rand = random.randrange(0,len(df))
        cle_privee = df.loc[rand,'cle']
        h = int(df.loc[rand,'h'])
        print(f'h:{h}')

        print(f'A:{A}')
        sendMes = {'A':A,'w':w,'h':h}
        sendMes = json.dumps(sendMes)
        connectionA2Client.send(sendMes.encode())

    elif recvMes['type'] == 'ZERO': #la fonction de calculer si A=g^w=g^reponse * pcn^challenge = A'   2ZKP + 1 chiffrement (ZKP de cn, ZKP de c2, chiffrement Elgama(c1,c2))
        challenge = recvMes['challenge'] #et aussi recevoir le vote chiffrer par Elgama
        response = recvMes['response'] #et aussi la SIGNATURE RSA de c2
        recvVeri = recvMes['veri']
        uuid = recvMes['uuid']

        c = recvMes['c']
        signature = recvMes['signature']
        e = recvMes['e']
        n = recvMes['n']

        c1 = c[0]
        c2 = c[1]
        print(f'signature:{signature}')
        print(f'c2:{c2}')
        checkSignature = Montgomery(signature,e,n)
        print(f'check:{checkSignature}')


        df = pd.read_csv('../database/users.csv',index_col='uuid')
        pcn = df.loc[uuid,'pcn']
        pcn = int(pcn)
        A1 = Montgomery(pcn, challenge, p) * Montgomery(g, -response * (p - 2), p) % p
        print(f'A1={A1}')
        df = pd.read_csv('../database/checkVote.csv')
        isrepeat = 0
        if A == A1 and recvVeri == randnum and checkSignature == c2:
            for rows in df.itertuples():  # deja vote ou non
                if getattr(rows, 'uuid') == uuid:
                    sendMes = 'repeat'
                    isrepeat = 1
                    break
            if isrepeat != 1:  # c'est d a dire a reussi, envoyer la liste a serverur S
                sendMes = 'success'
                timeNow = time.strftime("%d-%m-%Y %H:%M",time.localtime())
                newVote = {'type':'bulletin',
                           'uuid': str(uuid),
                           'c1': int(c1),
                           'c2': int(c2),
                           'signature': str(signature),
                           'cle_privee': int(cle_privee),
                           'time': timeNow}
                print(newVote)
                message = decrypt(c1, c2, cle_privee)
                print(f'message:{message}')
                newVote = json.dumps(newVote)
                socketA2S.send(newVote.encode())
        else:
            sendMes = 'failed'
        sendMes = json.dumps(sendMes)
        connectionA2Client.send(sendMes.encode())

    elif recvMes['type'] == 'verify':  #c'est tres simple ici parceque la list de signature est generer pas la serveur S, seveurA est seulement un 'canal'
        print('receive')
        socketA2S.send(json.dumps(recvMes).encode())
        recvMes = socketA2S.recv(1024).decode()
        connectionA2Client.send(recvMes.encode())
        print('send')

    elif recvMes['type'] == 'stopVote': #quand l'admin entrer la page de depouillement
        df = pd.read_csv('../database/candidates.csv')
        df.loc[0,'isVote'] = 0
        if df.loc[0,'isBegin'] == 0:   #si c'est la premiere admin qui commence la depouillement.
            sendMes = {'type': 'initial'}
            socketA2S.send(json.dumps(sendMes).encode())
            recvMes = socketA2S.recv(1024).decode()
            connectionA2Client.send(recvMes.encode())
        else:
            sendMes = {'type': 'getPara'}  # si la depouillement est deja commence.
            socketA2S.send(json.dumps(sendMes).encode())  #il y a une grande difference parce que on va copier le csv de les vote a un csv nommé 'votesRestes'
            recvMes = socketA2S.recv(1024).decode() # et dans la phase de depouillment, les vote correspendant a la cle de entreé vont etre transféré a un autre csv nommé 'votesComptés'
            connectionA2Client.send(recvMes.encode())  #seule la premiere admin va executer l'initiation
        df.to_csv('../database/candidates.csv',index=False)

    elif recvMes['type'] == 'calculate':    #envoyer la demande de calculer les resultat de vote a serveur S
        iffound = 0 #les votes correspendant a la cle va etre transféré a
        df = pd.read_csv('../database/cleElgama.csv')

        for rows in df.itertuples():
            if str(getattr(rows,'cle')) == str(recvMes['cle']):
                iffound = 1
                break
        if iffound == 1:
            sendMes = {'type':'calculate','cle':recvMes['cle']} #si la clé validé
            socketA2S.send(json.dumps(sendMes).encode())
            recvMes = socketA2S.recv(1024).decode()
            connectionA2Client.send(recvMes.encode())
        else:
            sendMes = 'notfound' #si non
            connectionA2Client.send(json.dumps(sendMes).encode())
        print(iffound)


    if not recvMes:
        break
connectionA2Client.close()  #se temine si le client a quité




# connectionSocket.send(message1).encode()
# message2 = connectionSocket.recv(1024).decode()
# connectionSocket.send((message2 + "123").encode())
# print(message1)
# connectionSocket.close()

