from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.db import models
import time
import hashlib
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Block
from LedgerBoardApp.helperFunctions import blockHelperFunctions
from LedgerBoardApp.helperFunctions import distributeEntity
from LedgerBoardApp.helperFunctions import getPosts






class Command(BaseCommand):

    def add_arguments(self, parser):
        print('')

    def handle(self, *args, **options):
        feedback = ""
        while True: #we'll make this better


            latestBlock = Block.objects.latest('index')   #fix this up see if u can get the latest attribute

            protoIndex = latestBlock.index + 1


            protoPreviousBlockHash = latestBlock.blockHash

            protoTarget = blockHelperFunctions.getTargetForBlock(protoIndex)

            print(protoTarget)

            nonceRange = [1, 16]
            while True:

                currentTime = int(time.time())

                posts = getPosts.GetPosts('timeStampForBlockUse', [latestBlock.timeStamp, currentTime])


                feedback = blockHelperFunctions.blockHandler(protoIndex, currentTime, protoPreviousBlockHash, protoTarget, 16, posts, True, True, False, nonceRange)

                if feedback == "" or feedback == "new valid block recieved whilst mining":
                    
                    break
                print(feedback)
                nonceRange[0] = nonceRange[1] + 1
                nonceRange[1] = nonceRange[1] + 17  #int(round(nonceRange[1] * 1.5))

            if feedback == "new valid block recieved whilst mining":
                continue

            newBlock = Block.objects.get(index=protoIndex)
            newBlockDataArray = [newBlock.index, newBlock.timeStamp, newBlock.previousBlockHash, newBlock.target, newBlock.nonce, str(posts)]

            distributeEntity.distributeEntity(newBlockDataArray, 'block')
