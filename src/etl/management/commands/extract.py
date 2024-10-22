from django.core.management.base import BaseCommand
from etl.extractors import OECDExtractor, IMFExtractor
import logging

class Command(BaseCommand):
    help = """Download all publications for every institution."""

    def setup_logger(self):
        return logging.getLogger('etl')

    def extract_and_log(self, extractor):
        self.stdout.write(f"Extracting publications from endpoint {extractor.BASE_URL}")
        self.logger.info(f"Extracting publications from endpoint {extractor.BASE_URL}")
        success = extractor.extract_publications()

        if success is None:
            self.stdout.write(self.style.SUCCESS('Data is up to date.'))
            self.logger.info(f'Data for institution is up to date.')
            return True
        
        if success:
            self.stdout.write(self.style.SUCCESS(f'Publications downloaded to {extractor.FULL_DATA_PATH}'))
            self.logger.info(f'Publications downloaded to {extractor.FULL_DATA_PATH}')
        else:
            self.stdout.write(self.style.ERROR('Data extraction or saving failed.'))
            self.logger.error('Data extraction or saving failed.')

    def handle(self, *args, **kwargs):
        self.logger = self.setup_logger()
    
        oecd_extractor = OECDExtractor(country_code="all", indicator="all", frequency="Q", data_download="2010")
        self.extract_and_log(oecd_extractor)

        oecd_extractor = OECDExtractor(country_code="all", indicator="all", frequency="A", data_download="2010")
        self.extract_and_log(oecd_extractor)

        imf_extractor = IMFExtractor()
        self.extract_and_log(imf_extractor)
