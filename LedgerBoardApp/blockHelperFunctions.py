from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.db import models
import time
import hashlib
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Block
from operator import itemgetter, attrgetter
from LedgerBoardApp.postHelperFunctions import verifyPost

#need OrphanBlock procedures


def receiveNewBlock(blockIndex, previousBlockHashFromNewBlock, timeStamp, nonce, postTupleArray):

    feedBack = ""








    #post array [0][0] pubk [0][1] ts [0][2] content
    #below should be in verifyBlock function
    #sort given postArray so ts order. Compare to original if same then keep otherwise reject
    #check previousBlockHash is the same as the most recent blocks hash.
    #create long chain of postHashes, storing them in [3] for each post

   #in progress: hash block together with nonce. If below difficulty then accept! (create function to calc difficulty based on last 2056 blocks.
    #above should be in verifyBlock function
    #create new block object and save
    #add block index to all posts in the postobjectarray. Save. Then delete all posts with no block index that are inbertween block ts of prev block (inclusive) and block ts of new block (exclusive)
    #pass on block to other nodes.

def blockHandler(blockIndex, previousBlockHash, timeStamp, nonce, postTupleArray, saveBlockStatus):


    currentTime = int(time.time())

    if timeStamp > currentTime:
        return "Block is from the future."

    previousBlock = Block.objects.latest('index')




    if previousBlock.blockHash != previousBlockHash:

        return "Block does not fit on chain."

    sortedPostTupleArray = sorted(postTupleArray, key=itemgetter(1))  # sort by ts

    if postTupleArray != sortedPostTupleArray:
        return "Posts are not ordered by timestamp."

    if previousBlock.index >= blockIndex:

        return "Block is old."

    earliestPost = sortedPostTupleArray[0]
    latestPost = sortedPostTupleArray[-1]

    if earliestPost[1] < previousBlock.timeStamp:

        return "Includes previous posts."

    if latestPost[1] >= timeStamp:

        return "Includes later posts."

    appendedPostHashesArray = []

    postObjectArrayToBeSaved = []

    for post in sortedPostTupleArray:
        response = verifyPost(post[0], post[1], post[2], post[3])

        if response[0] != "" or response != "Exact post already exists.":
            return "Error in verifying posts."

        if saveBlockStatus and response[0] == "Exact post already exists.":
            postObject = Post.objects.get(postHash=response[1])
            postObjectArrayToBeSaved.append(postObject)

        if saveBlockStatus:
            postObject = Post(publicKeyOfSender=post[0], signature=post[3], postHash=response[1], content=post[2],
                          timeStamp=post[1])
            postObjectArrayToBeSaved.append(postObject)

        appendedPostHashesArray.append(response[1])
    blockTotalContents = str(blockIndex) + str(timeStamp) + str(previousBlockHash) + str(appendedPostHashesArray)

    blockHash = hashlib.pbkdf2_hmac('sha512', blockTotalContents.encode('utf-8'), bytes(nonce), 1000000).hex()









