from LedgerBoardApp.models import Node
import random
import time

#returns all the node's known nodes.

def GetNodes():

    nodeArray = []
    try:

        nodes = Node.objects.all()

        currentTime = int(time.time())

        for node in nodes:

            if int(node.secondsSinceLastInteraction) < int(currentTime - 5400):
                node.delete()


            nodeDataArray = []
            nodeDataArray.append(node.host)
            nodeDataArray.append(node.version)
            nodeDataArray.append(node.secondsSinceLastInteraction)
            nodeArray.append(nodeDataArray)


        random.shuffle(nodeArray)

        return ("", nodeArray)


    except:
        return ("No nodes.", [])


