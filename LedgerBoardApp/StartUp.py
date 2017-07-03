from django.db import models
import time

from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions import blockHelperFunctions

#call this something else




def startUp():

    feedback = "-"

    while feedback != "":

        feedback = blockHelperFunctions.badChainFixer()

