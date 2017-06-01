from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.db import models
import time
import hashlib
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Block


def receiveNewBlock(blockIndex, previousBlockHash, timeStamp, nonce, postArray):

    #post array [0][0] pubk [0][1] ts [0][2] content

    #sort given postArray so ts order. Compare to original if same then keep otherwise reject
    #below should be in verifyBlock function
    #check previousBlockHash is the same as the most recent blocks hash.
    #create long chain of postHashes, storing them in [3] for each post
    # hash block together with nonce. If below difficulty then accept! (create function to calc difficulty based on last 2056 blocks.
    #above should be in verifyBlock function
    #create new block object and save
    #compare postArray with all posts between prev block timestamp and newBlock timestamp -1.
    #delete any posts that are not in postArray.
    #posts that are in postArray add blockIndex and save.
    #pass on block to other nodes.
