from hashlib import sha256
import hmac
import math
import random
import numpy as np
import base64
from rsa import newkeys
from Montgomery import Montgomery



p = 92904936882697929445726711920691941953763517081
g = 7

def hmac_sha256(uuid):
    uuid = str(uuid)
    str1 = list('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
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

def generateKey():
    cle_privee = random.randrange(10000, 99999)
    h = Montgomery(g, cle_privee, p)
    return (cle_privee,h)

def encrypt(key,message):
    cle_publique = random.randrange(2,p)
    c1 = Montgomery(g,cle_publique,p)
    c2 = message*(Montgomery(key,cle_publique,p))%p
    return (c1,c2)

def decrypt(c1,c2,cle_privee):
    h1 = Montgomery(c1, p-1-cle_privee, p)
    return c2*h1%p

def fast_power(base, power, n):
    result = 1
    tmp = base
    while power > 0:
        if power&1 == 1:
            result = (result * tmp) % n
        tmp = (tmp * tmp) % n
        power = power>>1
    return result

def Miller_Rabin(n, iter_num):
    # 2 is prime
    if n == 2:
        return True
    # if n is even or less than 2, then n is not a prime
    if n&1 == 0 or n<2:
        return False
    # n-1 = (2^s)m
    m,s = n - 1,0
    while m&1==0:
        m = m>>1
        s += 1
    # M-R test
    for _ in range(iter_num):
        b = fast_power(random.randint(2,n-1), m, n)
        if b==1 or b== n-1:
            continue
        for __ in range(s-1):
            b = fast_power(b, 2, n)
            if b == n-1:
                break
        else:
            return False
    return True

def signer(message):
    signaturePub, signaturePri = newkeys(256)
    n = signaturePub[0]
    e = signaturePub[1]
    d = signaturePri[2]
    signature = Montgomery(message,d,n)
    return signature,e,n






