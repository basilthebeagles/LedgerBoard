from django.core.management.base import BaseCommand, CommandError

from LedgerBoardApp.helperFunctions.addNewHosts import AddNewHosts

#call this something else

#used to manually add new node



class Command(BaseCommand):

    def add_arguments(self, parser):
        print('')
        parser.add_argument('selfHost', nargs='+', type=str)
        parser.add_argument('host', nargs='+', type=str)



    def handle(self, *args, **options):
        selfHost = ""

        for host in options['selfHost']:
            selfHost = host


        host = ""

        for hos in options['host']:
            host = hos

        print(str(AddNewHosts(host, 0.1, selfHost)))



