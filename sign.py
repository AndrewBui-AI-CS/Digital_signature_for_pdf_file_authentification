# import hashlib
# from types import CodeType
# from typing import MutableSequence
# import rsa

# CA = {}

# def rsaEncrypt(str,privk):
#     print(str)
#     content = str.encode('utf-8')
#     crypto = rsa.sign(content,privk,'SHA-1')
#     print('here')
#     print(crypto)
#     return crypto


# def rsaDecrypt(mess, signa, pubk):

#     try:
#         rsa.verify(mess.encode(),signa,pubk)
#     except rsa.VerificationError:
#         result = False
#     else:
#         result = True
#     return result

# def applyKey(name,pubk):

#     CA[name] = pubk

# class User:
#     def __init__(self,name):
#         self.name = name
#         self.crypto = ''

#         (self.pubkey,self.privkey) = rsa.newkeys(512)
#         applyKey(self.name,self.pubkey)

#     def sign(self,str):
#         self.crypto = rsaEncrypt(hashlib.md5((str + self.name).encode()).hexdigest(),self.privkey)
#         print(self.crypto.decode('utf-8'))
#         return self.crypto.decode('unicode_escape')

#     def check(self,str,user,crypto):
#         crypto=bytes(crypto,'latin-1')
#         if user.name not in CA:
#             print("khong ton tai")
#         else:
#             pubk = CA[user.name]
#             if rsaDecrypt(hashlib.md5((str+user.name).encode()).hexdigest(),crypto,pubk):
#                 print("xac minh thanh cong")
#             else:
#                 print("khong xac minh")

# message = 'test123'
# user1 = User('user1')
# demo = user1.sign(message)
# print(type(demo))
# print(demo)

# user2 = User('user2')
# user2.check(message, user1, demo)
# user3 = User('user3')
# print("{0} {1} ".format(user1.name,message))
# miwen = user1.sign(message)
# print(miwen)
# print(type(miwen))
#a=miwen.decode('unicode_escape')
#b=bytes(a,'latin-1')

# user2.check(message,user1,miwen)

from json import encoder
from Crypto.PublicKey import RSA
from numpy.testing._private.utils import decorate_methods
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

# Generate 1024-bit RSA key pair (private + public key)
def generateKey():
    priKey = RSA.generate(bits=1024) #private key
    pubKey = priKey.publickey()
    return priKey, pubKey

# Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
def sign_msg(msg, sk):
    hash = SHA256.new(msg)
    signer = PKCS115_SigScheme(sk)
    signature = signer.sign(hash)
    return signature

# Verify valid PKCS#1 v1.5 signature (RSAVP1)
def verify_msg(message, pubkey, sig):
    hash = SHA256.new(message)
    verifier = PKCS115_SigScheme(pubkey)
    try:
        verifier.verify(hash, sig)
        print("Signature is valid.")
        return True
    except:
        print("Signature is invalid.")
        return False


# sk, pk = generateKey()
# msg = b'buiviethoang'
# signature = sign_msg(msg, sk)
# sig_modify = binascii.hexlify(signature).decode('utf-8')
# sig2 = binascii.unhexlify(sig_modify)
# print(signature)
# print(sig_modify)
# print(sig2)
# print(binascii.unhexlify(bytes(sig_modify, 'utf-8')))
# verify_msg(bytes(mess, 'utf-8'), pk, bytes(sig_modify, 'utf-8'))
