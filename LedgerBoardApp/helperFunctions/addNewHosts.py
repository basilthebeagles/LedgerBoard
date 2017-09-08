import time
import requests
import ast
from LedgerBoardApp.helperFunctions.nodeHelperFunctions import NewNode

def AddNewHosts(host, version, selfHost):
    currentTime = int(time.time())

    if host == selfHost:
        return "CAnnot add self."

    try:

        url = "http://" + str(host) + "/handShake/"
        print("connecting to " + str(url))
        payload = {

            'vers': 0.1,
            'currentTime': str(currentTime),
            'programName': "LedgerBoard",
            'host': selfHost

        }


        try:
            r = requests.post(url, data=payload, timeout=40)
        except requests.exceptions.Timeout:
            return "could not connect"
    except:
        return 'could not connect'



    if str(r.text) == "Connection created." or "Host already exists.":
        feedback = NewNode(host, version)
        print("new node feedback: " + feedback)
        if feedback == "":
            GetNewHosts(host, selfHost)#get new nodes from the node we have just added
            return ""
        elif feedback == "" and str(r.text) == "Host already exists.":
            GetNewHosts(host, selfHost)

            return "we are already on other hosts list. But we have now added that host to our list."

        else:
            return "Other host has added us to their list but for us: "  + feedback
    else:
        return "response: " + str(r.content)


def GetNewHosts(host, selfHost):

    url = "http://" + str(host) + "/getNodes/"
    print(url)

    print('here')

    try:
        r = requests.post(url, timeout=2)
        print(r.text)
        nodeArray = ast.literal_eval(str(r.text))

        for node in nodeArray: #handshake with list of nodes recieved

            if node[0] == selfHost:
                continue

            feedback = AddNewHosts(node[0], node[1], selfHost )
            print(feedback)


    except:
        print("get new hosts failed.")





    return
