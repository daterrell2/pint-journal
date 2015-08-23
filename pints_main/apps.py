from django.apps import AppConfig
from utils.brewerydb import BreweryDb
from pint_journal_project import dev_settings

class PintsMainConfig(AppConfig):
    name = 'pints_main'
    verbose_name = "pints_main"
    def ready(self):
        '''
        Configures BreweryDb API wrapper with API key.
        '''
        key = dev_settings.BREWERYDB_KEY
        BreweryDb.configure(key)
        