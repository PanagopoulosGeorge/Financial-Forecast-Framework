import pandas as pd
import os
import sys
from django.conf import settings
from pathlib import Path

BASE_DIR = settings.BASE_DIR

class OECDTransformer:

    def __init__(self):
        self.DATA_DIR = Path(BASE_DIR / 'data' / 'oecd')
        self.file_path = Path(self.DATA_DIR / 'data.csv')
        self.last_historical_date_file = str(Path(BASE_DIR / 'data' / 'last_historical_date.txt'))
        self.last_historical_date = pd.to_datetime(open(self.last_historical_date_file).read().strip())
        self.DB_COLUMNS = ["inst_instid", "indic_indicid", "area_areaid", "value", "value_normalized", "date_from", "date_until", "date_published", "date_updated", "is_forecast"]
        self.column_mapping = {
            "REF_AREA": "area_areaid",
            "MEASURE": "indic_indicid",
            "OBS_VALUE": "value",
            "TIME_PERIOD": "date_from",
        }
        self.dtypes = { "REF_AREA": str,"MEASURE": str, "OBS_VALUE": float, "TIME_PERIOD": str}
        self.data = pd.DataFrame()
        self.institute = "OECD"
    
    def transform(self) -> bool:
        """
        Transfrom the data from the OECD data.csv file and saves data ready for loading.

        """
        success = True
        if not self.file_path.exists():
            return 1
        try:
            df_orig = pd.read_csv(self.file_path, dtype=self.dtypes)
        except Exception as e:
            print(f"Error reading file: {e}")
            return not success
        df = df_orig.copy()
        try:
            df = df.assign(
                TIME_PERIOD = pd.to_datetime(df["TIME_PERIOD"]),
                date_until = pd.to_datetime(df["TIME_PERIOD"]) + pd.DateOffset(months=3),
                date_published = self.last_historical_date,
                value_normalized=0,
                date_updated=pd.to_datetime("today"),
                inst_instid='OECD',
                is_forecast=None
            )
            df = df.rename(columns=self.column_mapping)
            df["is_forecast"] = df["date_from"].apply(self.update_forecast_status)
            self.data = df[self.DB_COLUMNS]
        except Exception as e:
            print(f"Error transforming data: {e}")
            return not success
        
        self.save_data()
        return success
        
    def save_data(self):
        self.data.to_csv(self.DATA_DIR / 'data_transformed.csv', index=False)

    def update_forecast_status(self, date=None):
        """ last_historical_date.txt file contains the last date for which we have actual historical recorded data.
            returns 1 or 0 if date is greater than the last historical date in the file.
        """
        return int(date >= self.last_historical_date)