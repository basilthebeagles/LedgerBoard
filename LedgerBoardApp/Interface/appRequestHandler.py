
from LedgerBoardApp.models import Block
from LedgerBoardApp.models import Post
from LedgerBoardApp.helperFunctions.getHeight import GetHeight
from LedgerBoardApp.helperFunctions.getPosts import GetPosts
from LedgerBoardApp.helperFunctions.getBlocks import GetBlocks


from LedgerBoardApp.helperFunctions import postHelperFunctions
from LedgerBoardApp.helperFunctions import blockHelperFunctions



def AppRequestHandler(attribute, parameter):
    try:
        if attribute == "Broadcaster":

            return GetPosts(attribute, [parameter])

        elif attribute == "Block":
            blockIndex = 0
            if parameter == 'latest':
                blockIndex = int(GetHeight()[1])
            else:
                blockIndex = int(parameter)

            return GetBlocks([blockIndex, blockIndex])

        elif attribute == "Post":
            post = Post.objects.filter(postHash=parameter)

            if post.exists():
                post = Post.objects.get(postHash=parameter)


                postDataArray = []

                postDataArray.append(post.publicKeyOfSender)
                postDataArray.append(post.timeStamp)
                postDataArray.append(post.content)
                postDataArray.append(post.signature)

                return ("", postDataArray)

            else:
                return ("Post not found.", [])


        else:
            return ("invalid parameter", "")
    except:
        return ("Error", "")

