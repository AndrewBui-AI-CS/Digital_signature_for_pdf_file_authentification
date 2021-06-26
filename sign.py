import hashlib
import rsa

CA = {}

def rsaEncrypt(str,privk):

    content = str.encode('utf-8')

    crypto = rsa.sign(content,privk,'SHA-1')
    return crypto

def rsaDecrypt(mess, signa, pubk):

    try:
        rsa.verify(mess.encode(),signa,pubk)
    except rsa.VerificationError:
        result = False
    else:
        result = True
    return result

def applyKey(name,pubk):

    CA[name] = pubk

class User:
    def __init__(self,name):
        self.name = name
        self.crypto = ''

        (self.pubkey,self.privkey) = rsa.newkeys(512)
        applyKey(self.name,self.pubkey)

    def sign(self,str):
        self.crypto = rsaEncrypt(hashlib.md5((str + self.name).encode()).hexdigest(),self.privkey)
        return self.crypto

    def check(self,str,user,crypto):
        if user.name not in CA:
            print("k ton tai")
        else:
            pubk = CA[user.name]
            if rsaDecrypt(hashlib.md5((str+user.name).encode()).hexdigest(),crypto,pubk):
                print("xac minh thanh cong")
            else:
                print("khong xac minh")

message = 'test123'
user1 = User('user1')
user2 = User('user2')
user3 = User('user3')
print("{0} {1} ".format(user1.name,message))
miwen = user1.sign(message)

user2.check(message,user1,miwen)

user3.check(message,user2,miwen)