
import requests
from LedgerBoardApp.models import Node
import time



#distributes a new post or block to all known nodes

def distributeEntity(dataArray, type, originHost, selfHost):

    urlAddition = ""
    payload = {}
    if type == "block":


        urlAddition = "/newBlock/"
        payload = {
            'index':str(dataArray[0]),
            'ts':str(dataArray[1]),
            'prevBlockHash': str(dataArray[2]),
            'target':str(dataArray[3]),
            'nonce':str(dataArray[4]),
            'postArray': str(dataArray[5]),
            'originHost': str(selfHost)
        }
    elif type == "post":
        urlAddition = "/newPost/"

        payload = {

            'pubk':str(dataArray[0]),
            'ts':str(dataArray[1]),
            'content':str(dataArray[2]),
            'sig':str(dataArray[3]),
            'originHost': str(selfHost)

        }

    '''if originHost != 'self':
        nodes = Node.objects.exclude(host=originHost)
    else:'''
    nodes = Node.objects.all()

    feedbackDictionary = {}

    if nodes.__len__() == 0:
        print('no nodes')

    for node in nodes:

        if node.timeOfBlackList != 0:
            print('blacklisted')
            continue

        if node.host == originHost:
            continue

        currentTime = int(time.time())

        url = "http://" + str(node.host) + urlAddition
        try:
            print("distributing to:" + str(url))
            r = requests.post(url, data=payload, timeout=4)
            feedbackDictionary[str(node.host)] = r.content
            node.secondsSinceLastInteraction = currentTime
            node.save()

        except:

            if node.secondsSinceLastInteraction < currentTime - 5400:
                node.delete()


            feedbackDictionary[str(node.host)] = "Node took too long."


    return feedbackDictionary
