
from LedgerBoardApp.models import Block


def GetHeight():

    previousBlock = Block.objects.latest('index')


    height = previousBlock.index

    return ("", str(height))