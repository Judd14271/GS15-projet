from hashlib import sha256
import hmac
import math
import random
import numpy as np
import base64
from Montgomery import Montgomery



p = 92904936882697929445726711920691941953763517081
g = 7

def hmac_sha256(uuid):
    uuid = str(uuid)
    str1 = list('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
    cn = random.sample(str1, 14)
    sumIndex = sum([str1.index(x) for x in cn])
    cnIndex = [str(str1.index(x)) for x in cn]
    checksum = str1[(53 - sumIndex) % 53]
    cnIndex.append(str((53 - sumIndex) % 53))
    cn.append(checksum)
    cn = ''.join(cn)
    cnIndex = ''.join(cnIndex)
    cnIndex = int(cnIndex)
    message = cn.encode()
    for i in range(1000):
        message = hmac.new(uuid.encode('utf-8'), message, digestmod=sha256).hexdigest()
        message = message.encode('utf-8')
    message = message.decode()
    message = int(message,16)
    message = str(message)
    # message = bin(int(message,16))[2:].zfill(256)
    return {'secret':message,'cn':cn,'cnIndex':cnIndex}

def into_256bit(message):
    message = bin(int(message,16))[2:].zfill(256)
    return message

# print(hmac_sha256(123))

def xxx(uuid):
    uuid = str(uuid)
    lista = [str(x) for x in range(0,58)]
    cnIndex = random.sample(lista, 14)
    cnIndex = ''.join(cnIndex)
    cnIndex = int(cnIndex)%p
    print(f'cn:{cnIndex}')
    A = str(Montgomery(g,113,p))
    print(f'A:{A}')
    A = A.encode()
    challenge = hmac.new(uuid.encode('utf-8'), A, digestmod=sha256).hexdigest()
    challenge = challenge.encode('utf-8')
    challenge = challenge.decode()
    challenge = int(challenge, 16)%p
    print(f'challenge:{challenge}')
    resp = 113 - cnIndex*challenge
    print(f'resp:{resp}')
    pcn = Montgomery(g, cnIndex, p)
    print(f'pcn:{pcn}')
    A1 = (Montgomery(pcn,challenge,p) * Montgomery(g, -resp * (p - 2), p)) % p
    print(A1)
