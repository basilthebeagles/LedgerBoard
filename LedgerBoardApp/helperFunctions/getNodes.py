from LedgerBoardApp.models import Node
import random
import requests

def getNodes():

    nodeArray = []
    try:

        nodes = Node.objects.all()

        for node in nodes:
            nodeDataArray = []
            nodeDataArray.append(node.host)
            nodeDataArray.append(node.version)
            nodeDataArray.append(node.secondsSinceLastInteraction)
            nodeArray.append(nodeDataArray)


        random.shuffle(nodeArray)

        return ("", nodeArray)


    except:
        return ("No nodes.", [])


