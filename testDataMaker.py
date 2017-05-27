
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

privateKey = "15d0dbf0ade8450b6d4b4e6820e66cfacd7eca446856dfc067c06bbdbbdbdb99"    #"4254014fd2e94bb30c3b3ffea907bf51ab06fc56c5a170bab4f7c43a1aa048e2"

publicKey =  "f2d6daeaeeaeb800ba6aa1b31f254c3cfbe315361c3bcbf24473e17a5939e4784a22245df2e41f5b8ebfad5f9c130a9093b57a26f82bf7546084c13957d51b78"  #"4f5d196638d00cb0c4c9b68a68edd3bad0247b855ecfb3bb171738f79078267760c6576dc2847185552e478064a4fbf65e14254e5ceb90e7113cfc7ae619063c"

content = "test test test"

timeStamp = 1234567#int(time.time())


totalPostContent = publicKey + content + str(timeStamp)

postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()

print(postHash)

sk = ecdsa.SigningKey.from_string(bytes.fromhex(privateKey), curve= ecdsa.SECP256k1)



signature = sk.sign(bytes.fromhex(postHash)).hex()
#signature = "784d9d79e8a8668f155d78d87ff6956b4e5ecfaea72d58168022d2bd9a663c8e8220eab68a4dd8bf9cf0103a2e3204361f5ff66698140e03e90e14442e44c24f"
print(signature)


vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1)


print(vk.verify(bytes.fromhex(signature), bytes.fromhex(postHash)) )# if postHash is a hex string then use bytes.fromhex
