from django.db import models
import time

from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions import blockHelperFunctions
from LedgerBoardApp.models import Data
from LedgerBoardApp.helperFunctions import getHeight
import hashlib
import time
import requests

import bcrypt
import operator

from LedgerBoardApp.models import Block
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Node

from LedgerBoardApp.helperFunctions import postHelperFunctions
from LedgerBoardApp.helperFunctions import nodeHelperFunctions
from LedgerBoardApp.helperFunctions import blockHelperFunctions




import ast


import random

#call this something else




def StartUp():

    feedback = "-"
    firstBadBlockTimeObject = Data.objects.get(datumTitle="Time of First Bad Block After Chainable Block")

    if int(getHeight.GetHeight()[1]) == 0:
        currentTime = int(time.time())
        postsToDelete = Post.objects.filter(timeStamp__lte=currentTime)
        for post in postsToDelete:
            post.delete()

        feedback = nodeHelperFunctions.getHighestNode(0)

        if feedback[0] != '':

            print( 'could not get highest node')
            return


        # sorted_nodeData = sorted(nodeData.items(), key=operator.itemgetter(0), reverse=True)

        highestNode = feedback[1]
        print(highestNode['Host'])

        blockIndexRange = [1, 1]

        url = "http://" + highestNode['Host'] + "/getBlocks/"

        payload = {'attribute': 'index', 'attributeParameters': str(blockIndexRange)}

        blockArray = []

        r = requests.post(url=url, timeout=1, data=payload)

        blockArray = ast.literal_eval(str(r.text))


        print('could not get blockArray from highest node')
        return

        for block in blockArray:

            url = "http://" + highestNode['Host'] + "getPosts/"
            previousBlockTimeStamp = Block.objects.get(index=0).timeStamp

            postTimeStampRange = [previousBlockTimeStamp, (block[1] - 1)]

            payload = {'attribute': 'timeStamp', 'attributeParameters': str(postTimeStampRange)}

            postArray = []
            r = requests.get(url, timeout=1, payload=payload)

            postArray = ast.literal_eval(str(r.content))

            if postArray.__len__() > 1023:

                print ('too many posts in block')
                return

            postsInTimeStampRange = Post.objects.filter(timeStamp__gte=previousBlockTimeStamp,
                                                            timeStamp__lt=block[1])

            for post in postsInTimeStampRange:
                post.delete()

            for post in postArray:

                postFeedback = postHelperFunctions.newPost(post[0], post[1], post[2], post[3], True)

                if postFeedback[0] != ("" or "Exact post already exists."):
                    node = Node.objects.get(host=highestNode['Host'])

                    node.timeOfBlackList = time.time()
                    node.save()

                    print( "Post error: " + postFeedback[0])
                    return

            blockFeedback = blockHelperFunctions.blockHandler(block[0], block[1], block[2], block[3], block[4], True, False, False,
                                             [0, 0])

            if blockFeedback[0] != '':

                print( "Block error: " + blockFeedback[0])
                return








    while feedback != "":

            feedback = blockHelperFunctions.badChainFixer(firstBadBlockTimeObject)
            print(feedback)

