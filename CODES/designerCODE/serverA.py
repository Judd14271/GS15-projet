import json
import random
from socket import *
from sendEmail import mailVeri
import pandas as pd
import base58
from hashlib import md5
from Montgomery import Montgomery

socketA2Client = socket(AF_INET, SOCK_STREAM)
socketA2Client.bind((gethostname(), 1200)) # 服务器为A

socketA2E = socket(AF_INET, SOCK_STREAM)
socketA2E.connect((gethostname(), 1100)) # 作为client连接服务器E

socketA2Client.listen(2)
print('Server Ready') #等待client连接

connectionA2Client, address = socketA2Client.accept()
print('已建立一个连接：',address) #与client连接成功
p = 92904936882697929445726711920691941953763517081
g = 7
randnum = 1
while True:

    recvMes = connectionA2Client.recv(1024).decode()
    recvMes = json.loads(recvMes)
    sendMes = {} #初始化收发信息

    if recvMes['type'] == 'login': #检验请求类型

        readUsers = pd.read_csv("../database/users.csv")
        users = pd.DataFrame(readUsers)
        email = recvMes['email']
        password = recvMes['password']

        for rows in users.itertuples():
            if getattr(rows, 'email') == email and getattr(rows, 'password') == password:
                if getattr(rows, 'admin') == 1:
                    sendMes['isAdmin'] = 1
                sendMes['isLogin'] = 1 #核对登录用户权限
                sendMes['uuid'] = getattr(rows,'uuid')
                break
            else:
                sendMes['isAdmin'],sendMes['isLogin'] = 0,0
        connectionA2Client.send((json.dumps(sendMes)).encode()) #返回是否成功登录信息

    elif recvMes['type'] == 'register': #注册行为

        username = recvMes['username']
        email = recvMes['email']
        password = recvMes['password']
        df = pd.read_csv("../database/users.csv", index_col=None)
        sendMes['isRepeat'] = 0

        for rows in df.itertuples(): #检查是否已经注册
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
            socketA2E.send(usersE.encode()) #将新注册用户信息发给E服务器

            df = df.append(newUser, ignore_index=True)
            df.to_csv("../database/users.csv", index=False) #完成新用户注册

        connectionA2Client.send((json.dumps(sendMes)).encode()) #返回是否注册成功信息

    elif recvMes['type'] == 'vote':

        startVote = {'type':'vote'}
        startVote = json.dumps(startVote)
        socketA2E.send(startVote.encode())
        del recvMes['type']
        recvMes = list(recvMes.values())
        df = pd.DataFrame(columns=['candidates','isVote'])
        df['candidates'] = recvMes
        df.iat[0,1] = 1
        df.to_csv('../database/candidates.csv',index=False)
        recvMes = socketA2E.recv(1024).decode()
        recvMes = json.loads(recvMes)
        print(recvMes)
        df = pd.read_csv('../database/users.csv',index_col='uuid')
        for items in recvMes:
            df.loc[items[0],'pcn'] = items[1]
        df.to_csv('../database/users.csv')


    elif recvMes['type'] == 'getCandidates':

        df = pd.read_csv("../database/candidates.csv")
        if df['isVote'][0] == 0:
            candidates = 'noVote'
        else:
            candidates = list(df['candidates'])
        candidates = json.dumps(candidates)
        connectionA2Client.send(candidates.encode())

    elif recvMes['type'] == 'sendVeri':
        receiver = recvMes['email']
        randnum = random.randrange(1000,9999)
        mailVeri(receiver,randnum)
        randnum = md5(str(randnum).encode(encoding='utf-8')).hexdigest()

    elif recvMes['type'] == 'startZERO':
        w = random.randrange(2,92904936882697929445726711920691941953763517081)
        A = Montgomery(g,w,p)
        print(f'A:{A}')
        sendMes = {'A':A,'w':w}
        sendMes = json.dumps(sendMes)
        connectionA2Client.send(sendMes.encode())

    elif recvMes['type'] == 'ZERO':
        challenge = recvMes['challenge']
        response = recvMes['response']
        recvVeri = recvMes['veri']
        uuid = recvMes['uuid']
        df = pd.read_csv('../database/users.csv',index_col='uuid')
        pcn = df.loc[uuid,'pcn']
        pcn = int(pcn)
        print(pcn)
        A1 = Montgomery(pcn, challenge, p) * Montgomery(g, -response * (p - 2), p) % p
        print(f'A1={A1}')
        if A == A1 and recvVeri == randnum:
            sendMes = 'success'
        else:
            sendMes = 'failed'
        sendMes = json.dumps(sendMes)
        connectionA2Client.send(sendMes.encode())




    if not recvMes:
        break
connectionA2Client.close()




# connectionSocket.send(message1).encode()
# message2 = connectionSocket.recv(1024).decode()
# connectionSocket.send((message2 + "123").encode())
# print(message1)
# connectionSocket.close()

