from .base import Extractor
from institution.models import Institutions
from django.conf import settings
from pathlib import Path
from indicator.models import Indicators
from institution.models import Institutions
from publication.models import Publishes
import requests
import json
import datetime
IMF_ENDPOINT  = settings.ENDPOINTS['IMF']
IMF_BASE_ENDPOINT = IMF_ENDPOINT['publications']
BASE_PATH = settings.BASE_DIR

class IMFExtractor(Extractor):

    def __init__(self, base_url=IMF_BASE_ENDPOINT, data_dir=BASE_PATH / 'data' / 'imf'):
        self.BASE_URL = base_url
        self.DATA_DIR = data_dir
        self.ROOT_DATA_DIR = BASE_PATH / 'data'
        self.FULL_DATA_PATH = Path(self.DATA_DIR / 'data.json')
        self.data = {}
        self.last_historical_date = Path(self.ROOT_DATA_DIR / 'last_historical_date.txt')
        if not self.DATA_DIR.exists():
            self.DATA_DIR.mkdir(parents=True)

    def _fetch_imf_data(self, endpoint, params=None) -> dict:
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch data from {endpoint}: {e}")
            raise RuntimeError(f"Failed to fetch data from {endpoint}")
            
    def save_data(self):
        """Saves data to a JSON file."""
        try:
            with open(self.FULL_DATA_PATH, "w") as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            self.logger.error(f"Failed to save data to {self.FULL_DATA_PATH}: {e}")
            raise RuntimeError(f"Failed to save data to {self.FULL_DATA_PATH}: {e}")
    
    def is_up_to_date(self) -> bool:
        try:
            last_published_year = self.date_to_year(Publishes.objects.filter(inst_instid='IMF').latest('date_published').date_published)
            with open(self.last_historical_date, 'r') as file:
                last_historical_year = file.read().strip()[:4]
            return last_published_year == last_historical_year
        except Publishes.DoesNotExist:
            return False
        except Exception as e:
            raise Exception(f"Error checking if data is up to date: {e}")
    
    def date_to_year(self, date: datetime.date) -> str:
        return str(date.year)
    
    def extract_publications(self) ->bool:
        success = True
        imf_institution = Institutions.objects.get(instid="IMF")
        existing_indicators = Indicators.objects.filter(inst_instid=imf_institution)
        if not self.DATA_DIR.exists():
            self.DATA_DIR.mkdir(parents=True)
        
        symbols = [indicator.indicid for indicator in existing_indicators]
        if len(symbols) == 0:
            self.logger.warning("No indicators found for IMF institution.")
            return success
        
        if self.is_up_to_date():
            print("Data is up to date.")
            return None
        
        for indicator in symbols:
            endpoint = self.BASE_URL + indicator
            indicator_data = self._fetch_imf_data(endpoint)
            if indicator_data == 1000:
                return not success
            
            indicator_data = indicator_data['values']
            self.data = {**self.data, **indicator_data}
        self.save_data()
        return success
