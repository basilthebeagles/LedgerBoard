# Create your views here.
#need to handle orphans etc.

import time


from django.http import HttpResponse
#from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from LedgerBoardApp.helperFunctions.blockHelperFunctions import blockHandler
from LedgerBoardApp.helperFunctions.distributeEntity import distributeEntity
from LedgerBoardApp.helperFunctions.getBlocks import GetBlocks
from LedgerBoardApp.helperFunctions.getPosts import GetPosts
from LedgerBoardApp.helperFunctions.getNodes import GetNodes
from LedgerBoardApp.helperFunctions.getHeight import GetHeight
from LedgerBoardApp.helperFunctions.addNewHosts import AddNewHosts




from LedgerBoardApp.helperFunctions.nodeHelperFunctions import NewNode
from LedgerBoardApp.helperFunctions.postHelperFunctions import NewPost

from LedgerBoardApp.StartUp import StartUp


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

    feedback = NewPost(publicKey, timeStamp, content, signature, False)

    if feedback != "":
        response.status_code = 406
        response.content = feedback
        return response

    print('bjj')
    response.status_code = 201
    response.content = "Success."

    postDataArray = [publicKey, timeStamp, content, signature]
    distributeEntity(postDataArray, "post")

    return response
@csrf_exempt

def newBlock(request):
    response = HttpResponse()
    rawPostData = request.POST

    try:
        blockIndex = int(rawPostData.__getitem__('index'))
        timeStamp = int(rawPostData.__getitem__('ts'))
        previousBlockHash = rawPostData.__getitem__('prevBlockHash')
        target = rawPostData.__getitem__('target')
        nonce = int(rawPostData.__getitem__('nonce'))



    except:
        response.status_code = 406
        response.content = "Missing content."
        return response

    feedback = blockHandler(blockIndex, timeStamp, previousBlockHash, target, nonce, True, False, False, [0, 0])

    if feedback != "":
        response.status_code = 406
        response.content = feedback
        return response

    response.status_code = 201
    response.content = "Success."

    blockDataArray = [blockIndex, timeStamp, previousBlockHash, target, nonce]

    distributeEntity(blockDataArray, "block")

    return response
@csrf_exempt

def handShake(request):

    response = HttpResponse()
    rawPostData = request.POST
    host = ""
    version = ""
    currentTime = 0
    givenTime = 0
   # defaultStatus = False

    try:
        if rawPostData.__getitem__('programName') == 'LedgerBoard':
            try:
                print('handshake fine1')
                host = str(rawPostData.__getitem__('host'))
                print("host is: " + host)

                version = str(rawPostData.__getitem__('vers'))
                print('handshake fine3')

                givenTime = int(rawPostData.__getitem__('currentTime'))
                print('handshake fine4')

                currentTime = time.time()
                print('handshake fine1')
                #defaultStatus = rawPostData.__getitem__('defaultStatus')



            except:
                response.status_code = 406
                response.content = "Missing content in handshake"
                return response
        else:
            response.status_code = 421
            response.content = "Wrong program"
            return response



    except:

        response.status_code = 421
        response.content = "Wrong program"
        return response

    if abs(currentTime - givenTime) > 5:
        response.status_code = 403
        response.content = "Clock is out of sync."
        return response

    feedback = NewNode(host, version)
    if feedback != "":
        response.status_code = 406
        response.content = feedback
        return response

    response.status_code = 200
    response.content = "Connection created."
    return response
@csrf_exempt
def getBlocks(request):
    response = HttpResponse()
    rawPostData = request.POST


    try:
        attribute = rawPostData.__getitem__('attribute')
        attributeParameters = rawPostData.__getitem__('attributeParameters')

    except:
        response.status_code = 406
        response.content = "Missing data."
        return response

    feedback = GetBlocks(attribute, attributeParameters)
    if feedback[0] == "":
        response.content = str(feedback[1])
        response.status_code = 200
        return response
    else:
        response.content = feedback[0]
        response.status_code = 404
        return response



@csrf_exempt
def getPosts(request):
    response = HttpResponse()
    rawPostData = request.POST


    try:
        attribute = rawPostData.__getitem__('attribute')
        attributeParameters = rawPostData.__getitem__('attributeParameters')

    except:
        response.status_code = 406
        response.content = "Missing data."
        return response

    feedback = GetPosts(attribute, attributeParameters)
    if feedback[0] == "":
        response.content = str(feedback[1])
        response.status_code = 200
        return response
    else:
        response.content = feedback[0]
        response.status_code = 404
        return response
@csrf_exempt
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

    feedback = GetNodes()#attribute, attributeParameter)
    if feedback[0] == "":
        response.content = str(feedback[1])
        response.status_code = 200
        return response
    else:
        response.content = feedback[0]
        response.status_code = 404
        return response

@csrf_exempt
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

    feedback = GetHeight()
    if feedback[0] == "":
        response.content = str(feedback[1])
        response.status_code = 200
        return response
    else:
        response.content = feedback[0]
        response.status_code = 404
        return response

@csrf_exempt
def startUp(request):
    response = HttpResponse()
    rawPostData = request.POST

    feedback = StartUp(str(request.get_host()))
    if feedback == "":
        response.content = "success"
    else:
        response.content = feedback

    return response

@csrf_exempt
def addNewHosts(request):
    response = HttpResponse()
    rawPostData = request.POST
    host = str(rawPostData.__getitem__('host'))
    version = str(rawPostData.__getitem__('vers'))

    feedback = AddNewHosts(host, version, str(request.get_host()))

    if feedback != '':
        response.status_code = 406
        response.content = feedback
        return response
    else:
        response.status_code = 200
        response.content = "success"
        return response


