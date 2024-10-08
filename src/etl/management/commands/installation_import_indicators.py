from django.core.management.base import BaseCommand
from pathlib import Path
from indicator.models import Indicators
from institution.models import Institutions
import csv
from django.conf import settings
REL_PATH_INDICATORS = 'install/postgres/indicators.csv'

class Command(BaseCommand):
    help = """Import indicators from a CSV file into the Indicators model.
    Only used during installation of the application."""
    
    def handle(self, *args, **kwargs):
        csv_file = Path(settings.BASE_DIR.parent.resolve() / REL_PATH_INDICATORS)
        if not csv_file.exists():
            self.stderr.write(f"File {csv_file} not found.")
            return
        self.stdout.write(f'Importing indicators from {csv_file}...')
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"', skipinitialspace=True)
            next(reader)
            for row in reader:
                inst_instid,indicid,name,abbreviation,unit_measure,description = row
                institution_instance = Institutions.objects.get(instid=inst_instid)
                indicator_instance = Indicators.objects.create(inst_instid=institution_instance,
                                                                indicid=indicid,name=name,
                                                                abbreviation=abbreviation,unit_measure=unit_measure,
                                                                description=description)
                self.stdout.write(f"Indicator imported: {indicator_instance.indicid} published by {indicator_instance.inst_instid} imported.")
        self.stdout.write(self.style.SUCCESS('Indicators imported successfully!'))