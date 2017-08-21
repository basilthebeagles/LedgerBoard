
from LedgerBoardApp.models import Block
from LedgerBoardApp.models import Post
from LedgerBoardApp.helperFunctions.getHeight import GetHeight
from LedgerBoardApp.helperFunctions.getPosts import GetPosts
from LedgerBoardApp.helperFunctions.getBlocks import GetBlocks
import ast

from LedgerBoardApp.helperFunctions import postHelperFunctions
from LedgerBoardApp.helperFunctions import blockHelperFunctions

#WORK OUT JSON

def AppRequestHandler(attribute, parameter):
    try:
        if attribute == "Broadcaster":
            functionResponse = GetPosts("publicKey", [parameter])

            if functionResponse[0] != "":
                return functionResponse
            else:

                broadcasterPostArray = ast.literal_eval(str(functionResponse[1]))

                JSONResponse = {}
                JSONResponse['currentHeight'] = int(GetHeight()[1])

                JSONResponse['postArray'] = []
                for post in broadcasterPostArray:
                    dict = {}

                    dict['publicKey'] = post[0]
                    dict['timeStamp'] = post[1]
                    dict['content'] = post[2]
                    dict['signature'] = post[3]
                    JSONResponse['postArray'].append(dict)



                return ("", JSONResponse)






        elif attribute == "Block":
            blockIndex = 0
            if parameter == 'latest':
                blockIndex = int(GetHeight()[1])
            else:
                blockIndex = int(parameter)
            functionResponse = GetBlocks('index', [blockIndex, blockIndex])

            if functionResponse[0] != "":
                return functionResponse
            else:

                blockArray = ast.literal_eval(str(functionResponse[1]))
                JSONResponse = {}
                JSONResponse['currentHeight'] = int(GetHeight()[1])
                JSONResponse['blockMetadata'] = {}
                JSONResponse['blockMetadata']['index'] = blockArray[0][0]
                JSONResponse['blockMetadata']['timeStamp'] = blockArray[0][1]
                JSONResponse['blockMetadata']['previousBlockHash'] = blockArray[0][2]
                JSONResponse['blockMetadata']['target'] = blockArray[0][3]
                JSONResponse['blockMetadata']['nonce'] = blockArray[0][4]

                JSONResponse['postDictArray'] = []

                for post in blockArray[1]:

                    dict = {}

                    dict['publicKey'] = post[0]
                    dict['timeStamp'] = post[1]
                    dict['content'] = post[2]
                    dict['signature'] = post[3]

                    JSONResponse['postDictArray'].append(dict)









                return ("", JSONResponse)



        elif attribute == "Post":
            post = Post.objects.filter(postHash=parameter)

            if post.exists():
                post = Post.objects.get(postHash=parameter)
                JSONResponse = {}
                JSONResponse['currentHeight'] = int(GetHeight()[1])

                JSONResponse['publicKey'] = post.publicKeyOfSender
                JSONResponse['timeStamp'] = post.timeStamp
                JSONResponse['content'] = post.content
                JSONResponse['signature'] = post.signature
                JSONResponse['blockIndex'] = post.blockIndex


                return ("", JSONResponse)

            else:
                return ("Post not found.", [])


        else:
            return ("invalid parameter", "")
    except:
        return ("Error", "")

