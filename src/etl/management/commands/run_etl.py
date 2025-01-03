from django.core.management.base import BaseCommand, CommandError
from .include.oecd import OECDClient
from .include.imf import IMFClient
from .include.philadephia import PhiladelphiaClient
from .include.ecb import ECBClient


class Command(BaseCommand):
    help = 'Run ETL process for each data source'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str,
                            help='Mode to run the ETL process (t, e, l, etl for full process)')
        parser.add_argument('--source', type=str,
                            help='Run ETL process for a specific source')
        
    def handle(self, *args, **kwargs):
        mode = kwargs['mode']
        source = kwargs['source']
        if mode not in ['t', 'e', 'l', 'etl']:
            raise CommandError("Invalid mode. Use 't', 'e', 'l', or 'etl'")
        if source not in ('oecd', 'imf', 'philadelphia', 'ecb'):
            raise CommandError("Invalid source. Use 'oecd' or 'imf' or 'philadelphia' or 'ecb'")
        with open('year.txt', 'r') as f:
            year = f.read()
        with open('quarter.txt', 'r') as f:
            quarter = f.read()
        if source == 'oecd':
            print("Running ETL for OECD")
            oecd_client = OECDClient(mode)
            oecd_client.run()
        elif source == 'imf':
            print("Running ETL for IMF")
            imf_client = IMFClient(mode)
            imf_client.run()
        elif source == 'philadelphia':
            print("Running ETL for Philadelphia")
            url = f'https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/spf-q{quarter}-{year}'
            philly_client = PhiladelphiaClient(url, mode)
            philly_client.run()

        elif source == 'ecb':
            print("Running ETL for ECB")
            url = f'https://www.ecb.europa.eu/stats/ecb_surveys/survey_of_professional_forecasters/html/table_3_{year}q{quarter}.en.html'
            ecb_client = ECBClient(url, mode)
            ecb_client.run()
        else:
            raise CommandError("Source does not exist")
        