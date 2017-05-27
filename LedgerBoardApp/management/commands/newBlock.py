from django.core.management.base import BaseCommand, CommandError
from LedgerBoardApp.models import Block
from django.db import models
import time
import hashlib
from LedgerBoardApp.models import Post
from LedgerBoardApp.models import Block



class NewBlock(BaseCommand):

    def add_arguments(self, parser):
        print('')

    def handle(self, *args, **options):

        protoBlock = Block.objects.all().aggregate(max('blockIndex'))

        protoBlockIndex = protoBlock.index()

        blockTimeStamp = time.time()

        unblockedPosts = Post.objects.filter(blockIndex = None, timeStamp__lt = (blockTimeStamp) )

        appendedPostHashes = ""

        unblockedPosts.order_by('timeStamp')

        for post in unblockedPosts:
            if post.timeStamp() <= Block.objects.all().aggregate(max('blockTimeStamp')):
                post.delete()
            else:
                post.blockIndex = protoBlockIndex
                appendedPostHashes += post.postHash()
                post.save()





        protoBlock.timeStamp = blockTimeStamp



        protoBlockTotalContents = str(protoBlockIndex) + str(blockTimeStamp) + appendedPostHashes

        protoBlockHash = hashlib.sha256(protoBlockTotalContents.encode('utf-8')).hexdigest()

        newBlock = Block(index = (protoBlockIndex + 1), previousBlockHash= str(protoBlockHash))

        newBlock.save()



        #.orderby to get in time order
        print('')

#get protoBlock (i.e has index and prevBlockHash)
#get all posts with no index. Add index. somehow hash them all along with other block data. Save block hash and add to new block.
#basically get highest block index. Add timestamp. save. hash. Create new block with hash.