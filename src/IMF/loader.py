import pandas as pd
import os
import sys
import json

class IMFDataLoader:

    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.DB_COLUMNS = ["inst_instid", "indic_indicid", "area_areaid", "value", "value_normalized", "date_from", "date_until", "date_published", "date_updated", "is_forecast"]
        self.last_historical_date = open("last_historical_date.txt").read().strip()

    def load_json(self):
        if not os.path.exists(self.json_file_path):
            print("No json file path provided")
            sys.exit(1)
        with open(json_file_path, 'r') as f:
            text = f.read()
        jsondata = json.loads(text.replace('\'', '\"'))
        return jsondata
        
    def load_data():
        pass
    def update_forecast_status(self, date=None):
        """ last_historical_date.txt file contains the last date for which we have actual historical recorded data.
            returns 1 or 0 if date is greater than the last historical date in the file.
        """
        return int(date[:4] >= self.last_historical_date[:4])

if __name__ == "__main__":
    ld = OECDDataLoader("data/OECD_data.csv")
    df = ld.load_data()
    print(df[df['is_forecast'] != 0].head())