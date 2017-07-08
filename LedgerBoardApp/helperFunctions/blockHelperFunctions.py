import hashlib
import time
import requests

import bcrypt
import operator

from LedgerBoardApp.models import Block
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Data
from LedgerBoardApp.models import Node

from LedgerBoardApp.helperFunctions import getHeight
from LedgerBoardApp.helperFunctions import postHelperFunctions
from LedgerBoardApp.helperFunctions import nodeHelperFunctions



import ast


import random

#need OrphanBlock procedures













def blockHandler(blockIndex, blockTimeStamp, previousBlockHash, blockTarget, blockNonce, newBlockStatus, miningStatus, orphanBlockFix, nonceRange):


    currentTime = int(time.time())

    if blockTimeStamp > currentTime:
        return "Block is from the future."

    if orphanBlockFix:
        previousBlock = Block.objects.get(index=(blockIndex -1))
    else:
        previousBlock = Block.objects.latest('index')

    amalgationA = str(previousBlock.index) + str(previousBlock.timeStamp) + str(previousBlock.timeStamp) + str(previousBlock.nonce)
    amalgationB = str(blockIndex) + str(blockTimeStamp) + str(previousBlockHash) + str(blockNonce)

    if amalgationA == amalgationB:
        return "Block already exists on chain."
    


    if previousBlock.blockHash != previousBlockHash:


        #replace this with time since good block

        print("previousBlockHash:   " + previousBlock.blockHash)
        print("so called prev hash:   " + previousBlockHash)



        badBlockHandler(False)




        return "Block does not fit on chain."
    


    if previousBlock.index >= blockIndex and (orphanBlockFix != True ):

        return "Block is old."
    
    if blockTarget != getTargetForBlock(blockIndex):
        return "Wrong target."



    unblockedPosts = Post.objects.filter(blockIndex=None, timeStamp__lt=(blockTimeStamp))
    unblockedPosts.order_by('timeStamp')









    postObjectArrayToBeSaved = []
    postObjectArrayToBeDeleted = []

    appendedPostHashesArray = []

    postNum = 0

    for post in unblockedPosts:


        if postNum > 1023:
            postObjectArrayToBeDeleted.append(post)

        elif post.timeStamp < Block.objects.latest('timeStamp').timeStamp:
            if newBlockStatus:
                postObjectArrayToBeDeleted.append(post)


        else:
            post.blockIndex = blockIndex
            appendedPostHashesArray.append(post.postHash)
            if newBlockStatus:
                postObjectArrayToBeSaved.append(post)

        postNum += 1









    blockHash = ''

    blockTotalContents = str(blockIndex) + str(blockTimeStamp) + str(previousBlockHash) + str(blockTarget)+ str(appendedPostHashesArray)
    blockPreHash = hashlib.sha256(blockTotalContents.encode('utf-8')).hexdigest()
    if miningStatus:
        nonce = nonceRange[1]
        while nonce >= nonceRange[0]:
            blockHash = bcrypt.kdf(password=bytes.fromhex(blockPreHash), salt= bytes(nonce), rounds= 100, desired_key_bytes= 32).hex()
            if metTarget(blockHash, blockTarget) and newBlockStatus:
                print('mined: ' + str(blockHash))
                blockNonce = nonce
                break
            #elif metTarget(blockHash, blockTarget):
            #    return str(blockNonce)

            nonce -= 1


        if nonce == (nonceRange[0] -1):
            return "Could not mine."



    else:
        blockHash = bcrypt.kdf(password=bytes.fromhex(blockPreHash), salt= bytes(blockNonce), rounds= 100, desired_key_bytes= 32).hex()


    if newBlockStatus and metTarget(blockHash, blockTarget):
        for post in postObjectArrayToBeSaved:
            post.save()
        for post in postObjectArrayToBeDeleted:
            post.delete()
        newBlock = Block(index=blockIndex, previousBlockHash=previousBlockHash, timeStamp=blockTimeStamp,
                         blockHash=blockHash, nonce=blockNonce, target=blockTarget)
        newBlock.save()

        badBlockHandler(True)
        print("added new block: " + str(blockHash))
        return ""
    else:
        badBlockHandler(False)

        return "Did not meet target."

def metTarget(blockHash, blockTarget):



    if int(blockHash, 16) <= int(blockTarget, 16):

        print('target met')

        return True
    else:

        return False


def getTargetForBlock(index):

    if index < 2016:
        return "0x446de077a113ac000000000000000000000000000000000000000000000000"

    indexRangeB = index - 1
    indexRangeA = index - 2016


    blocksToCheck = Block.objects.filter(index__lte = (indexRangeB), index__gte = (indexRangeA)).order_by('index')

    earliestBlock = blocksToCheck.earliest('index')
    latestBlock = blocksToCheck.latest('index')


    blocksToTargetChange = 0
    firstTarget = earliestBlock.target

    for block in blocksToCheck:
        if block.target == firstTarget:
            blocksToTargetChange += 1

    target = 1

    intRepLatestBlockTarget = int(latestBlock.target, 16)

    if blocksToTargetChange != 2016:
        target = intRepLatestBlockTarget
    else:

        timeBetweenAandB = latestBlock.timeStamp - earliestBlock.timeStamp
        print("time between a and b:  " + str(timeBetweenAandB))
        target = (timeBetweenAandB/1209600) * intRepLatestBlockTarget

        print(target)
        while (target / intRepLatestBlockTarget) > 4:
            target = target / 1.5

        target = int(round(target))





    return hex(target)




def badChainFixer(firstBadBlockTimeObject, startUp):
    rebuildStatus = Data.objects.get(datumTitle="Rebuilding")

    if rebuildStatus.datumContent == "True":

        return "error"
    else:
        rebuildStatus.datumContent = "True"
        rebuildStatus.save()

    # StartBadChainProcedures

    currentIndex = getHeight.getHeight()
    if startUp:
        currentIndex += 1

    postsOfLatestBlock = Post.objects.filter(blockIndex=int(currentIndex))


    for post in postsOfLatestBlock:
        post.blockIndex = None

        post.save()


    latestBlock = Block.objects.get(index=currentIndex)


    count = 0

    feedback = nodeHelperFunctions.getHighestNode(currentIndex)

    if feedback != '':
        rebuildStatus.datumContent = "False"

        rebuildStatus.save()
        return 'error'

    #sorted_nodeData = sorted(nodeData.items(), key=operator.itemgetter(0), reverse=True)

    highestNode = feedback[1]




    blockIndexRange = [currentIndex, highestNode['Height']]



    url = "http://" + highestNode['Host'] + "getBlocks/"



    payload = {'attribute' : 'index', 'attributeParameters' : str(blockIndexRange)}


    blockArray = []
    try:
        r = requests.get(url, timeout=0.1, payload=payload)


        blockArray = ast.literal_eval(str(r.content))
    except:

        rebuildStatus.datumContent = "False"

        rebuildStatus.save()
        print('error')
        return 'errror'

    orphanBlockFix = True

    for block in blockArray:
        latestBlock = Block.objects.latest('index')

        if orphanBlockFix:

            if block[0] != latestBlock.index:
                rebuildStatus.datumContent = "False"

                rebuildStatus.save()
                return 'error'

        url = "http://" + highestNode['Host'] + "getPosts/"

        postTimeStampRange = [latestBlock.timeStamp, block[1]]

        payload = {'attribute': 'timeStamp', 'attributeParameters': str(postTimeStampRange)}

        postArray = []
        try:
            r = requests.get(url, timeout=0.1, payload=payload)

            postArray = ast.literal_eval(str(r.content))

            if postArray.__len__() > 1023:
                rebuildStatus.datumContent = "False"

                rebuildStatus.save()
                return 'error'

            if orphanBlockFix:
                previousBlockTimeStamp =  Block.objects.get(index=(currentIndex -1)).timeStamp
            else:
                previousBlockTimeStamp =  Block.objects.get(index=(currentIndex)).timeStamp


            postsInTimeStampRange = Post.objects.filter(timeStamp__gte=previousBlockTimeStamp, timeStamp__lt=block[1])

            for post in postsInTimeStampRange:
                post.delete()

            for post in postArray:

                postFeedback = postHelperFunctions.newPost(post[0], post[1], post[2], post[3], True)

                if postFeedback[0] != ("" or "Exact post already exists."):
                    node = Node.objects.get(host=highestNode['Host'])

                    node.timeOfBlackList = time.time()
                    node.save()
                    rebuildStatus.datumContent = "False"

                    rebuildStatus.save()
                    return 'error'



            blockFeedback = blockHandler(block[0], block[1], block[2], block[3], block[4], True, False , orphanBlockFix)



            if blockFeedback[0] != '':
                rebuildStatus.datumContent = "False"

                rebuildStatus.save()
                return 'error'


            if orphanBlockFix == True:
                latestBlock.delete()
                orphanBlockFix = False

        except:
            rebuildStatus.datumContent = "False"

            rebuildStatus.save()
            print('error')
            return 'error'

    latestBlock.delete()


    firstBadBlockTimeObject.datumContent = 0
    firstBadBlockTimeObject.save()

    rebuildStatus.datumContent = "False"

    rebuildStatus.save()
    return ''

def badBlockHandler(chainableBlockOccured):
    firstbadBlockTime = 0



    firstBadBlockTimeObject = Data.objects.get(datumTitle="Time of First Bad Block After Chainable Block")
    if chainableBlockOccured:
        firstBadBlockTimeObject.datumContent = 0
        firstBadBlockTimeObject.save()
        return

    firstBadBlockTime = int(firstBadBlockTimeObject.datumContent)

    currentTime = time.time()

    if firstBadBlockTimeObject.datumContent == 0:
        firstBadBlockTimeObject.datumContent = int(time.time())
        return

    timeToStartBadChainProcedures = firstBadBlockTime + 2400 + random.randint(0, 2400)

    if currentTime - timeToStartBadChainProcedures > 0:

        badChainFixer(firstBadBlockTimeObject, False)


    else:

        firstBadBlockTimeObject.datumContent = timeToStartBadChainProcedures
        firstBadBlockTimeObject.save()

    return



