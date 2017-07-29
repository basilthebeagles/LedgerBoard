import hashlib
import time
import ecdsa


from ecdsa import VerifyingKey
from LedgerBoardApp.models import Post


def verifySig(signature, publicKey, postHash):






    vk = VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1)

    try:
        if vk.verify(bytes.fromhex(signature), bytes.fromhex(postHash)):#if postHash is a hex string then use bytes.fromhex
            return True

    except:
        return False


def NewPost(publicKey, timeStamp, content, signature, notNewToNetwork):


    if notNewToNetwork != True: #
        if abs(timeStamp - time.time()) > 30:

            return "Post is too old."



    response = verifyPost(publicKey, timeStamp, content, signature)

    if response[0] != "":
        return response[0]


    postRecord = Post(publicKeyOfSender=publicKey, signature=signature, postHash=response[1], content=content,
                          timeStamp=timeStamp)

    postRecord.save()

    print("Added post.")
    print("Public key of sender: " + str(postRecord.publicKeyOfSender))
    print("Content: " + str(postRecord.content))


    return ""
#pass on post to other nodes!!!!!!!!!!!!

def verifyPost(publicKey, timeStamp, content, signature):


    if publicKey.__len__() != 128:
        return ("Public key must be 128 characters long.", "")

    if signature.__len__() != 128:

        return ("Signature must be 128 characters long.", "")

    if content.__len__() > 140:

        return ("Post must be less than or equal to 140 characters long.", "")



    #sig is signed postHash
    totalPostContent = publicKey + str(timeStamp) + content

    postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()


    if verifySig(signature, publicKey, postHash) == False:

        return ("Error in verifying signature.", "")

    if Post.objects.filter(postHash = postHash).exists():

        return ("Exact post already exists.", postHash)

    return ("", postHash)