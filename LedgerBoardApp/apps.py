from django.apps import AppConfig
from LedgerBoardApp.StartUp import startUp

class LedgerBoardAppConfig(AppConfig):

    name = 'LedgerBoardApp'

    startUp()
