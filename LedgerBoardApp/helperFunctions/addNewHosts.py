from django.db import models
import time
import requests
from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions.nodeHelperFunctions import NewNode

def addNewHosts(host, version):
    currentTime = int(time.time())

    try:

        url = str(host) + "/handShake/"
        payload = {
            'host': host,
            'vers': version,
            'currentTime': str(currentTime),

        }

        r = requests.post(url, data=payload, timeout=1)
        if r.content == "Connection created.":

            feedback = NewNode(host, version)
            if feedback == "":
                return ''
            else:
                return 'fail'
        else:
            return 'fail'
    except:
        return 'fail'

