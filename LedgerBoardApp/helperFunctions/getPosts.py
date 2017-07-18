from LedgerBoardApp.models import Post

from LedgerBoardApp.models import Block
import ast


def GetPosts(attribute, attributeParameters):

    parameters = ast.literal_eval(str(attributeParameters))

    postArray = []

    flaggedPosts = ''

    try:

        if attribute == 'publicKey':
            flaggedPosts = Post.objects.filter(publicKeyOfSender=parameters[0])

        elif attribute == 'timeStamp':
            flaggedPosts = Post.objects.filter(timeStamp__gte=(parameters[0]), timeStamp__lte=(parameters[1]))
        elif attribute == 'timeStampForBlockUse':
            flaggedPosts = Post.objects.filter(timeStamp__gte=(parameters[0]), timeStamp__lt=(parameters[1]))
        elif attribute == "blockIndex":
            flaggedPosts = Post.objects.filter(blockIndex__gte=parameters[0], blockIndex__lte=parameters[1])
        else:
            return ("invalid attribute", [])

        flaggedPosts.order_by('timeStamp')

        for post in flaggedPosts:
            postDataArray = []

            postDataArray.append(post.publicKeyOfSender)
            postDataArray.append(post.timeStamp)
            postDataArray.append(post.content)
            postDataArray.append(post.signature)

            postArray.append(postDataArray)

        return ("", postArray)


    except:
        return ("Invalid interval.", [])

