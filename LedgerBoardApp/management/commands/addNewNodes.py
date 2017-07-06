from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.db import models
import time
import requests
from LedgerBoardApp.models import Node
from LedgerBoardApp.helperFunctions.nodeHelperFunctions import NewNode


class Command(BaseCommand):

    def add_arguments(self, parser):
        print('')




    def handle(self, *args, **options):

        currentTime = int(time.time())
        for arg in args:
            try:
                host, version, currentIP = arg.split('.')

                url = str(host) + "/handShake/"
                payload = {
                    'host': currentIP,
                    'vers': '0.1',
                    'currentTime': str(currentTime),

                }

                r = requests.post(url, data=payload, timeout=1)
                if r.content == "Connection created.":

                    feedback = NewNode(host, version)
                    if feedback == "":
                        print('success')
                    else:
                        print('fail')
                else:
                    print('fail')
            except ValueError:
                print('fail')






            # defaultStatus = rawPostData.__getitem__('defaultStatus')














