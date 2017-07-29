from django.core.management.base import BaseCommand, CommandError

from LedgerBoardApp.models import Data
from LedgerBoardApp.helperFunctions import getHeight
import time
import requests
import socket

from LedgerBoardApp.models import Block
from LedgerBoardApp.models import Post

from LedgerBoardApp.helperFunctions import postHelperFunctions
from LedgerBoardApp.helperFunctions import blockHelperFunctions


import ast

from LedgerBoardApp.helperFunctions import nodeHelperFunctions
from LedgerBoardApp.helperFunctions import addNewHosts

from LedgerBoardApp.models import Node




#this should be called whenever the node starts up. This is because it ensures that the node is up to date.
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('selfHost', nargs='+', type=str)

    def handle(self, *args, **options):




        selfHost = ""

        for host in options['selfHost']:

                selfHost = host



        savedNodes = Node.objects.all()
        for node in savedNodes:
            url = "http://" + node.host + "/getBlocks/"
            try:
                r = requests.post(url=url, timeout=1)
            except:
                node.delete()

        savedNodes.update()
        if savedNodes.__len__() == 0:
            try:
                ip = socket.gethostbyname("ledgerboard.f-stack.com")
                host = str(ip) + ":4848"
                feedback = addNewHosts.AddNewHosts(host, 0.1, selfHost)
            except:
                return "connecting to default node failed."
            print("USING DEFAULT NODE")
            if feedback != "we are already on other hosts list. But we have now added that host." and feedback != "":
                return (feedback)


        feedback = "-"
        firstBadBlockTimeObject = Data.objects.get(datumTitle="Time of First Bad Block After Chainable Block")

        if int(getHeight.GetHeight()[1]) == 0:
            print('at 0 index')

            currentTime = int(time.time())
            postsToDelete = Post.objects.filter(timeStamp__lte=currentTime)
            for post in postsToDelete:
                post.delete()
            feedback = nodeHelperFunctions.getHighestNode(0)

            if feedback[0] != '':
                return feedback[0]

            # sorted_nodeData = sorted(nodeData.items(), key=operator.itemgetter(0), reverse=True)

            highestNode = feedback[1]

            blockIndexRange = [1, highestNode['Height']]

            url = "http://" + highestNode['Host'] + "/getBlocks/"

            payload = {'attribute': 'index', 'attributeParameters': str(blockIndexRange)}

            blockArray = []
            try:
                r = requests.post(url, timeout=0.5, data=payload)

                blockArray = ast.literal_eval(str(r.text))
            except:

                return 'could not get blockArray from highest node'

            count = 0
            for block in blockArray:

                if (count % 2 != 0):
                    count += 1
                    continue

                currentIndex = int(getHeight.GetHeight()[1])

                if block[0] != currentIndex + 1:
                    nodeHelperFunctions.blackList(highestNode['Host'])
                    return 'blockArray is not sorted'
                print(block)
                blockFeedback = blockHelperFunctions.blockHandler(block[0], block[1], block[2], block[3], block[4],
                                                                  str(blockArray[count + 1]), True,
                                                                  False, True, [0, 0])

                if blockFeedback != "":
                    nodeHelperFunctions.blackList(highestNode['Host'])

                    return "invalid blocks given"

                count = count + 1

            currentTime = int(time.time())

            url = "http://" + highestNode['Host'] + "/getPosts/"

            currentIndex = int(getHeight.GetHeight()[1])

            latestBlock = Block.objects.get(index=currentIndex)

            payload = {'attribute': 'timeStamp', 'attributeParameters': str([latestBlock.timeStamp, currentTime])}

            postArray = []

            try:
                r = requests.post(url, timeout=0.5, data=payload)

                postArray = ast.literal_eval(str(r.text))
            except:


                return 'could not get postArray from highest node'

            for post in postArray:
                feedback = postHelperFunctions.NewPost(publicKey=post[0], timeStamp=post[1], content=post[2],
                                                       signature=post[3], notNewToNetwork=True)


            return "successful start up"

        count = 0




        feedback = blockHelperFunctions.badChainFixer(firstBadBlockTimeObject)
        print("feedback: " + feedback)





        return "success"