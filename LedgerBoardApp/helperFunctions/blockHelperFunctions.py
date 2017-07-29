import hashlib
import time
import requests

import bcrypt

from LedgerBoardApp.models import Block
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Data

from LedgerBoardApp.helperFunctions import getHeight
from LedgerBoardApp.helperFunctions import postHelperFunctions
from LedgerBoardApp.helperFunctions import nodeHelperFunctions



import ast


import random




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



    amalgationA = str(previousBlock.index) + str(previousBlock.timeStamp) + str(previousBlock.timeStamp) + str(previousBlock.nonce) + str(intendedPostsForBlock)
    amalgationB = str(blockIndex) + str(blockTimeStamp) + str(previousBlockHash) + str(blockNonce) + str(intendedPostsForBlock)

    if newBlockStatus == True and amalgationA == amalgationB:
        print("newblock error: Block already exists on chain." )

        return "Block already exists on chain."



    if previousBlock.blockHash != previousBlockHash:



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


    if orphanBlockStatus != True: #in this situation (if orphan was true) none of the given posts would exist in the database already since they would be deleted/different as different chain
        intendedPostsForBlockLength = len(intendedPostsForBlock)
        if intendedPostsForBlockLength != 0:
            if newBlockStatus and ((amountOfPostsThatAlreadyExist / intendedPostsForBlockLength) < 0.51):
                print("Posts given do not match up enough with node's posts.")
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
            return "x"



    else:
        blockHash = bcrypt.kdf(password=bytes.fromhex(blockPreHash), salt= bytes(blockNonce), rounds= 100, desired_key_bytes= 32).hex()



    if newBlockStatus != True:
        return "Block is valid."
    print("block hash: " + blockHash)
    if metTarget(blockHash, blockTarget):

        if newBlockStatus != True:
            if blockHash == Block.objects.get(blockIndex = blockIndex).blockHash:
                return "Block verified."

            else:
                return "Hashs do not match up."



        count = 0
        for post in intendedPostsForBlock:

            if Post.objects.filter(postHash=appendedPostHashesArray[count] ).exists():
                tempPost = Post.objects.get(postHash=appendedPostHashesArray[count])
                tempPost.blockIndex = blockIndex
                tempPost.save()


            else:
                newPost = Post(publicKeyOfSender=post[0], timeStamp=post[1], content=post[2], signature=post[3], postHash=appendedPostHashesArray[count], blockIndex=blockIndex)
                newPost.save()
            count += 1

        postsToDelete = Post.objects.filter(blockIndex=None, timeStamp__lt=(blockTimeStamp))

        for post in postsToDelete:
            post.delete()



        newBlock = Block(index=blockIndex, previousBlockHash=previousBlockHash, timeStamp=blockTimeStamp,
                         blockHash=blockHash, nonce=blockNonce, target=blockTarget)

        newBlock.save()
        if miningStatus != True:
            badBlockHandler(True)
        print("added new block: " + str(blockHash))
        return ""
    else:
        badBlockHandler(False)
        print("newblock error: did not meet target")

        return "Did not meet target."

def metTarget(blockHash, blockTarget):



    if int(blockHash, 16) <= int(blockTarget, 16):


        return True
    else:

        return False


def getTargetForBlock(index):

    if index < 2016:

        genesisBlock = Block.objects.get(index=0)



        return genesisBlock.target
               

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


#below function will be called at startup or when node hasnt received a valid block for a while (indicates that it may've gone off chain after an orphan block)
#So it identifies the blocks it is missing when compared to the longest chain and then deletes any 'off chain blocks' and reconfigures to the longest chain.

def badChainFixer(firstBadBlockTimeObject):


    # StartBadChainProcedures

    currentIndex = int(getHeight.GetHeight()[1])

    if currentIndex == 0:
        return "genisis block"





    count = 0
    feedback = nodeHelperFunctions.getHighestNode(currentIndex)

    if feedback[0] == "could not find node higher than current index":
        currentTime = int(time.time())
        highestNode = feedback[1]

        url = "http://" + highestNode['Host'] + "/getPosts/"

        currentIndex = int(getHeight.GetHeight()[1])

        latestBlock = Block.objects.get(index=currentIndex)

        payload = {'attribute': 'timeStamp', 'attributeParameters': str([latestBlock.timeStamp, currentTime])}

        postArray = []

        try:
            r = requests.post(url, timeout=2, data=payload)

            postArray = ast.literal_eval(str(r.text))
        except:


            return 'could not get postArray from highest node'

        firstBadBlockTimeObject.datumContent = 0
        firstBadBlockTimeObject.save()





        return "updated posts."
    elif feedback[0] != '':

        return feedback[0]

    #sorted_nodeData = sorted(nodeData.items(), key=operator.itemgetter(0), reverse=True)

    highestNode = feedback[1]


    #loop through our blokc until we find one in node. Then delete all of our one to that block and rebuild

    blockIndexRange = [1, highestNode['Height']] #remember the technical current index is this minus one since its been deleted


    url = "http://" + highestNode['Host'] + "/getBlocks/"



    payload = {'attribute' : 'index', 'attributeParameters' : str(blockIndexRange)}


    blockArray = []
    try:
        r = requests.post(url, timeout=10, data=payload)


        blockArray = ast.literal_eval(str(r.text))
    except:


        return 'could not get blockArray from highest node'

    count = 0

    allLocalBlocks = Block.objects.all().order_by('-index')

    breakOutOfSecondLoop = False

    indexToStartFrom = 0

    for localBlock in allLocalBlocks:
        count = 0
        for block in blockArray:
            if (count % 2 != 0):
                count += 1
                continue
            #print("block: " + str(block))

            if block[2] == localBlock.blockHash:
                indexToStartFrom = int(block[0])
                breakOutOfSecondLoop = True
                break
            count += 1
        if breakOutOfSecondLoop:
            break



    for localBlock in allLocalBlocks:

        localBlockIndex = localBlock.index

        if localBlockIndex >= indexToStartFrom:
            postsOfLatestBlock = Post.objects.filter(blockIndex=int(localBlockIndex))


            for post in postsOfLatestBlock:
                post.delete()

            localBlock.delete()



    count = 0
    for block in blockArray:



        if (count % 2 != 0):
            count += 1
            continue

        if int(block[0]) < indexToStartFrom:
            count += 1
            continue
        currentIndex = int(getHeight.GetHeight()[1])
        print("so called currentIndex:" + str(currentIndex))
        if block[0] != (currentIndex + 1):

            #print("BLACKLISTINGING AS blockArray is not sorted")
            #nodeHelperFunctions.blackList(highestNode['Host'])
            return 'blockArray is not sorted'




        blockFeedback = blockHandler(block[0], block[1], block[2], block[3], block[4], str(blockArray[count + 1]), True, False, True, [0,0])

        if blockFeedback != "":

            nodeHelperFunctions.blackList(highestNode['Host'])
            print("BLACKLISTINGING AS invalid blocks given")


            return "invalid blocks given"




        count = count + 1


    currentTime = int(time.time())



    url = "http://" + highestNode['Host'] + "/getPosts/"

    currentIndex = int(getHeight.GetHeight()[1])

    latestBlock = Block.objects.get(index=currentIndex)


    payload = {'attribute': 'timeStamp', 'attributeParameters': str([latestBlock.timeStamp, currentTime])}

    postArray = []


    try:
        r = requests.post(url, timeout=2, data=payload)


        postArray = ast.literal_eval(str(r.text))
    except:


        return 'could not get blockArray from highest node'


    for post in postArray:

        feedback = postHelperFunctions.NewPost(publicKey=post[0], timeStamp=post[1], content=post[2], signature=post[3], notNewToNetwork=True)



    firstBadBlockTimeObject.datumContent = 0
    firstBadBlockTimeObject.save()


    return ""

#this function decides whether the node has gone off chain or not (due to orphan block etc).


def badBlockHandler(chainableBlockOccured):
    firstbadBlockTime = 0


    firstBadBlockTimeObject = Data.objects.get(datumTitle="Time of First Bad Block After Chainable Block")
    if chainableBlockOccured:
        firstBadBlockTimeObject.datumContent = 0
        firstBadBlockTimeObject.save()
        return

    firstBadBlockTime = int(firstBadBlockTimeObject.datumContent)

    currentTime = time.time()

    if firstBadBlockTime == 0:
        firstBadBlockTimeObject.datumContent = int(time.time())

        firstBadBlockTimeObject.save()
        print(firstBadBlockTimeObject.datumContent)
        print("here^")
        return

    timeToStartBadChainProcedures = firstBadBlockTime + 2400 + random.randint(100, 2400) #
    print("timeToStartBadChainProcedures: " + str(timeToStartBadChainProcedures))
    if currentTime - timeToStartBadChainProcedures > 0:
        feedback = "x"

        feedback = badChainFixer(firstBadBlockTimeObject)
        print(feedback)





    return



