from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.db import models
import time

from LedgerBoardApp.models import Node




class Command(BaseCommand):

    def add_arguments(self, parser):
        print('')

    def handle(self, *args, **options):

        currentTime = int(time.time())

        inactiveNodes = Node.objects.filter(secondsSinceLastInteraction__lt = (currentTime - 5400))

        inactiveNodes.all().delete()









