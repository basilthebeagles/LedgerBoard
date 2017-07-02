
from LedgerBoardApp.models import Block


def getHeight():

    previousBlock = Block.objects.latest('index')


    height = previousBlock.index


    return ("", str(height))