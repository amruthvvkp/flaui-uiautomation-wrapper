import os
from testplan.testing.multitest.driver import Driver
from loguru import logger


class BankSystemDriver(Driver):

    def __init__(self, **options):
        super().__init__(**options)
        self.application_path = os.environ.get('BANK_SYSTEM_EXE_PATH', None)
        self.application_process_name = 'BankSystem.exe'

    def starting(self):
        assert self.application_path is not None
        logger.debug('Starting BankSystem application drivers')

    def stopping(self):
        logger.debug('Stopping BankSystem application drivers')