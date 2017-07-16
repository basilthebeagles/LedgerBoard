from django.db import models
import time
import requests
from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions.nodeHelperFunctions import NewNode

def AddNewHosts(host, version, selfHost):
    currentTime = int(time.time())

    try:

        url = "http://" + str(host) + "/handShake/"
        print(url)
        payload = {

            'vers': 0.1,
            'currentTime': str(currentTime),
            'programName': "LedgerBoard",

        }
        print(payload)
        print('here')
        headers = {'HTTP_HOST' : selfHost}
        try:
            r = requests.post(url, data=payload, timeout=5, headers=headers)
        except requests.exceptions.Timeout:
            return "could not connect"
    except:
        return 'could not connect'



    if str(r.text) == "Connection created." or "Host already exists.":
        print('here1')
        feedback = NewNode(host, version)
        if feedback == "":
            return ''
        elif feedback == "" and str(r.text) == "Host already exists.":
            return "we are already on other hosts list. But we have now added that host."
        else:
            return "Other host has added us to their list but for us: "  + feedback
    else:
        return "response: " + str(r.content)


