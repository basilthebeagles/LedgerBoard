
import requests
from LedgerBoardApp.models import Node




def distributeEntity(dataArray, type):

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
        }
    elif type == "post":
        urlAddition = "/newPost/"

        payload = {

            'pubk':str(dataArray[0]),
            'ts':str(dataArray[1]),
            'content':str(dataArray[2]),
            'sig':str(dataArray[3]),


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

        url = str(node.host) + urlAddition
        try:
            r = requests.post(url, data=payload, timeout=1)
            feedbackDictionary[str(node.host)] = r.content
            node.secondsSinceLastInteraction = 0

        except:
            print("took too long or bad connection")
            feedbackDictionary[str(node.host)] = "Node took too long."


    return feedbackDictionary
