from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.db import models
import time
import hashlib
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Block
from LedgerBoardApp.helperFunctions import blockHelperFunctions



class Command(BaseCommand):

    def add_arguments(self, parser):
        print('')

    def handle(self, *args, **options):
        while True: #we'll make this better
            target = blockHelperFunctions.getTargetForBlock()


            latestBlock = Block.objects.latest('timeStamp')   #fix this up see if u can get the latest attribute

            protoIndex = latestBlock.index + 1


            protoPreviousBlockHash = latestBlock.blockHash

            protoTarget = blockHelperFunctions.getTargetForBlock(protoIndex)



            while True:
                currentTime = int(time.time())



                feedback = blockHelperFunctions.blockHandler(protoIndex, currentTime, protoPreviousBlockHash, protoTarget, 16, True, True) #get final nonce from here

                if feedback == "":
                    break


