# Create your views here.


from LedgerBoardApp.models import Block

from LedgerBoardApp.postHelperFunctions import postHandler
from LedgerBoardApp.nodeHelperFunctions import newNode


from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

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

    feedback = postHandler(publicKey, timeStamp, content, signature, True)

    if feedback[0] != "":
        response.status_code = 406
        response.content = feedback
        return response

    print('bjj')
    response.status_code = 201
    response.content = "Success."

    return response


def newBlock(request):
    response = HttpResponse()
    rawPostData = request.POST

    try:
        blockIndex = int(rawPostData.__getitem__('index'))
        previousBlockHash = rawPostData.__getitem__('prevBlockHash')
        timeStamp = rawPostData.__getitem__('ts')

        nonce = int(rawPostData.__getitem__('index'))
       # postArray = we'll figure this out...

    except:
        response.status_code = 406
        response.content = "Missing content."
        return response

    feedback =


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
                #defaultStatus = rawPostData.__getitem__('defaultStatus')



            except:
                response.status_code = 406
                response.content = "Missing content in handshake"




    except:

        response.status_code = 421
        response.content = "Wrong program"
        return response

    feedback = newNode(host, version)
    if feedback != "":
        response.status_code = 406
        response.content = feedback
        return response

    response.status_code = 200
    response.content = "Connection created."
    return response