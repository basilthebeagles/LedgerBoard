#! /usr/bin/env python

import ecdsa
import time
import hashlib

import requests
import sys
import socket
from datetime import datetime, timezone



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



        reSign = False

        while True:



            host = input("\nEnter the host (ip + port eg 127.0.0.1:4848) of the node you would like to initially broadcast to; enter default to use a default one: ")

            if host == "default":
                ip = socket.gethostbyname("ledgerboard.f-stack.com")
                host = str(ip) + ":4848"



            url = "\nhttp://" + str(host) + "/newPost/"


            timeStamp = int(time.time())

            totalPostContent = publicKey + str(timeStamp) + content
            postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()
            signature = sk.sign(bytes.fromhex(postHash)).hex()

            timeAndDate = datetime.fromtimestamp(timeStamp, timezone.utc)

            ts = timeAndDate.strftime('%H:%M:%S %d/%m/%Y')

            print("\nPost hash: " + str(postHash))

            print("\nUse the above to identify your post if you search for it.")

            print("\nSignature: " + str(signature))

            payload = {

                'pubk': str(publicKey),
                'ts': str(timeStamp),
                'content': str(content),
                'sig': str(signature),
                'originHost': str("127.0.0.1:9999")

            }





            try:
                print("\nBroadcasting to : " + str(url))
                r = requests.post(url, data=payload, timeout=10)

                if r.text == "Success.":
                    print("\nPost has been successfully broadcasted to node")
                    print("\nPosted at: " + str(ts))

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

