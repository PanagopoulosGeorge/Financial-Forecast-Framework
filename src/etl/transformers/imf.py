import pandas as pd
import os
import sys
from django.conf import settings
from pathlib import Path
import json
BASE_DIR = settings.BASE_DIR

class IMFTransformer:

    def __init__(self):
        self.DATA_DIR = Path(BASE_DIR / 'data' / 'imf')
        self.file_path = Path(self.DATA_DIR / 'data.json')
        self.last_historical_date_file = str(Path(BASE_DIR / 'data' / 'last_historical_date.txt'))
        self.last_historical_date = pd.to_datetime(open(self.last_historical_date_file).read().strip())
        self.DB_COLUMNS = ["inst_instid", "indic_indicid", "area_areaid", "value", "value_normalized", "date_from", "date_until", "date_published", "date_updated", "is_forecast"]
        self.institute = "IMF"
        self.data = pd.DataFrame()

    def save_data(self):
        self.data.to_csv(self.DATA_DIR / 'data_transformed.csv', index=False)

    def load_json(self):
        if not os.path.exists(self.file_path):
            print("No json file path provided")
            sys.exit(1)
        with open(self.file_path, 'r') as f:
            text = f.read()
        jsondata = json.loads(text.replace('\'', '\"'))
        return jsondata
    
    def transform(self) -> bool:
        success = True
        jsondata = self.load_json()
        try:
            data = pd.DataFrame(columns=self.DB_COLUMNS)
            for symbol in jsondata.keys():
                try:
                    df = self.unpack_symbol(jsondata, symbol)
                except Exception as e:
                    print(f"Error unpacking symbol: {e}")
                    return not success
                data = pd.concat([data, df], ignore_index=True)
            data["date_from"] = pd.to_datetime(data["date_from"])            

            data = data.assign(
                date_until = data["date_from"] + pd.DateOffset(months=12),
                date_updated = pd.to_datetime("now"),
                date_published = pd.to_datetime(str(self.last_historical_date.year)+'-01-01'),
            )
            
            self.data = data.reset_index(drop=True)
            self.save_data()
            return success
        except Exception as e:
            print(f"Error transforming data: {e}")
            return not success

    def update_forecast_status(self, date) -> int:
        """ 
            last_historical_date.txt file contains the last date for which we have actual historical recorded data.
            returns 1 or 0 if date is greater than the last historical date in the file.
        """
        last_historical_date = pd.to_datetime(self.last_historical_date)
        return int(date.year >= last_historical_date.year)

    def unpack_symbol(self, jsondata, symbol):
        result =[]
        data = jsondata[symbol]
        for area, values in data.items():
            for date, value in values.items():
                date_from = pd.to_datetime(date)
                result.append({'inst_instid': 'IMF', 
                                'indic_indicid': symbol, 
                                'area_areaid': area, 
                                'value': value, 'value_normalized': 0, 
                                'date_from': date, 'date_until': None, 'date_published': None, 'date_updated': None, 
                                'is_forecast': self.update_forecast_status(pd.to_datetime(date))})
        return pd.DataFrame(result)