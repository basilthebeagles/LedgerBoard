from django.core.management.base import BaseCommand, CommandError
from LedgerBoardApp.models import Block



class NewBLock(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        print('')

    def handle(self, *args, **options):
        print('')
#get all posts with no index. Add index. somehow hash them all along with other block data. Save block hash and add to new block.
#basically get highest block index. Add timestamp. save. hash. Create new block with hash.