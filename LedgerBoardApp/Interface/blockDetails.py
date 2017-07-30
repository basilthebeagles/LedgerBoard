from LedgerBoardApp.models import Block
from datetime import datetime, timezone

from LedgerBoardApp.models import Post
from LedgerBoardApp.Interface.postDetails import PostDetails
from LedgerBoardApp.helperFunctions.getHeight import GetHeight

#this and the others in this folder are used to answer user requests via http for details of blocks etc...

def BlockDetails(blockIndex):



    if blockIndex == 'latest':
        blockIndex = int(GetHeight()[1])




    block = Block.objects.filter(index=blockIndex)

    if block.exists():
        block = Block.objects.get(index=blockIndex)
        timeAndDate = datetime.fromtimestamp(block.timeStamp, timezone.utc)

        ts = timeAndDate.strftime('%H:%M:%S %d/%m/%Y')


        postsOfBlock = Post.objects.filter(blockIndex=blockIndex)

        numberOfPosts = len(postsOfBlock)

        response = "Block hash: " + block.blockHash + "<br/>Previous block hash: " + block.previousBlockHash + "<br/>Index(height): " + str(blockIndex) +  "<br/>Created at: " + ts + " (UTC)" + "<br/>Number of posts: " + str(numberOfPosts) + "<br/>Target(difficulty): " + str(block.target) + "<br/>Nonce: " + str(block.nonce)


        response += "<br/></br>Posts of block: "
        count = 0
        for post in postsOfBlock:

            response += "<br/></br>" + PostDetails(post.postHash)

            count += 1

        if count == 0:
            response += "<br/></br><h4>No Posts In Block"
        return response


    else:
        return "block does not exist"