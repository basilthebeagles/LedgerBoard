
import ecdsa
import time
import hashlib
import binascii
import binascii

import bcrypt



"0998b81f244478aad5f512262bf46490991a36bfb2c9f30547282f7499d4dfd4034b9364e012765be5410b3650c9a72a1d3e836b598877c5059b316727f93a9ca57ccd40d5aa531a8c9df7a31209d0b582f86192068f7820da0cef6bbc0668f64e6a5031cc2e711be72b88f53ca360c965232a7fac3ef71121c459352968802e546de0c80fb97541ca0678da7a4631425b05461e2c9265f2f763e79b9e2b544deb02ae063657ac8d3365421ce03f8e3cd2224dec828cf167ca2b6d6f0ae6caf53ce164e6507a994179910258daa07b4da6bdd053db944b7a68a93840dc6603d291f93e400245d351238fbaea8f5d96a1fe908a21a08ddc5603ea4b4f70df8a59e44453e063056ba918e40afc10cdf63e5f6ffc3ec797081d5b0ab8d2b3be5356aa5236179da37eca43cd55d861cfbff069b1a91b094a7a3ed2b34174b69be7b7b920a63c1be5877f56dfe24a5c949a2b6ef2a8e90e90c44945b108c745b20d39b7e1e3e3fa60725494ce6d8dce60748c8c7472f2519336fd169b73bfeccbc3cfb11db3fc5b0d5f21818a3fb539095e60f42e03b4e7a466266e000dc4004bb882c797f2931d86ecacf615b048984200b83748dd465f199e88a3b2bc387618102fea5952478ee15d4a7ecced95555e0218958db3fc37177c97a10963ceb85bc38350d4a51c0c3c4c50a963cc8416d65b9685c68b431106d621a43d3183f2496172"

print(bcrypt.kdf(password="New World".encode('utf-8'), salt= bytes(1), rounds= 100, desired_key_bytes= 32).hex())

'''
sk = ecdsa.SigningKey.generate(curve= ecdsa.SECP256k1)
vk = sk.get_verifying_key()

print(sk.to_string().hex())
print(vk.to_string().hex())
'''

privateKey = "726e05ccf0fbbcde14674d64c749d04ca8e8ca68e91692468beedd466bb80a3f"    #"4254014fd2e94bb30c3b3ffea907bf51ab06fc56c5a170bab4f7c43a1aa048e2"

publicKey =  "9f44b86ad077235836ad5290cd9060f460818891341e9d3e1be97566e9e308f5f272af356544b9096d73e99b04f82da275b2c21562419f7732858311dddb3b18"  #"4f5d196638d00cb0c4c9b68a68edd3bad0247b855ecfb3bb171738f79078267760c6576dc2847185552e478064a4fbf65e14254e5ceb90e7113cfc7ae619063c"




content = "testing"
#fix not working wont verify on back end
timeStamp = int(time.time()) + 30
print(timeStamp)

print('here1')

totalPostContent = publicKey + str(timeStamp) + content
print('here2')
postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()



#print(str(totalPostContent))

print(postHash)

sk = ecdsa.SigningKey.from_string(bytes.fromhex(privateKey), curve= ecdsa.SECP256k1)

print('here3')


signature = sk.sign(bytes.fromhex(postHash)).hex()
print('here4')

#signature = "784d9d79e8a8668f155d78d87ff6956b4e5ecfaea72d58168022d2bd9a663c8e8220eab68a4dd8bf9cf0103a2e3204361f5ff66698140e03e90e14442e44c24f"
print(signature)


vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1)


print(vk.verify(bytes.fromhex(signature), bytes.fromhex(postHash)) )# if postHash is a hex string then use bytes.fromhex


