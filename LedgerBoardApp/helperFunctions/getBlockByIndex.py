from LedgerBoardApp.models import Block


def getBlockByIndex(index):
    blockDataArray = []
    try:
        block = Block.objects.get(index=index)

        blockDataArray.append(block.index)
        blockDataArray.append(block.timeStamp)
        blockDataArray.append(block.previousBlockHash)
        blockDataArray.append(block.target)
        blockDataArray.append(block.nonce)

        return ("", blockDataArray)


    except:
         return ("Block does not exist.", [])

