
import ecdsa
import time
import hashlib
import binascii

privateKey = "15d0dbf0ade8450b6d4b4e6820e66cfacd7eca446856dfc067c06bbdbbdbdb99"

publicKey = "f2d6daeaeeaeb800ba6aa1b31f254c3cfbe315361c3bcbf24473e17a5939e4784a22245df2e41f5b8ebfad5f9c130a9093b57a26f82bf7546084c13957d51b78"

content = "test test test"

timeStamp = 1234567#int(time.time())

print("ehll")

totalPostContent = publicKey + content + str(timeStamp)

postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()

print(postHash)

sk = ecdsa.SigningKey.from_string(string=bytes.fromhex(privateKey), curve= ecdsa.SECP256k1)



signature = sk.sign(postHash.encode('utf-8')).hex()
#signature = "784d9d79e8a8668f155d78d87ff6956b4e5ecfaea72d58168022d2bd9a663c8e8220eab68a4dd8bf9cf0103a2e3204361f5ff66698140e03e90e14442e44c24f"
print(signature)


vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1)

print(vk.verify(bytes.fromhex(signature), bytes.fromhex(postHash)) ) # if postHash is a hex string then use bytes.fromhex
