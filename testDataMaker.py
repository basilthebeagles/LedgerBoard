
import ecdsa
import time
import hashlib
import binascii
import binascii





'''
sk = ecdsa.SigningKey.generate(curve= ecdsa.SECP256k1)
vk = sk.get_verifying_key()

print(sk.to_string().hex())
print(vk.to_string().hex())
'''

privateKey = "726e05ccf0fbbcde14674d64c749d04ca8e8ca68e91692468beedd466bb80a3f"    #"4254014fd2e94bb30c3b3ffea907bf51ab06fc56c5a170bab4f7c43a1aa048e2"

publicKey =  "9f44b86ad077235836ad5290cd9060f460818891341e9d3e1be97566e9e308f5f272af356544b9096d73e99b04f82da275b2c21562419f7732858311dddb3b18"  #"4f5d196638d00cb0c4c9b68a68edd3bad0247b855ecfb3bb171738f79078267760c6576dc2847185552e478064a4fbf65e14254e5ceb90e7113cfc7ae619063c"

content = "testing 54321"
#fix not working wont verify on back end
timeStamp = int(time.time()) + 30
print(timeStamp)

print('here1')





totalPostContent= publicKey + content + str(timeStamp)
print('here2')
print(str(totalPostContent))
postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()

print(postHash)

sk = ecdsa.SigningKey.from_string(bytes.fromhex(privateKey), curve= ecdsa.SECP256k1)

print('here3')


signature = sk.sign(bytes.fromhex(postHash)).hex()
print('here4')

#signature = "784d9d79e8a8668f155d78d87ff6956b4e5ecfaea72d58168022d2bd9a663c8e8220eab68a4dd8bf9cf0103a2e3204361f5ff66698140e03e90e14442e44c24f"
print(signature)


vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1)


print(vk.verify(bytes.fromhex(signature), bytes.fromhex(postHash)) )# if postHash is a hex string then use bytes.fromhex


