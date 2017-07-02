from django.db import models


# Create your models here.
class Block(models.Model):

    index = models.IntegerField(primary_key = True)

    previousBlockHash = models.CharField(max_length=64)
    timeStamp = models.IntegerField(null = True)

    blockHash = models.CharField(max_length=64)
    nonce = models.IntegerField(null = True)

    target = models.IntegerField()





class Post(models.Model):

    publicKeyOfSender = models.CharField(max_length=64)

    signature = models.CharField(max_length=128 )


    content  = models.CharField(max_length=140)

    postHash = models.CharField(max_length=64, primary_key= True)

    timeStamp = models.IntegerField()


    blockIndex = models.IntegerField(null=True, blank=True)



class Node(models.Model):

    host = models.CharField(max_length=64) #changeThisToSomethingBetter
    version = models.CharField(max_length=64) #changeThisToSomethingBetter

    #defaultStatus = models.BinaryField()
    secondsSinceLastInteraction = models.IntegerField()



class Data(models.Model):

    datumTitle =  models.CharField(max_length=64)
    datumContent = models.CharField(max_length=64)
