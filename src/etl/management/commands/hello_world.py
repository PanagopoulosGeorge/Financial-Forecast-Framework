from django.core.management.base import BaseCommand
from etl import download_local, ETL_ROOT
from pathlib import Path

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Hello, World!')
        print(ETL_ROOT)