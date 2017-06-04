import bcrypt
import hashlib



print(hex(327650872364957283694857923478659287345))

string = 'test'

testStringEncode = string.encode('utf-8')

#test = bcrypt.kdf(password=testStringEncode, salt= bytes(124124), rounds= 100, desired_key_bytes= 256).hex()





for i in range(100000000):
    print(hashlib.sha256(bytes(76576494 + i)).hexdigest())
