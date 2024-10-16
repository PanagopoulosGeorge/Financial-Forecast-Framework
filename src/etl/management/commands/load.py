from io import StringIO
import os
from etl.loader.loader import DataLoader
from django.core.management.base import BaseCommand
from pathlib import Path
import logging
DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent.resolve() / 'data'
class Command(BaseCommand):
    help = 'Load CSV files from the data directory into the database'

    def setup_logger(self):
        return logging.getLogger('etl')
    
    def __init__(self) -> None:
        super().__init__()
        
        self.FILENAME_FOR_LOADING = 'data_transformed.csv'
    
    def data_for_import_exist(self, path: Path) -> bool:
        return path.exists() and path.is_file()

    def handle(self, *args, **kwargs):
        self.logger = self.setup_logger()
        data_sources = {
                        f.name.upper(): f / self.FILENAME_FOR_LOADING
                        for f in DATA_DIR.iterdir() if f.is_dir()}
        print(data_sources)
        for institution in data_sources:
            self.logger.info(f"Loading data for {institution}")
            if self.data_for_import_exist(data_sources[institution]):
                loader = DataLoader(data_sources[institution], institution)
                loaded = loader.load()
                if loaded:
                    os.remove(data_sources[institution])
                    self.logger.info(f"Deleted file for {institution}")
            else:
                self.logger.info(f"File not found for {institution}")
            