from django.db import models


# Create your models here.
class Block(models.Model):

    index = models.IntegerField
    index.primary_key = True

    previousBlockHash = models.CharField(max_length=64)
    timestamp = models.DateField(auto_now=True)






    
