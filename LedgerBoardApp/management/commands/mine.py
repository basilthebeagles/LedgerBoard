from django.core.management.base import BaseCommand, CommandError

import time
import hashlib
from LedgerBoardApp.models import Block
from LedgerBoardApp.helperFunctions import blockHelperFunctions
from LedgerBoardApp.helperFunctions import distributeEntity
from LedgerBoardApp.helperFunctions import getPosts






class Command(BaseCommand):

    def add_arguments(self, parser):
        print('')
        parser.add_argument('selfHost', nargs='+', type=str)


    def handle(self, *args, **options):

        selfHost = ""

        for host in options['selfHost']:
            selfHost = host

        timeOfLastValidBlock = int(time.time())

        feedback = ""
        while True: #we'll make this better


            timeForValidBlockInMin = (time.time() - timeOfLastValidBlock) / 60

            print("Valid block took "  + str(timeForValidBlockInMin) + " minutes. ")
            timeOfLastValidBlock = int(time.time())

            latestBlock = Block.objects.latest('index')   #fix this up see if u can get the latest attribute

            protoIndex = latestBlock.index + 1


            protoPreviousBlockHash = latestBlock.blockHash

            protoTarget = blockHelperFunctions.getTargetForBlock(protoIndex)

            print("protoTarget: " + protoTarget)

            nonceRange = [1, 68]

            count = 0

            currentTimeForMeasurement = int(time.time())

            while True:

                currentTime = int(time.time())

                posts = getPosts.GetPosts('timeStampForBlockUse', [latestBlock.timeStamp, currentTime])[1]


                feedback = blockHelperFunctions.blockHandler(protoIndex, currentTime, protoPreviousBlockHash, protoTarget, 16, posts, True, True, False, nonceRange)

                if feedback == "" or feedback == "new valid block recieved whilst mining":
                    
                    break
                print(feedback)

                if (count % 3 != 0) and count != 0:
                    timeForBlockHashing = int(time.time()) - currentTimeForMeasurement

                    timePerBlock = 204 / timeForBlockHashing
                    print(str(timePerBlock) + " hashes a second")



                    currentTimeForMeasurement = int(time.time())
                    count += 1








                nonceRange[0] = nonceRange[1] + 1
                nonceRange[1] = nonceRange[1] + 69
                count += 1
            if feedback == "new valid block recieved whilst mining":
                continue

            newBlock = Block.objects.get(index=protoIndex)
            newBlockDataArray = [newBlock.index, newBlock.timeStamp, newBlock.previousBlockHash, newBlock.target, newBlock.nonce, str(posts)]

            distributeEntity.distributeEntity(newBlockDataArray, 'block', selfHost, selfHost)
            #take me out