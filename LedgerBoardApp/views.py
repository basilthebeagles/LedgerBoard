# Create your views here.
#need to handle orphans etc.



from django.http import HttpResponse
#from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from LedgerBoardApp.helperFunctions.blockHelperFunctions import blockHandler
from LedgerBoardApp.helperFunctions.distributeEntity import distributeEntity
from LedgerBoardApp.helperFunctions.getBlocks import getBlocks
from LedgerBoardApp.helperFunctions.getPosts import getPosts
from LedgerBoardApp.helperFunctions.getNodes import getNodes
from LedgerBoardApp.helperFunctions.getHeight import getHeight



from LedgerBoardApp.helperFunctions.nodeHelperFunctions import newNode
from LedgerBoardApp.helperFunctions.postHelperFunctions import newPost


@csrf_exempt

#create a getconnections view

def newPost(request):
    #error handling pls

    #gen = Block(index = 0, previousBlockHash= "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9", timeStamp= time.time())

    #gen.save()

    response = HttpResponse()
    rawPostData = request.POST
    try:
        publicKey = str(rawPostData.__getitem__('pubk'))

        timeStamp = int(rawPostData.__getitem__('ts')) #verify this later

        content = str(rawPostData.__getitem__('content'))


        signature =  str(rawPostData.__getitem__('sig'))

    except:
        response.status_code = 406
        response.content = "Missing content."
        return response

    feedback = newPost(publicKey, timeStamp, content, signature, False)

    if feedback[0] != "":
        response.status_code = 406
        response.content = feedback
        return response

    print('bjj')
    response.status_code = 201
    response.content = "Success."

    postDataArray = [publicKey, timeStamp, content, signature]
    distributeEntity(postDataArray, "post", request.get_host())

    return response

def newBlock(request):
    response = HttpResponse()
    rawPostData = request.POST

    try:
        blockIndex = int(rawPostData.__getitem__('index'))
        timeStamp = int(rawPostData.__getitem__('ts'))
        previousBlockHash = rawPostData.__getitem__('prevBlockHash')
        target = int(rawPostData.__getitem__('target'))
        nonce = int(rawPostData.__getitem__('nonce'))



    except:
        response.status_code = 406
        response.content = "Missing content."
        return response

    feedback = blockHandler(blockIndex, timeStamp, previousBlockHash, target, nonce, True, False)

    if feedback != "":
        response.status_code = 406
        response.content = feedback
        return response

    response.status_code = 201
    response.content = "Success."

    blockDataArray = [blockIndex, timeStamp, previousBlockHash, target, nonce]

    distributeEntity(blockDataArray, "block", request.get_host())

    return response

def handShake(request):

    response = HttpResponse()
    rawPostData = request.POST
    host = ""
    version = ""
   # defaultStatus = False

    try:
        if rawPostData.__getitem__('programName') == 'LedgerBoard':
            try:
                host = str(request.get_host())
                version = str(rawPostData.__getitem__('vers'))
                time = int(rawPostData.__getitem__('currentTime'))
                currentTime = time.time()
                #defaultStatus = rawPostData.__getitem__('defaultStatus')



            except:
                response.status_code = 406
                response.content = "Missing content in handshake"




    except:

        response.status_code = 421
        response.content = "Wrong program"
        return response

    if abs(currentTime - time) > 5:
        response.status_code = 403
        response.content = "Clock is out of sync."
        return response

    feedback = newNode(host, version)
    if feedback != "":
        response.status_code = 406
        response.content = feedback
        return response

    response.status_code = 200
    response.content = "Connection created."
    return response

def getBlocks(request):
    response = HttpResponse()
    rawPostData = request.POST


    try:
        attribute = rawPostData.__getitem__('attribute')
        attributeParameter = rawPostData.__getitem__('attributeData')

    except:
        response.status_code = 406
        response.content = "Missing data."

    feedback = getPosts(attribute, attributeParameter)
    if feedback[0] == "":
        response.content = str(feedback[1])
        response.status_code = 200
        return response
    else:
        response.content = feedback[0]
        response.status_code = 404
        return response




def getPosts(request):
    response = HttpResponse()
    rawPostData = request.POST


    try:
        attribute = rawPostData.__getitem__('attribute')
        attributeParameter = rawPostData.__getitem__('attributeData')

    except:
        response.status_code = 406
        response.content = "Missing data."

    feedback = getPosts(attribute, attributeParameter)
    if feedback[0] == "":
        response.content = str(feedback[1])
        response.status_code = 200
        return response
    else:
        response.content = feedback[0]
        response.status_code = 404
        return response

def getNodes(request):
    response = HttpResponse()
    rawPostData = request.POST

    ''' 
    try:
        attribute = rawPostData.__getitem__('attribute')
        attributeParameter = rawPostData.__getitem__('attributeData')

    except:
        response.status_code = 406
        response.content = "Missing data."
    '''

    feedback = getNodes()#attribute, attributeParameter)
    if feedback[0] == "":
        response.content = str(feedback[1])
        response.status_code = 200
        return response
    else:
        response.content = feedback[0]
        response.status_code = 404
        return response


def getHeight(request):
    response = HttpResponse()
    rawPostData = request.POST

    ''' 
    try:
        attribute = rawPostData.__getitem__('attribute')
        attributeParameter = rawPostData.__getitem__('attributeData')

    except:
        response.status_code = 406
        response.content = "Missing data."
    '''

    feedback = getHeight()
    if feedback[0] == "":
        response.content = str(feedback[1])
        response.status_code = 200
        return response
    else:
        response.content = feedback[0]
        response.status_code = 404
        return response

