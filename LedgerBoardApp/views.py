

import time

import json

from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from LedgerBoardApp.helperFunctions.blockHelperFunctions import blockHandler
from LedgerBoardApp.helperFunctions.distributeEntity import distributeEntity
from LedgerBoardApp.helperFunctions.getBlocks import GetBlocks
from LedgerBoardApp.helperFunctions.getPosts import GetPosts
from LedgerBoardApp.helperFunctions.getNodes import GetNodes
from LedgerBoardApp.helperFunctions.getHeight import GetHeight
from LedgerBoardApp.helperFunctions.addNewHosts import AddNewHosts
from django.http import JsonResponse


from LedgerBoardApp.models import Node

from LedgerBoardApp.Interface.postDetails import PostDetails
from LedgerBoardApp.Interface.blockDetails import BlockDetails
from LedgerBoardApp.Interface.broadcasterDetails import BroadcasterDetails

from LedgerBoardApp.Interface.appRequestHandler import AppRequestHandler



from LedgerBoardApp.helperFunctions.nodeHelperFunctions import NewNode
from LedgerBoardApp.helperFunctions.postHelperFunctions import NewPost



@csrf_exempt


def newPost(request):


    response = HttpResponse()
    rawPostData = request.POST
    try:
        publicKey = str(rawPostData.__getitem__('pubk'))

        timeStamp = int(rawPostData.__getitem__('ts'))

        content = str(rawPostData.__getitem__('content'))


        signature =  str(rawPostData.__getitem__('sig'))
        selfHost = str(request.get_host())
        originHost = str(rawPostData.__getitem__('originHost'))




    except:
        response.status_code = 406
        response.content = "Missing content."
        return response



    feedback = NewPost(publicKey, timeStamp, content, signature, False)

    if feedback != "":
        response.status_code = 406
        response.content = feedback
        return response
    nodeInteractionUpdater(originHost, selfHost)

    response.status_code = 201
    response.content = "Success."

    postDataArray = [publicKey, timeStamp, content, signature]
    distributeEntity(postDataArray, "post", originHost, selfHost)

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

        postArray = str(rawPostData.__getitem__('postArray'))

        selfHost = str(request.get_host())
        originHost = str(rawPostData.__getitem__('originHost'))



    except:
        response.status_code = 406
        response.content = "Missing content."
        return response



    feedback = blockHandler(blockIndex, timeStamp, previousBlockHash, target, nonce, postArray, True, False, False, [0, 0])

    if feedback != "":
        response.status_code = 406
        response.content = feedback
        return response
    nodeInteractionUpdater(originHost, selfHost)

    response.status_code = 201
    response.content = "Success."

    blockDataArray = [blockIndex, timeStamp, previousBlockHash, target, nonce, str(postArray)]

    distributeEntity(blockDataArray, "block", originHost, selfHost)

    return response
@csrf_exempt

def handShake(request):

    response = HttpResponse()
    rawPostData = request.POST
    host = ""
    version = ""
    currentTime = 0
    givenTime = 0


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



    feedback = GetNodes()
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
def interfaceBlockDetails(request):
    response = HttpResponse()
    rawGetData = request.GET
    print(rawGetData)
    index = rawGetData.get('blockIndex')
    try:


        response.content = BlockDetails(index)
        return response

    except:
        response.content = "no data given."
        return response


@csrf_exempt
def interfacePostDetails(request):
    response = HttpResponse()
    rawGetData = request.GET

    postHash = rawGetData.get('postHash')

    try:

        response.content = PostDetails(postHash)
        return response

    except:
        response.content = "no data given."
        return response

@csrf_exempt
def interfaceBroadcasterDetails(request):
    response = HttpResponse()
    rawGetData = request.GET

    broadcasterPublicKey = rawGetData.get('broadcasterPublicKey')

    try:

        response.content = BroadcasterDetails(broadcasterPublicKey)
        return response

    except:
        response.content = "no data given."
        return response



@csrf_exempt
def appRequest(request):
    rawPostData = request.POST


    try:
        attribute = rawPostData.__getitem__('attribute')
        attributeParameter = rawPostData.__getitem__('attributeParameter')

    except:
        response = JsonResponse({'error':"Missing data."})

        response.status_code = 406

        return response

    feedback = AppRequestHandler(attribute, attributeParameter)

    if feedback[0] == "":

        response = JsonResponse(feedback[1])
        response.status_code = 200
        return response
    else:
        response = JsonResponse({'error':feedback[0]})

        response.status_code = 404
        return response


def nodeInteractionUpdater(host, selfHost):


    currentTime = int(time.time())

    try:
        node = Node.objects.get(host=str(host))
        node.secondsSinceLastInteraction = currentTime
        node.save()

    except:
        try:
            AddNewHosts(host, 0.1, selfHost)
        except:
            print('')

    return
