from LedgerBoardApp.models import Block
from datetime import datetime, timezone

from LedgerBoardApp.models import Post
from LedgerBoardApp.Interface.postDetails import PostDetails

#this and the others in this folder are used to answer user requests via http for details of blocks etc...

def BlockDetails(blockIndex):


    block = Block.objects.filter(index=blockIndex)

    if block.exists():
        block = Block.objects.get(index=blockIndex)
        timeAndDate = datetime.fromtimestamp(block.timeStamp, timezone.utc)

        ts = timeAndDate.strftime('%H:%M:%S %d/%m/%Y')


        postsOfBlock = Post.objects.filter(blockIndex=blockIndex)

        numberOfPosts = len(postsOfBlock)

        response = "Block hash: " + block.blockHash + "<br/>Previous block hash: " + block.previousBlockHash + "<br/>Index(height): " + str(blockIndex) +  "<br/>Timestamp: " + ts + " (UTC)" + "<br/>Number of posts: " + str(numberOfPosts) + "<br/>Target(difficulty): " + str(block.target) + "<br/>Nonce: " + str(block.nonce)


        response += "<br/>Posts of block: "

        for post in postsOfBlock:

            response += "<br/>" + PostDetails(post.postHash)

        return response


    else:
        return "block does not exist"