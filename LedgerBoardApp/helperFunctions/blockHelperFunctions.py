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













def blockHandler(blockIndex, blockTimeStamp, previousBlockHash, blockTarget, blockNonce, intendedPostsForBlockStr, newBlockStatus, miningStatus, orphanBlockStatus, nonceRange):


    currentTime = int(time.time())

    intendedPostsForBlock = ast.literal_eval(str(intendedPostsForBlockStr))


    if blockTimeStamp > currentTime and newBlockStatus == True:
        print("newblock error: Block is from the future." )
        return "Block is from the future."


    if len(intendedPostsForBlock) > 1023:
        return "Too many posts given."


    if newBlockStatus != True:
        previousBlock = Block.objects.filter(index=blockIndex)
    else:
        previousBlock = Block.objects.latest('index')



    amalgationA = str(previousBlock.index) + str(previousBlock.timeStamp) + str(previousBlock.timeStamp) + str(previousBlock.nonce)
    amalgationB = str(blockIndex) + str(blockTimeStamp) + str(previousBlockHash) + str(blockNonce)

    if newBlockStatus == True and amalgationA == amalgationB:
        print("newblock error: Block already exists on chain." )

        return "Block already exists on chain."



    if previousBlock.blockHash != previousBlockHash:


        #replace this with time since good block

        print("previousBlockHash:   " + previousBlock.blockHash)
        print("so called prev hash:   " + previousBlockHash)


        if newBlockStatus:

            badBlockHandler(False)

        print("newblock error: Block does not fit on chain.")


        return "Block does not fit on chain."
    


    if previousBlock.index >= blockIndex and newBlockStatus != True:
        print("newblock error: block is old")

        return "Block is old."
    
    if blockTarget != getTargetForBlock(blockIndex):
        print("newblock error: wrong target")

        return "Wrong target."








    appendedPostHashesArray = []



    amountOfPostsThatAlreadyExist = 0
    previousPostTimeStamp = 0

    for post in intendedPostsForBlock:
        if post[1] < previousPostTimeStamp:
            return "Posts given are not in order."
        else:
            previousPostTimeStamp = post[1]



        if (post[1] >= blockTimeStamp):
            return "Posts given contain posts that are out of their blocks domain."


        if post[1] < previousBlock.timeStamp:
            return "Posts given contain posts that are too old."





        feedback = postHelperFunctions.verifyPost(publicKey=post[0], timeStamp=post[1], content=post[2], signature=post[3])

        if feedback[0] == "Exact post already exists.":

            amountOfPostsThatAlreadyExist += 1

            appendedPostHashesArray.append(feedback[1])

        elif feedback[0] != "":
            return "Posts given contain invalid posts"
        else:

            if newBlockStatus != True:
                return "Posts given contain posts that are not part of block."

            appendedPostHashesArray.append(feedback[1])


    if orphanBlockStatus != True:
        intendedPostsForBlockLength = len(intendedPostsForBlock)
        if intendedPostsForBlockLength != 0:
            if newBlockStatus and ((amountOfPostsThatAlreadyExist / intendedPostsForBlockLength) < 0.51):
                return "Posts given do not match up enough with node's posts."







    blockHash = ''

    blockTotalContents = str(blockIndex) + str(blockTimeStamp) + str(previousBlockHash) + str(blockTarget)+ str(appendedPostHashesArray)
    blockPreHash = hashlib.sha256(blockTotalContents.encode('utf-8')).hexdigest()
    if miningStatus:
        nonce = nonceRange[0]
        while nonce <= nonceRange[1]:
            checkBlock = Block.objects.latest('index')
            if checkBlock.index == blockIndex:
                return "new valid block recieved whilst mining"

            blockHash = bcrypt.kdf(password=bytes.fromhex(blockPreHash), salt= bytes(nonce), rounds= 100, desired_key_bytes= 32).hex()
            if metTarget(blockHash, blockTarget) and newBlockStatus:
                print('mined: ' + str(blockHash))
                blockNonce = nonce
                break
            #elif metTarget(blockHash, blockTarget):
            #    return str(blockNonce)

            nonce += 1


        if nonce == (nonceRange[1] +1):
            return "Could not mine."



    else:
        blockHash = bcrypt.kdf(password=bytes.fromhex(blockPreHash), salt= bytes(blockNonce), rounds= 100, desired_key_bytes= 32).hex()



    if newBlockStatus != True:
        return "Block is valid."

    if metTarget(blockHash, blockTarget):

        if newBlockStatus != True and blockHash == Block.objects.get(blockIndex = blockIndex).blockHash:
            return "Block verified."

        else:
            return "Hashs do not match up."



        count = 0
        for post in intendedPostsForBlock:

            if postsForBlock.get(postHash=appendedPostHashesArray[count] ).exists():
                tempPost = Post.objects.get(postHash=appendedPostHashesArray[count])
                tempPost.blockIndex = blockIndex
                tempPost.save()

                continue
            else:
                newPost = Post(publicKeyOfSender=post[0], timeStamp=post[1], content=post[2], signature=post[3], postHash=appendedPostHashesArray[count], blockIndex=blockIndex)
                newPost.save()
            count += 1

        postsToDelete = Post.objects.filter(blockIndex=None, timeStamp__lt=(blockTimeStamp))

        for post in postsToDelete:
            post.delete()



        newBlock = Block(index=blockIndex, previousBlockHash=previousBlockHash, timeStamp=blockTimeStamp,
                         blockHash=blockHash, nonce=blockNonce, target=blockTarget)

        print('block should be saved')
        newBlock.save()

        badBlockHandler(True)
        print("added new block: " + str(blockHash))
        return ""
    else:
        badBlockHandler(False)
        print("newblock error: did not meet target")

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




def badChainFixer(firstBadBlockTimeObject):
    rebuildStatus = Data.objects.get(datumTitle="Rebuilding")

    if rebuildStatus.datumContent == "True":

        return "rebuildStatus is true"
    else:
        rebuildStatus.datumContent = "True"
        rebuildStatus.save()

    # StartBadChainProcedures

    currentIndex = int(getHeight.GetHeight()[1])

    if currentIndex == 0:
        return "genisis block"

    postsOfLatestBlock = Post.objects.filter(blockIndex=int(currentIndex))


    for post in postsOfLatestBlock:

        post.delete()

    latestBlock = Block.objects.get(index=currentIndex)

    latestBlock.delete()

    count = 0

    feedback = nodeHelperFunctions.getHighestNode(currentIndex)

    if feedback[0] != '':
        rebuildStatus.datumContent = "False"

        rebuildStatus.save()
        return feedback[0]

    #sorted_nodeData = sorted(nodeData.items(), key=operator.itemgetter(0), reverse=True)

    highestNode = feedback[1]




    blockIndexRange = [currentIndex, highestNode['Height']]



    url = "http://" + highestNode['Host'] + "/getBlocks/"



    payload = {'attribute' : 'index', 'attributeParameters' : str(blockIndexRange)}


    blockArray = []
    try:
        r = requests.post(url, timeout=0.1, data=payload)


        blockArray = ast.literal_eval(str(r.text))
    except:

        rebuildStatus.datumContent = "False"

        rebuildStatus.save()
        return 'could not get blockArray from highest node'

    count = 0
    for block in blockArray:

        if (count % 2 != 0):
            count += 1
            continue

        currentIndex = int(getHeight.GetHeight()[1])

        if block[0] != currentIndex:
            rebuildStatus.datumContent = "False"

            rebuildStatus.save()

            nodeHelperFunctions.blackList(highestNode['Host'])
            return 'blockArray is not sorted'




        blockFeedback = blockHandler(block[0], block[1], block[2], block[3], block[4], blockArray[count + 1], True, False, True, [0,0])

        if blockFeedback != "":

            nodeHelperFunctions.blackList(highestNode['Host'])


            return "invalid blocks given"




        count = count + 1



    firstBadBlockTimeObject.datumContent = 0
    firstBadBlockTimeObject.save()

    rebuildStatus.datumContent = "False"

    rebuildStatus.save()
    return ""

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

        feedback = badChainFixer(firstBadBlockTimeObject)
        print(feedback)

    else:

        firstBadBlockTimeObject.datumContent = timeToStartBadChainProcedures
        firstBadBlockTimeObject.save()

    return



