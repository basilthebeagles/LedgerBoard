from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.db import models
import time

from LedgerBoardApp.models import Node

#call this something else





class Command(BaseCommand):

    def add_arguments(self, parser):
        print('')

    def handle(self, *args, **options):

        currentTime = int(time.time())

        inactiveNodes = Node.objects.filter(secondsSinceLastInteraction__lt = (currentTime - 5400))

        inactiveNodes.all().delete()

        blackListNodes = Node.objects.filter(timeOfBlackList__gt= 0)



        for node in blackListNodes:
            if node.timeOfBlackList > currentTime + 259200:
                node.timeOfBlackList = 0
                node.save()








