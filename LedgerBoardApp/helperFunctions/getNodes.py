from LedgerBoardApp.models import Node
import random

#returns all the node's known nodes.

def GetNodes():

    nodeArray = []
    try:

        nodes = Node.objects.all()



        for node in nodes:

            if node.secondsSinceLastInteraction > 5400:
                node.delete()
            elif node.timeOfBlackList != 0:
                continue

            nodeDataArray = []
            nodeDataArray.append(node.host)
            nodeDataArray.append(node.version)
            nodeDataArray.append(node.secondsSinceLastInteraction)
            nodeArray.append(nodeDataArray)


        random.shuffle(nodeArray)

        return ("", nodeArray)


    except:
        return ("No nodes.", [])


