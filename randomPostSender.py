
import ecdsa
import time
import hashlib
import binascii
import binascii
from random import randint

import bcrypt



"0998b81f244478aad5f512262bf46490991a36bfb2c9f30547282f7499d4dfd4034b9364e012765be5410b3650c9a72a1d3e836b598877c5059b316727f93a9ca57ccd40d5aa531a8c9df7a31209d0b582f86192068f7820da0cef6bbc0668f64e6a5031cc2e711be72b88f53ca360c965232a7fac3ef71121c459352968802e546de0c80fb97541ca0678da7a4631425b05461e2c9265f2f763e79b9e2b544deb02ae063657ac8d3365421ce03f8e3cd2224dec828cf167ca2b6d6f0ae6caf53ce164e6507a994179910258daa07b4da6bdd053db944b7a68a93840dc6603d291f93e400245d351238fbaea8f5d96a1fe908a21a08ddc5603ea4b4f70df8a59e44453e063056ba918e40afc10cdf63e5f6ffc3ec797081d5b0ab8d2b3be5356aa5236179da37eca43cd55d861cfbff069b1a91b094a7a3ed2b34174b69be7b7b920a63c1be5877f56dfe24a5c949a2b6ef2a8e90e90c44945b108c745b20d39b7e1e3e3fa60725494ce6d8dce60748c8c7472f2519336fd169b73bfeccbc3cfb11db3fc5b0d5f21818a3fb539095e60f42e03b4e7a466266e000dc4004bb882c797f2931d86ecacf615b048984200b83748dd465f199e88a3b2bc387618102fea5952478ee15d4a7ecced95555e0218958db3fc37177c97a10963ceb85bc38350d4a51c0c3c4c50a963cc8416d65b9685c68b431106d621a43d3183f2496172"

#print(bcrypt.kdf(password="New World".encode('utf-8'), salt= bytes(1), rounds= 100, desired_key_bytes= 32).hex())

'''
sk = ecdsa.SigningKey.generate(curve= ecdsa.SECP256k1)
vk = sk.get_verifying_key()

print(sk.to_string().hex())
print(vk.to_string().hex())
'''

privateKey = "726e05ccf0fbbcde14674d64c749d04ca8e8ca68e91692468beedd466bb80a3f"    #"4254014fd2e94bb30c3b3ffea907bf51ab06fc56c5a170bab4f7c43a1aa048e2"

publicKey =  "9f44b86ad077235836ad5290cd9060f460818891341e9d3e1be97566e9e308f5f272af356544b9096d73e99b04f82da275b2c21562419f7732858311dddb3b18"  #"4f5d196638d00cb0c4c9b68a68edd3bad0247b855ecfb3bb171738f79078267760c6576dc2847185552e478064a4fbf65e14254e5ceb90e7113cfc7ae619063c"


privateKeyArray = ["726e05ccf0fbbcde14674d64c749d04ca8e8ca68e91692468beedd466bb80a3f",
                   "15d0dbf0ade8450b6d4b4e6820e66cfacd7eca446856dfc067c06bbdbbdbdb99",
                   "0d87e8dde27ae87831c94a1dfdd6b65981beda87ef5db93f31e91ef8a18bd91a",
                   "37c50d62bd37da5a739880001e0d64e4a4fbb6b9a5e3c24f85bd961f5cb7f6a8",
                   "58e293e450085d0b0c12facace2015b59418ccb0cf761eb762993f30749db0e4",
                   "726e05ccf0fbbcde14674d64c749d04ca8e8ca68e91692468beedd466bb80a3f"]

publicKeyArray = ["9f44b86ad077235836ad5290cd9060f460818891341e9d3e1be97566e9e308f5f272af356544b9096d73e99b04f82da275b2c21562419f7732858311dddb3b18",
                  "f2d6daeaeeaeb800ba6aa1b31f254c3cfbe315361c3bcbf24473e17a5939e4784a22245df2e41f5b8ebfad5f9c130a9093b57a26f82bf7546084c13957d51b78",
                  "a63dea0b64e597015f4bc9a30e8e0979b5a453618be0cfcc3e8b0bb6d9415c04705e745fc1b301df7f85ec8703af87a0b250da8afafdbc1273e05bc1db9deabd",
                  "e6486d0214719c4761972a912880afa162e5d045137069772f9995bbb9248b22badc35e87f5248f6c96140f25693c1e1abc558b88241235c315df5dd6633a90a",
                  "33d690c61929179f01f17ef0c1359f199e88dbb0964280324fb1b9d1a5ec9eeed12ad21161dbb12e11fe3dede4bfe0b7e9a9e8dd6d81f92ffeb2460712a564fc",
                  "9f44b86ad077235836ad5290cd9060f460818891341e9d3e1be97566e9e308f5f272af356544b9096d73e99b04f82da275b2c21562419f7732858311dddb3b18"



]

contentArray = [ "網站有中、英文版本，也有繁、簡體版，可通過每頁左上角的連結隨"  ,"@#%&^@#)RASODGJOASJ~!~!$+_~!$*","قعحبيبكزززززللث ٧٧٧٦٢صثمططططللللل فففب فقهههفاباا", "Testing new post message this is going to be over 140 chr;asdgulasidglasdiug;asdigua;sdiug;asidgu;asidgu;asidug;asidug;asdiug;sadiug;siudg;saidug;asudig;sadiug;saidgu;saudg;sdug;asdigu;asidgu;saidgu;sadigu;isadgu", "normal message", ""]


while True:
    rand = randint(1, 6)
    timeStamp = int(time.time())
    pubk = publicKeyArray[rand]


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

