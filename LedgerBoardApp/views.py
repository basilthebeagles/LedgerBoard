from django.http import HttpResponse
# Create your views here.
import hashlib

import ecdsa
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from ecdsa import VerifyingKey

import rsa



@csrf_exempt

def newPost(request):
    #error handling pls
    response = HttpResponse()
    rawPostData = request.POST

    publicKey = str(rawPostData.__getitem__('pubk'))

    timeStamp = rawPostData.__getitem__('ts') #verify this later


    signature =  str(rawPostData.__getitem__('sig'))

    content = str(rawPostData.__getitem__('content'))



    if publicKey.__len__() != 128:
        response.status_code = 406
        response.content = "Public key must be 64 characters long."
        return response

    if signature.__len__() != 128:
        response.status_code = 406
        response.content = "Signature must be 128 characters long."
        return response

    if content.__len__() > 140:
        response.content = "Post must be less than or equal to 140 characters long."
        response.status_code = 406
        return response


    #IMPORTANT. CHECK TIME IS NOT +- 30s
#sig is signed postHash
    totalPostContent = publicKey + content + timeStamp

    postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()

    print(str(postHash))

    if verifySig(signature, publicKey, postHash) == False:
        response.content = "Error in verifying signature."
        response.status_code = 406
        return response





    #check for duplicate

    #postRecord = Post(publicKeyOfSender = publicKey, signature = signature, postHash= postHash, content = content, timeStamp = timeStamp)

    #save the record.
    #after that I just need to make the block logic & timestamp check

    print('bjj')

    return response

def verifySig(signature, publicKey, postHash):




    vk = VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1)

    if vk.verify(bytes.fromhex(signature), bytes.fromhex(postHash)):#if postHash is a hex string then use bytes.fromhex
        print("verified")
        return True
    else:
        return False

