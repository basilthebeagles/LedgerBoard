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
from LedgerBoardApp.helperFunctions import nodeHelperFunctions
from LedgerBoardApp.helperFunctions import addNewHosts

from LedgerBoardApp.models import Node
#call this something else




def StartUp(selfHost):



    savedNodes = Node.objects.all()
    for node in savedNodes:
        url = "http://" + node.host + "/getBlocks/"
        try:
            r = requests.post(url=url, timeout=1)
        except:
            node.delete()

    savedNodes.update()
    print('now1')
    if savedNodes.__len__() == 0:
        feedback = addNewHosts.AddNewHosts("127.0.0.1:4847", 0.1, selfHost)
        print("USING DEFAULT NODE")
        if feedback != "we are already on other hosts list. But we have now added that host." or feedback != "":
            return feedback

    print('now2')

    feedback = "-"
    firstBadBlockTimeObject = Data.objects.get(datumTitle="Time of First Bad Block After Chainable Block")

    if int(getHeight.GetHeight()[1]) == 0:
        print('at 0 index')

        currentTime = int(time.time())
        postsToDelete = Post.objects.filter(timeStamp__lte=currentTime)
        for post in postsToDelete:
            post.delete()
        print('now3')
        feedback = nodeHelperFunctions.getHighestNode(0)

        if feedback[0] != '':


            return feedback[0]
        print('now4')


        # sorted_nodeData = sorted(nodeData.items(), key=operator.itemgetter(0), reverse=True)

        highestNode = feedback[1]
        print(highestNode['Host'])

        blockIndexRange = [1, 1]

        url = "http://" + highestNode['Host'] + "/getBlocks/"

        payload = {'attribute': 'index', 'attributeParameters': str(blockIndexRange)}

        blockArray = []

        r = requests.post(url=url, timeout=1, data=payload)

        blockArray = ast.literal_eval(str(r.text))

        print('now5')

        #print('could not get blockArray from highest node')


        for block in blockArray:

            url = "http://" + highestNode['Host'] + "/getPosts/"
            previousBlockTimeStamp = Block.objects.get(index=0).timeStamp

            postTimeStampRange = [previousBlockTimeStamp, (block[1] - 1)]

            payload = {'attribute': 'timeStamp', 'attributeParameters': str(postTimeStampRange)}

            postArray = []
            try:
                r = requests.post(url, timeout=1, data=payload)
            except:
                return "could not get posts"
            postArray = ast.literal_eval(str(r.text))

            if postArray.__len__() > 1023:


                return  'too many posts in block'

            postsInTimeStampRange = Post.objects.filter(timeStamp__gte=previousBlockTimeStamp,
                                                            timeStamp__lt=block[1])

            for post in postsInTimeStampRange:
                post.delete()

            for post in postArray:
                print(postArray)
                print(post)
                postFeedback = postHelperFunctions.NewPost(post[0], post[1], post[2], post[3], True)

                if postFeedback != ("" or "Exact post already exists."):
                    node = Node.objects.get(host=highestNode['Host'])

                    node.timeOfBlackList = time.time()
                    node.save()


                    return "Post error: " + postFeedback

            blockFeedback = blockHelperFunctions.blockHandler(block[0], block[1], block[2], block[3], block[4], True, False, False,
                                             [0, 0])

            if blockFeedback != '':


                return "Block error: " + blockFeedback






    count = 0
    feedback = '-'
    while feedback != "" and count < 20:
            print("in while loop")
            feedback = blockHelperFunctions.badChainFixer(firstBadBlockTimeObject)
            print(feedback)
            count += 1

    if count >= 18:
        return feedback

    return ""