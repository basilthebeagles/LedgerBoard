from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from  LedgerBoardApp.models import Post
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from ecdsa import VerifyingKey

import ecdsa
import hashlib

@csrf_exempt

def newPost(request):
    #error handling pls
    response = HttpResponse()
    rawPostData = request.POST

    publicKey = str(rawPostData.__getitem__('pubk'))

    timeStamp = rawPostData.__getitem__('ts') #verify this later


    signature =  str(rawPostData.__getitem__('sig'))

    content = str(rawPostData.__getitem__('content'))



    if publicKey.__len__() != 64:
        response.status_code = 406
        response.content = "Public key must be 64 characters long."
        return response

    if signature.__len__() != 64: #check this
        response.status_code = 406
        response.content = "Public key must be 64 characters long."
        return response

    if content.__len__() > 140:
        response.content = "Post must be less than or equal to 140 characters long."
        response.status_code = 406
        return response


    #IMPORTANT. CHECK TIME IS NOT +- 30s

    totalPostContent = publicKey + signature + content + timeStamp

    postHash = hashlib.sha256(totalPostContent)

    if verifySig(signature, publicKey, postHash) == False:
        response.content = "Error in verifying signature."
        response.status_code = 406
        return response

    # HttpResponse.status_code = 401 (unauth)

    totalPostContent = publicKey + signature + content + timeStamp

    postHash = hashlib.sha256(totalPostContent)

    postRecord = Post(publicKeyOfSender = publicKey, signature = signature, postHash= postHash, content = content, timeStamp = timeStamp)

    postRecord.checkForDuplicate#if this comes back all fine then we can just save the record.
    #after that I just need to make the block logic & timestamp check

    print('bjj')

    return response

def verifySig(signature, publicKey, postHash):



    vk = VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1)

    if vk.verify(bytes.fromhex(signature), postHash):
        return True
    else:
        return False
