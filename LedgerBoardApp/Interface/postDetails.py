
from datetime import datetime, timezone

from LedgerBoardApp.models import Post
from LedgerBoardApp.helperFunctions.getHeight import GetHeight


def PostDetails(postHash):

    post = Post.objects.filter(postHash=postHash)


    if post.exists():
        post = Post.objects.get(postHash=postHash)

        timeAndDate = datetime.fromtimestamp(post.timeStamp, timezone.utc)

        timeAndDate.dst()

        ts = timeAndDate.strftime('%d/%m/%Y %H:%M:%S')


        height = int(GetHeight()[1])

        confirmations = ""

        text = ""

        if post.blockIndex == None:
            text = "not included yet"
            confirmations = "N/A"
        else:
            confirmations = height - int(post.blockIndex)

            text = str(post.blockIndex)



        return "Post Hash: " + post.postHash + "<br/>Broadcaster: " + post.publicKeyOfSender + "<br/>Posted at: " + str(ts) + " (UTC)"+ "<br/>Confirmations: " + str(confirmations) + "<br/>Included in block: " + text +  "</br><br/>Content: " + post.content   + "</br><br/>Signature: " + post.signature + "<br/><br/><br/>"



    else:
        return "Post does not exist"
