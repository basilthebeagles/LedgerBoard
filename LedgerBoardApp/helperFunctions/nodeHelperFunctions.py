from LedgerBoardApp.models import Node
import requests
import time



def NewNode(host, version):
    feedback = ""

    if Node.objects.filter(host = host).exists():
        feedback = "Host already exists."

        return feedback #basically say it exist already
    currentTime = int(time.time())

    node = Node(host = host, version=version, secondsSinceLastInteraction=currentTime, timeOfBlackList=0)
    node.save()
    return feedback

def getHighestNode(currentIndex):

    nodes = Node.objects.all()

    print(nodes)


    counter = 0

    highestNode = {"Host": '', 'Height': 0}

    for node in nodes:


        host = node.host

        url = "http://" + host + "/getHeight/"
        try:
            r = requests.get(url, timeout=10)

            height = int(r.text)
            print('height: ' + str(height))

            if height >= highestNode['Height']:
                highestNode['Host'] = host
                highestNode['Height'] = int(height)
        except:

            print('connection to node failed')

        counter += 1



    if highestNode['Height'] < currentIndex:
        return "No nodes with height above or equal to current index.", highestNode
    if highestNode['Host'] == '':
        return "Could not find nodes", highestNode
    if int(highestNode['Height']) == currentIndex:
        return "could not find node higher than current index", highestNode
    return "", highestNode

def blackList(host):

    currentTime = int(time.time())

    node = Node.objects.get(host=host)

    node.timeOfBlackList = currentTime
    node.save()