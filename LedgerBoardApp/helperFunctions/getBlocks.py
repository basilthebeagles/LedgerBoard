from LedgerBoardApp.models import Block
import ast

def getBlocks(attribute, attributeParameter):

    parameter = ast.literal_eval(str(attributeParameter))




    blockArray = []

    flaggedBlocks = ''


    try:

        if attribute == 'index':
            flaggedBlocks = Block.objects.filter(index__gt=(parameter[0]), index__lt=(parameter[1]) )

        elif attribute == 'timeStamp':
            flaggedBlocks = Block.objects.filter(timeStamp__gt=(parameter[0]), timeStamp__lt=(parameter[1]) )


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

