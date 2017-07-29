import ecdsa
import time
import hashlib

import requests
import sys



while True:

    choice = input("\nChoose from the following:\n[1] Generate key pair \n[2] Sign and send message\n[3] Exit ")

    if choice == '1':
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()

        print("Your private key is: " + sk.to_string().hex())
        print("\nYour public key is: " + vk.to_string().hex())
        print("\nKeep your private key safe.")
    elif choice == '2':




        privateKey = input("\nEnter your private key: ")
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(privateKey), curve=ecdsa.SECP256k1)



        vk = sk.get_verifying_key()

        publicKey = str(vk.to_string().hex())

        content = input("\nEnter the content of your post: ")

        timeStamp = int(time.time())



        totalPostContent = publicKey + str(timeStamp) + content
        postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()
        signature = sk.sign(bytes.fromhex(postHash)).hex()






        payload = {

            'pubk':str(publicKey),
            'ts':str(timeStamp),
            'content':str(content),
            'sig':str(signature),
            'originHost': str("127.0.0.1:9999")

        }



        while True:

            host = input("\nEnter the host (ip + port eg 127.0.0.1:4848) of the node you would like to initially broadcast to; enter default to use a default one: ")

            if host == "default":
                host = "127.0.0.1:4847"


            url = "\nhttp://" + str(host) + "/newPost/"
            try:
                print("Broadcasting to: " + str(url))
                r = requests.post(url, data=payload, timeout=1)

                if r.text == "Success.":
                    print("\nPost has been successfully broadcasted to node")
                    break
                print("\nError: " + r.text)

            except:
                print("\nCould not connect")


            choice = input("\nSomething went wrong. Do you wish to: \n\n[1] Choose another host \n[2] Modify your post \n[3] Exit ")


            if choice == '2':
                break
            elif choice == '3':
                sys.exit()
    else:
        sys.exit()