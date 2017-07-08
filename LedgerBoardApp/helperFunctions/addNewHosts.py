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
            'host': host,
            'vers': version,
            'currentTime': str(currentTime),
            'programName': "LedgerBoard",

        }
        print('here')
        r = requests.post(url, data=payload, timeout=5)
        if r.content == "Connection created.":

            feedback = NewNode(host, version)
            if feedback == "":
                return ''
            else:
                return 'fail'
        else:
            return r.content
    except:
        return 'fail'

