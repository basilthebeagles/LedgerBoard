from LedgerBoardApp.models import Post

from LedgerBoardApp.models import Block
import ast


def getPosts(attribute, attributeParameter):
    parameter = ast.literal_eval(str(attributeParameter))

    postArray = []

    flaggedPosts = ''

    try:

        if attribute == 'publicKey':
            flaggedPosts = Post.objects.filter(publicKeyOfSender=parameter[0])

        elif attribute == 'timeStamp':
            flaggedPosts = Post.objects.filter(timeStamp__gt=(parameter[0]), timeStamp__lt=(parameter[1]))

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

