import hashlib
import time
import ecdsa
from LedgerBoardApp.models import Post


from ecdsa import VerifyingKey



def verifySig(signature, publicKey, postHash):




    vk = VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1)

    try:
        if vk.verify(bytes.fromhex(signature), bytes.fromhex(postHash)):#if postHash is a hex string then use bytes.fromhex
            print("verified")
            return True

    except:
        return False


def postHandler(publicKey, timeStamp, content, signature, save):

    feedback = ""

    if publicKey.__len__() != 128:
        feedback = "Public key must be 128 characters long."
        return feedback

    if signature.__len__() != 128:
        feedback = "Signature must be 128 characters long."
        return feedback

    if content.__len__() > 140:
        feedback = "Post must be less than or equal to 140 characters long."
        return feedback

    if abs(timeStamp - time.time()) > 30:
        feedback = "Post is too old."
        return feedback

    #sig is signed postHash
    totalPostContent = publicKey + str(timeStamp) + content

    postHash = hashlib.sha256(totalPostContent.encode('utf-8')).hexdigest()

    print(str(postHash))

    if verifySig(signature, publicKey, postHash) == False:
        feedback = "Error in verifying signature."
        return feedback

    if Post.objects.filter(postHash = postHash).exists():
        feedback = "Exact post already exists."
        return feedback

    if save == True:
        postRecord = Post(publicKeyOfSender=publicKey, signature=signature, postHash=feedback[1], content=content,
                          timeStamp=timeStamp)

        postRecord.save()

    return feedback

#pass on post to other nodes!!!!!!!!!!!!

