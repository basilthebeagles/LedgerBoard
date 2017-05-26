from django.db import models


# Create your models here.
class Block(models.Model):

    index = models.IntegerField
    index.primary_key = True

    previousBlockHash = models.CharField(max_length=64)
    timestamp = models.DateField()
    #can put hash logic here


class Post(models.Model):

    publicKeyOfSender = models.CharField(max_length=64)

    signature = models.CharField(max_length=128)

    timestamp = models.DateField()

    content  = models.CharField(max_length=140)

    postHash = models.CharField(max_length=64, primary_key= True)



    blockIndex = models.IntegerField



    #reject if post exists with same selfHash






    
