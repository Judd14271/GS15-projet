# import random
# from Montgomery import Montgomery
# from hashlib import md5
#
#
#
# def miller_rabin(n, k):
#
#     # Implementation uses the Miller-Rabin Primality Test
#     # The optimal number of rounds for this test is 40
#     # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
#     # for justification
#
#     # If number is even, it's a composite number
#
#     if n == 2:
#         return True
#
#     if n % 2 == 0:
#         return False
#
#     r, s = 0, n - 1
#     while s % 2 == 0:
#         r += 1
#         s //= 2
#     for _ in range(k):
#         a = random.randrange(2, n - 1)
#         x = pow(a, s, n)
#         if x == 1 or x == n - 1:
#             continue
#         for _ in range(r - 1):
#             x = pow(x, 2, n)
#             if x == n - 1:
#                 break
#         else:
#             return False
#     return True
#
#
# #92904936882697929445726711920691941953763517081
# #7
#
# for i in range(1000):
#     num = random.randrange(10000000000000000000000000000000000000000000000,99999999999999999999999999999999999999999999999)
#     if miller_rabin(num,100):
#         print(f'{i}:{num}')
#
# def multimod(a,k,n):    #快速幂取模
#     ans=1
#     while(k!=0):
#         if k%2:         #奇数
#             ans=(ans%n)*(a%n)%n
#         a=(a%n)*(a%n)%n
#         k=k//2          #整除2
#     return ans
#
# def yg(n):		# 这样默认求最小原根
#     k=(n-1)//2
#     for i in range(2,n-1):
#         if i<100:
#             if multimod(i,k,n)!=1:
#                 print(i)
#         else:break
#
#
#
# print(yg(92904936882697929445726711920691941953763517081))

# import pandas as pd
# a = [(1,3),(2,11),(4,111),(3,131),(5,141),(6,151)]
# df = pd.read_csv('../database/xxx.csv',index_col='uuid')
# print(df)
# for items in a:
#     df.loc[items[0],'pcn'] = items[1]
# print(df)
# df.to_csv('../database/xxx.csv')
# #
# # print(df)
#
from  Montgomery import Montgomery
import random
p = 92904936882697929445726711920691941953763517081
g = 7
# pcn = 5017354747157304787591879445259692833524696798
# w = random.randrange(2,92904936882697929445726711920691941953763517081)
# A = Montgomery(g,w,p)
# A1 = Montgomery(pcn, challenge, p) * Montgomery(g, -response * (p - 2), p) % p
# print(f'A:{A}')
# sendMes = {'A':A,'w':w}
#91256125938284864977183353476741008361764787775

cn = 'C6kpZRaQ3yuDweo'
s = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
cnIndex = ''.join([str(list(s).index(i)) for i in list(cn)])
cnIndex = int(cnIndex) % p
print(cnIndex)
pcn = Montgomery(g,cnIndex,p)
print(pcn)