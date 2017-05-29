from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.db import models
import time
import hashlib
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Block




class Command(BaseCommand):

    def add_arguments(self, parser):
        print('')

    def handle(self, *args, **options):

        protoBlock = Block.objects.latest('index')

        print(protoBlock)
        protoBlockIndex = protoBlock.index

        blockTimeStamp = int(time.time())

        unblockedPosts = Post.objects.filter(blockIndex = None, timeStamp__lt = (blockTimeStamp) )

        appendedPostHashesBytes = b''

        unblockedPosts.order_by('timeStamp')

        for post in unblockedPosts:
            if post.timeStamp <= Block.objects.latest('timeStamp').timeStamp:
                post.delete()
            else:
                post.blockIndex = protoBlockIndex
                appendedPostHashesBytes += bytes.fromhex(post.postHash)
                post.save()



        print(appendedPostHashesBytes)

        protoBlock.timeStamp = blockTimeStamp

        protoBlock.save()

        print("here")
        protoBlockTotalContents = bytes(protoBlockIndex) + bytes(blockTimeStamp) + bytes(appendedPostHashesBytes)

        print("here1")

        protoBlockHash = hashlib.sha256(protoBlockTotalContents).hexdigest()
        print("here2")

        newBlock = Block(index = (protoBlockIndex + 1), previousBlockHash= str(protoBlockHash))

        newBlock.save()



        #.orderby to get in time order
        print('')

#get protoBlock (i.e has index and prevBlockHash)
#get all posts with no index. Add index. somehow hash them all along with other block data. Save block hash and add to new block.
#basically get highest block index. Add timestamp. save. hash. Create new block with hash.