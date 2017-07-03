from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions import getNodes
import requests



def newNode(host, version):
    feedback = ""

    if Node.objects.filter(host = host).exists():
        feedback = "Host already exists."

        return feedback #basically say it exist already

    node = Node(host = host, version=version, secondsSinceLastInteraction=0)
    node.save()
    return feedback

def getHighestNode(currentIndex):

    nodes = getNodes()




    counter = 0

    highestNode = {"Host": '', 'Height': 0}

    for node in nodes:
        if node.timeOfBlackList != 0:
            continue
        host = node.host

        url = "http://" + host + "getHeight/"
        try:
            r = requests.get(url, timeout=0.1)

            height = r.content

            if height > highestNode['Height']:
                highestNode['Host'] = host
                highestNode['Height'] = int(height)
        except:
            print('error')

        counter += 1



    if highestNode['Height'] < currentIndex:
        return "No nodes with height above or equal to current index.", highestNode

    return "", highestNode

