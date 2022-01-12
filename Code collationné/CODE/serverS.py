from socket import *
from encryptions import *
import json
import pandas as pd
from encryptions import decrypt
import re

from Montgomery import Montgomery

socketA2S = socket(AF_INET, SOCK_STREAM)
socketA2S.bind((gethostname(), 1300))

socketA2S.listen(2)
print('Server Ready')

connectionS2A,address = socketA2S.accept()
print('已与A服务器建立连接！')
str1 = list('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

while True:

    recvMes = connectionS2A.recv(1024).decode()
    recvMes = json.loads(recvMes)
    sendMes = {} #初始化收发信息

    if recvMes['type'] == 'verify':   #envoyer la liste de signature pour verifier la existance de vote
        print('verify')
        checkList = []
        df = pd.read_csv('../database/checkVote.csv', index_col=None)
        df = df[['time', 'signature']]
        print('df')
        for rows in range(len(df)):
            checkList.append((df.loc[rows, 'time'], df.loc[rows, 'signature']))
        sendMes = json.dumps(checkList).encode()
        connectionS2A.send(sendMes)
        print('send')

    elif recvMes['type'] == 'bulletin':  #recevoir la vote validé est la restorer
        print(f'recv{recvMes}')
        del recvMes['type']
        print(f'recv{recvMes}')
        df = pd.read_csv('../database/checkVote.csv', index_col=None)
        df = df.append(recvMes, ignore_index=True)
        df.to_csv("../database/checkVote.csv", index=False)

    elif recvMes['type'] == 'getPara':  #Envoi la situation du décompte actuel des votes
        print('para')
        df = pd.read_csv('../database/cleElgama.csv')
        nrest_keys = str(len(df))
        df = pd.read_csv('../database/votesComptes.csv')
        ncompte_votes = str(len(df))
        df = pd.read_csv('../database/votesRestes.csv')
        nrest_votes = str(len(df))
        sendMes = {'nrest_keys': nrest_keys, 'ncompte_votes': ncompte_votes, 'nrest_votes': nrest_votes}
        print(f'send{sendMes}')
        sendMes = json.dumps(sendMes)
        connectionS2A.send(sendMes.encode())

    elif recvMes['type'] == 'initial': #initialiser la depouilment, terminer la vote pour les votant
        print('ini')

        df = pd.read_csv('../database/checkVote.csv')
        df.to_csv('../database/votesRestes.csv',index=False)

        df = pd.read_csv('../database/cleElgama.csv')
        nrest_keys = str(len(df))
        df = pd.read_csv('../database/votesComptes.csv')
        ncompte_votes = str(len(df))
        df = pd.read_csv('../database/votesRestes.csv')
        nrest_votes = str(len(df))
        df = pd.read_csv('../database/resultat.csv')
        hi = df['votes'].max()
        for i in range(len(df)):
            if df.loc[i, 'votes'] == hi:
                final = df.loc[i, 'candidate']
        if nrest_votes != '0':
            final = ''
        sendMes = {'nrest_keys': nrest_keys, 'ncompte_votes': ncompte_votes, 'nrest_votes': nrest_votes, 'final': final}
        print(f'send{sendMes}')
        sendMes = json.dumps(sendMes)
        connectionS2A.send(sendMes.encode())

    elif recvMes['type'] == 'calculate':  #recevoir la cle valide
        print(f'calculate{recvMes}')   #copier la liste de vote a un nouvel csv 'votesRestes.csv'
        cle = recvMes['cle']        #trouver les votes correspendantes a la cle
        dfE = pd.read_csv('../database/cleElgama.csv')  #envoyer les votes correspendantes a la csv 'voteComptes.csv'
        for i in range(len(dfE)):                        #calculer les resultat en utilisant decrypt(c1,c2,cle)  (dans encryptions.py)
            if str(dfE.loc[i,'cle']) == cle:
                dfE = dfE.drop(labels=i)
        dfE.to_csv('../database/cleElgama.csv',index=False)

        dfR = pd.read_csv('../database/votesRestes.csv')
        dfC = pd.read_csv('../database/votesComptes.csv')
        for i in range(len(dfR)):
            if str(dfR.loc[i,'cle_privee']) == cle:
                resultat = decrypt(int(dfR.loc[i,'c1']),int(dfR.loc[i,'c2']),int(cle))

                list = re.findall(r'.{2}', str(resultat))
                resultat = ''.join([str1[int(x)] for x in list])
                df = pd.read_csv('../database/resultat.csv')
                for j in range(len(df)):
                    if df.loc[j,'candidate'] == resultat:
                        df.loc[j,'votes'] += 1

                dfC = dfC.append(dfR.iloc[i])
                dfR = dfR.drop(labels=i)
        dfR.to_csv('../database/votesRestes.csv',index=False)
        dfC.to_csv('../database/votesComptes.csv',index=False)
        df.to_csv('../database/resultat.csv',index=False)

        df = pd.read_csv('../database/cleElgama.csv')
        nrest_keys = str(len(df))
        df = pd.read_csv('../database/votesComptes.csv')
        ncompte_votes = str(len(df))
        df = pd.read_csv('../database/votesRestes.csv')
        nrest_votes = str(len(df))
        df = pd.read_csv('../database/resultat.csv')
        hi = df['votes'].max()
        print(f'hi{hi}')
        for i in range(len(df)):
            if df.loc[i,'votes'] == hi:
                final = df.loc[i,'candidate']
        print(f'final{final}')
        print(f'nhest{nrest_votes}')
        if nrest_votes != '0':
            final = ''
        print(f'final{final}')
        sendMes = {'nrest_keys': nrest_keys, 'ncompte_votes': ncompte_votes, 'nrest_votes': nrest_votes,'final':final}
        print(f'send{sendMes}')
        sendMes = json.dumps(sendMes)
        connectionS2A.send(sendMes.encode())






    if not recvMes:
        break
connectionS2A.close()