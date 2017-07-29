
from LedgerBoardApp.models import Post
from LedgerBoardApp.Interface.postDetails import PostDetails



def BroadcasterDetails(publicKeyOfPoster):


    postsOfUser = Post.objects.filter(publicKeyOfSender=publicKeyOfPoster)

    response = ""

    if postsOfUser.exists():
        response += "Broadcaster's (" +  str(publicKeyOfPoster)    + ") posts: <br/><br/></br>"
        for post in postsOfUser:

            response += PostDetails(post.postHash)
        return response

    else:
        return "Broadcaster's (" +  str(publicKeyOfPoster)    + ") has no posts/does not exist."