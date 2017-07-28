from django.db import models
import time
import requests
import ast
from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions.nodeHelperFunctions import NewNode

def AddNewHosts(host, version, selfHost):
    currentTime = int(time.time())

    if host == selfHost:
        return "CAnnot add self."

    try:

        url = "http://" + str(host) + "/handShake/"
        print(url)
        payload = {

            'vers': 0.1,
            'currentTime': str(currentTime),
            'programName': "LedgerBoard",
            'host': selfHost

        }
        print(payload)
        print('here')

        try:
            r = requests.post(url, data=payload, timeout=5)
        except requests.exceptions.Timeout:
            return "could not connect"
    except:
        return 'could not connect'



    if str(r.text) == "Connection created." or "Host already exists.":
        print('here1')
        feedback = NewNode(host, version)
        if feedback == "":
            GetNewHosts(host, selfHost)
            return ''
        elif feedback == "" and str(r.text) == "Host already exists.":
            GetNewHosts(host, selfHost)

            return "we are already on other hosts list. But we have now added that host."

        else:
            return "Other host has added us to their list but for us: "  + feedback
    else:
        return "response: " + str(r.content)


def GetNewHosts(host, selfHost):

    url = "http://" + str(host) + "/getNodes/"
    print(url)

    print('here')

    try:
        r = requests.post(url, timeout=5)
        print(r.text)
        nodeArray = ast.literal_eval(str(r.text))

        for node in nodeArray:
            feedback = AddNewHosts(node[0], node[1], selfHost )
            print(feedback)


    except:
        print("get new hosts failed.")





    return
