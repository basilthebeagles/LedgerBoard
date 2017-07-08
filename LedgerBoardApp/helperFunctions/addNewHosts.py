from django.db import models
import time
import requests
from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions.nodeHelperFunctions import NewNode

def AddNewHosts(host, version):
    currentTime = int(time.time())

    try:

        url = "http://" + str(host) + "/handShake/"
        print(url)
        payload = {

            'vers': version,
            'currentTime': str(currentTime),
            'programName': "LedgerBoard",

        }
        print(payload)
        print('here')
        r = requests.post(url, data=payload, timeout=5)
    except:
        return 'could not connect'

    if r.content == bytes("Connection created."):
        print('here1')
        feedback = NewNode(host, version)
        if feedback == "":
            return ''
        else:
            return 'fail'
    else:
        return "response: " + str(r.content)


