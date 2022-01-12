from json import encoder
from tkinter.constants import S
from Crypto.PublicKey import RSA
from numpy.testing._private.utils import decorate_methods
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

# Generate 1024-bit RSA key pair (private + public key)


def generateKey():
    priKey = RSA.generate(bits=1024)  # private key
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


#sk, pk = generateKey()
# f = open('public.pem', 'wb')
# f.write(pk.publickey().exportKey('PEM'))
# f.close()

# msg = b'buiviethoang'
# mess = 'buiviethoang'
# #Read key from file
# f = open('public.pem', 'rb')
# key = RSA.importKey(f.read())
# print(key)
# print(type(key))
# signature = sign_msg(msg, sk)
# sig_modify = binascii.hexlify(signature).decode('utf-8')
# sig2 = binascii.unhexlify(sig_modify)
# print(signature)
# print(sig_modify)
# print(sig2)
# print(binascii.unhexlify(bytes(sig_modify, 'utf-8')))
# # verify_msg(bytes(mess, 'utf-8'), pk, bytes(sig_modify, 'utf-8'))
# verify_msg(bytes(mess, 'utf-8'), key, sig2)
