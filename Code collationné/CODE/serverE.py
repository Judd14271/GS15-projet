from socket import *
from encryptions import *
import json
import pandas as pd
from sendEmail import mailCn
from encryptions import hmac_sha256
from Montgomery import Montgomery

socketA2E = socket(AF_INET, SOCK_STREAM)
socketA2E.bind((gethostname(), 1100))

socketA2E.listen(2)
print('Server Ready')

connectionE2A,address = socketA2E.accept()
print('已与A服务器建立连接！')

p = 92904936882697929445726711920691941953763517081
g = 7
while True:

    recvMes = connectionE2A.recv(1024).decode()
    recvMes = json.loads(recvMes)
    sendMes = {}

    if recvMes['type'] == 'update':  #si un nouvel utilisateur est inscrit

        uuid = recvMes['uuid']
        email = recvMes['email']
        newUsers = {'uuid':uuid,'email':email}
        print(newUsers)
        df = pd.read_csv("../database/serverE.csv", index_col=None)
        df = df.append(newUsers, ignore_index=True)
        df.to_csv("../database/serverE.csv", index=False)

    elif recvMes['type'] == 'cvote': #la commande de creer un vote

        indexT = 0
        sendMes = []
        df = pd.read_csv("../database/serverE.csv", index_col=None)
        for users in df.itertuples(): # fonction de generer la credential (cn)
            uuid = getattr(users,'uuid')
            receiver = getattr(users,'email')
            X = hmac_sha256(uuid)
            cn = X['cn']
            cnIndex = X['cnIndex']
            secret = X['secret']
            mailCn(receiver,cn)  # envoyer a chaque utilisateur leur cn propre
            pcn = str(Montgomery(g,cnIndex,p))
            df.loc[indexT,'pcn'] = pcn
            df.loc[indexT,'secret'] = secret
            tup = (uuid,pcn)
            sendMes.append(tup)
            indexT += 1
            print(tup)
            df.to_csv("../database/serverE.csv", index=False)
        print(sendMes)
        connectionE2A.send(json.dumps(sendMes).encode())

    if not recvMes:
        break
connectionE2A.close()

