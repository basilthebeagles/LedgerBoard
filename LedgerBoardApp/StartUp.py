from django.db import models
import time

from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions import blockHelperFunctions
from LedgerBoardApp.models import Data

#call this something else




def StartUp():

    feedback = "-"
    firstBadBlockTimeObject = Data.objects.get(datumTitle="Time of First Bad Block After Chainable Block")




