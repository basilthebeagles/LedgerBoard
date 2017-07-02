import hashlib
import time
import requests

import bcrypt
import operator

from LedgerBoardApp.models import Block
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Data
from LedgerBoardApp.helperFunctions import getNodes


import random

#need OrphanBlock procedures













def blockHandler(blockIndex, blockTimeStamp, previousBlockHash, blockTarget, blockNonce, newBlockStatus, miningStatus):


    currentTime = int(time.time())

    if blockTimeStamp > currentTime:
        return "Block is from the future."

    previousBlock = Block.objects.latest('index')

    amalgationA = str(previousBlock.index) + str(previousBlock.timeStamp) + str(previousBlock.timeStamp) + str(previousBlock.nonce)
    amalgationB = str(blockIndex) + str(blockTimeStamp) + str(previousBlockHash) + str(blockNonce)

    if amalgationA == amalgationB:
        return "Block already exists on chain."
    


    if previousBlock.blockHash != previousBlockHash:


        #replace this with time since good block






        return "Block does not fit on chain."



    if previousBlock.index >= blockIndex:

        return "Block is old."

    if blockTarget != getTargetForBlock(blockIndex):
        return "Wrong target."

    '''earliestPost = sortedPostTupleArray[0]
    latestPost = sortedPostTupleArray[-1]

    if earliestPost[1] < previousBlock.timeStamp:

        return "Includes previous posts."

    if latestPost[1] >= timeStamp:

        return "Includes later posts."
    '''
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
        nonce = 16
        while nonce != 0:
            blockHash = bcrypt.kdf(password=bytes.fromhex(blockPreHash), salt= bytes(nonce), rounds= 100, desired_key_bytes= 512).hex()
            if metTarget(blockHash, blockTarget) and newBlockStatus:

                blockNonce = nonce
                break
            elif metTarget(blockHash, blockTarget):
                return str(blockNonce)

            nonce -= 1


        if nonce == 0:
            return "Could not mine."



    else:
        blockHash = bcrypt.kdf(password=bytes.fromhex(blockPreHash), salt= bytes(blockNonce), rounds= 100, desired_key_bytes= 512).hex()


    if newBlockStatus and metTarget(blockHash, blockTarget):
        for post in postObjectArrayToBeSaved:
            post.save()
        for post in postObjectArrayToBeDeleted:
            post.delete()
        newBlock = Block(index=blockIndex, previousBlockHash=previousBlockHash, timeStamp=blockTimeStamp,
                         blockHash=blockHash, nonce=blockNonce, target=blockTarget)
        newBlock.save()

        badBlockHandler(True)
        #set unchainable thing to zero

        return ""
    else:
        return "Did not meet target."

def metTarget(blockHash, blockTarget):
    if int(blockHash, 16) < blockTarget:



        return True
    else:

        return False


def getTargetForBlock(index):
    indexRangeB = index - 1
    indexRangeA = index - 2016


    blocksToCheck = Block.objects.filter(timeStamp__lte = (indexRangeB), timeStamp__gte = (indexRangeA)).order_by('index')

    earliestBlock = blocksToCheck.earliest('index')
    latestBlock = blocksToCheck.latest('index')


    blocksToTargetChange = 0
    firstTarget = earliestBlock.target

    for block in blocksToCheck:
        if block.target == firstTarget:
            blocksToTargetChange += 1

    target = 1



    if blocksToTargetChange != 2016:
        target = int(latestBlock.target)
    else:

        timeBetweenAandB = latestBlock.timeStamp - earliestBlock.timeStamp

        target = (1209600/timeBetweenAandB) * latestBlock.target
    return target




def badChainFixer():

    nodes = getNodes.getNodes()

    counter = 0

    nodeData = {}


    for node in nodes:


        url = "http://" + node.host + "getHeight/"

        r = requests.get(url, timeout = 0.1)

        height = r.content

        nodeData[node.host] = height


        counter += 1

        if counter == 20:
            break

    sorted_nodeData = sorted(nodeData.items(), key=operator.itemgetter(0), reverse=True)




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

        #StartBadChainProcedures

    else:

        firstBadBlockTimeObject.datumContent = timeToStartBadChainProcedures
        firstBadBlockTimeObject.save()

    return



