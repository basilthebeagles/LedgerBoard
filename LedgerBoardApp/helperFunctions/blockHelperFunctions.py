import time
import hashlib
import time

import bcrypt

from LedgerBoardApp.models import Block
from LedgerBoardApp.models import Post


#need OrphanBlock procedures













def blockHandler(blockIndex, blockTimeStamp, previousBlockHash, blockTarget, blockNonce, newBlockStatus):


    currentTime = int(time.time())

    if blockTimeStamp > currentTime:
        return "Block is from the future."

    previousBlock = Block.objects.latest('index')




    if previousBlock.blockHash != previousBlockHash:

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


    for post in unblockedPosts:
        if post.timeStamp < Block.objects.latest('timeStamp').timeStamp:
            if newBlockStatus:
                postObjectArrayToBeDeleted.append(post)
        else:
            post.blockIndex = blockIndex
            appendedPostHashesArray.append(post.postHash)
            if newBlockStatus:
                postObjectArrayToBeSaved.append(post)




    blockTotalContents = str(blockIndex) + str(blockTimeStamp) + str(previousBlockHash) + str(blockTarget)+ str(appendedPostHashesArray)
    blockPreHash = hashlib.sha256(blockTotalContents.encode('utf-8')).hexdigest()
    blockHash = bcrypt.kdf(password=bytes.fromhex(blockPreHash), salt= bytes(blockNonce), rounds= 100, desired_key_bytes= 512).hex()

    if int(blockHash, 16) < blockTarget:

        if newBlockStatus:
            for post in postObjectArrayToBeSaved:
                post.save()
            for post in postObjectArrayToBeDeleted:
                post.delete()
            newBlock = Block(index= blockIndex, previousBlockHash=previousBlockHash, timeStamp=blockTimeStamp, blockHash=blockHash, nonce= blockNonce, target=blockTarget)
            newBlock.save()

        return ""
    else:

        return "Block did not meet target."


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















