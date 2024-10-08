from .base import Extractor
from institution.models import Institutions
from django.conf import settings
from pathlib import Path
import requests
from .utils import *

OECD_ENDPOINT  = settings.ENDPOINTS['OECD']
OECD_BASE_ENDPOINT = OECD_ENDPOINT['publications']
OECD_HISTORICAL_ENDPOINT = OECD_ENDPOINT['historical_points']
BASE_PATH = settings.BASE_DIR
TIMEOUT = 120
HEADERS = {'Accept': 'application/vnd.sdmx.data+csv; charset=utf-8; version=2'}

class OECDExtractor(Extractor):

    def __init__(self, country_code = "all", indicator= "all", frequency= "A", data_download="full"):
        self.country_code = "" if country_code == 'all' else country_code.upper()
        self.indicator = "" if indicator == 'all' else indicator.upper()
        self.frequency = frequency
        self.data_download = data_download
        self.headers = HEADERS
        self.params = {} if data_download == 'full' else {'startPeriod': data_download}
        self.BASE_URL = f"{OECD_BASE_ENDPOINT}/{self.country_code}.{self.indicator}.{self.frequency}"
        self.OECD_HISTORICAL_ENDPOINT = OECD_HISTORICAL_ENDPOINT
        self.ROOT_DATA_DIR = BASE_PATH / 'data'
        self.DATA_DIR = self.ROOT_DATA_DIR / 'oecd'
        self.FULL_DATA_PATH = Path(self.DATA_DIR / 'data.csv')
        self.TIMEOUT = TIMEOUT
        self.last_historical_date = Path(self.ROOT_DATA_DIR / 'last_historical_date.txt')

    def last_historical_date_extracted(self) -> bool:
        return write_last_historical_date(self.OECD_HISTORICAL_ENDPOINT, self.last_historical_date)
    
    def extract_publications(self) -> bool:
        self.FULL_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        is_historical_date_extracted = self.last_historical_date_extracted()
        if is_historical_date_extracted:
            try:
                response = requests.get(self.BASE_URL, 
                                        allow_redirects=True, 
                                        params=self.params, 
                                        headers=self.headers,
                                        timeout=self.TIMEOUT)
                response.raise_for_status()

                with open(self.FULL_DATA_PATH, "wb") as f:
                    data = response.content
                    f.write(data)
                return True
            except requests.exceptions.RequestException as e:
                raise RequestException(f"Request failed with error: {e}")

            except Exception as e:
                raise Exception(f"Failed to save data with error: {e}")
        else:
            raise Exception("Failed to extract last historical date.")
            
    