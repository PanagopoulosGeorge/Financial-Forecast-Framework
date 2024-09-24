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
        with open(self.json_file_path, 'r') as f:
            text = f.read()
        jsondata = json.loads(text.replace('\'', '\"'))
        return jsondata
        
    def load_data(self):
        jsondata = self.load_json()
        data = pd.DataFrame(columns=self.DB_COLUMNS)
        for symbol in jsondata.keys():
            df = self.unpack_symbol(jsondata, symbol)
            data = pd.concat([data, df], ignore_index=True)
        return data

    def update_forecast_status(self, date=None):
        """ last_historical_date.txt file contains the last date for which we have actual historical recorded data.
            returns 1 or 0 if date is greater than the last historical date in the file.
        """
        return int(date[:4] >= self.last_historical_date[:4])

    def unpack_symbol(self, jsondata, symbol):
        result =[]
        data = jsondata[symbol]
        for area, values in data.items():
            for date, value in values.items():
                result.append({'inst_instid': 'IMF', 
                               'indic_indicid': symbol, 
                               'area_areaid': area, 
                               'value': value, 'value_normalized': None, 
                               'date_from': date, 'date_until': None, 'date_published': None, 'date_updated': None, 
                               'is_forecast': self.update_forecast_status(date)})
        return pd.DataFrame(result)
        

        
if __name__ == "__main__":
    ld = IMFDataLoader("data/IMF_data.json")
    df = ld.load_data()
    print(df[['inst_instid', "indic_indicid", "area_areaid", "date_from", "is_forecast"]].head())
    print(df.shape)
    print(df[['inst_instid', "indic_indicid", "area_areaid", "date_from", "is_forecast"]].tail())