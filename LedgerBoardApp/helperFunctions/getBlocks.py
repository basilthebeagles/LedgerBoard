from LedgerBoardApp.models import Block
import ast

def GetBlocks(attribute, attributeParameters):

    parameters = ast.literal_eval(str(attributeParameters))




    blockArray = []

    flaggedBlocks = ''


    try:

        if attribute == 'index':
            flaggedBlocks = Block.objects.filter(index__gte=(parameters[0]), index__lte=(parameters[1]) )
            flaggedBlocks.order_by('index')

        elif attribute == 'timeStamp':
            flaggedBlocks = Block.objects.filter(timeStamp__gte=(parameters[0]), timeStamp__lte=(parameters[1]) )
            flaggedBlocks.order_by('timeStamp')




        for block in flaggedBlocks:
            blockDataArray = []

            blockDataArray.append(block.index)
            blockDataArray.append(block.timeStamp)
            blockDataArray.append(block.previousBlockHash)
            blockDataArray.append(block.target)
            blockDataArray.append(block.nonce)

            blockArray.append(blockDataArray)

        return ("", blockArray)


    except:
         return ("Block does not exist.", [])

