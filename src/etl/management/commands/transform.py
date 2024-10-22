from django.core.management.base import BaseCommand
from etl.transformers import OECDTransformer, IMFTransformer
import logging

class Command(BaseCommand):
    help = """Transforms Data from every source for unified loading into the database."""

    def setup_logger(self):
        return logging.getLogger('etl')

    def transform_and_log(self, transformer):
        self.stdout.write(f"Transforming publications from institute {transformer.institute}")
        success = transformer.transform()
        if success:
            self.stdout.write(self.style.SUCCESS(f'Publications transformed to {transformer.file_path}'))
            self.logger.info(self.style.SUCCESS(f'Publications transformed to {transformer.file_path}'))
        else:
            self.stdout.write(self.style.ERROR('Data transformation failed.'))
            self.logger.error(self.style.ERROR('Data transformation failed.'))

    def handle(self, *args, **kwargs):
        self.logger = self.setup_logger()

        oecd_transformer = OECDTransformer(frequency='A')
        self.transform_and_log(oecd_transformer)

        oecd_transformer = OECDTransformer(frequency='Q')
        self.transform_and_log(oecd_transformer)

        imf_transformer = IMFTransformer()
        self.transform_and_log(imf_transformer)
        
