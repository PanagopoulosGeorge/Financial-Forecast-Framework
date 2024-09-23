import pandas as pd
import os
import sys

class OECDDataLoader:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.DB_COLUMNS = ["inst_instid", "indic_indicid", "area_areaid", "value", "value_normalized", "date_from", "date_until", "date_published", "date_updated", "is_forecast"]
        self.column_mapping = {
            "REF_AREA": "area_areaid",
            "MEASURE": "indic_indicid",
            "OBS_VALUE": "value",
            "TIME_PERIOD": "date_from",
        }
        self.dtypes = { "REF_AREA": str,"MEASURE": str, "OBS_VALUE": float, "TIME_PERIOD": str}
        self.data = pd.DataFrame()
        self.last_historical_date = open("last_historical_date.txt").read().strip()

    def load_data(self):
        if not os.path.exists(self.csv_file_path):
            print("No CSV file path provided")
            sys.exit(1)
        
        data = pd.read_csv(self.csv_file_path, dtype=self.dtypes)
        data = data.assign(
            date_until = pd.to_datetime(data["TIME_PERIOD"]) + pd.DateOffset(months=3),
            date_published=None,
            value_normalized=None,
            date_updated=pd.to_datetime("today"),
            inst_instid='OECD',
            is_forecast=None
        )
        data = data.rename(columns=self.column_mapping)
        data["is_forecast"] = data["date_from"].apply(self.update_forecast_status)
        data["date_from"] = data["date_from"].apply(self.convert_quarter_to_date)
        return data[self.DB_COLUMNS]

    def convert_quarter_to_date(self, quarter_str):
        year, quarter = quarter_str.split('-Q')
        quarter_start_month = {
            '1': '01',
            '2': '04',
            '3': '07',
            '4': '10'
        }
        month = quarter_start_month[quarter]
        return f"{year}-{month}-01"

    def update_forecast_status(self, date=None):
        """ last_historical_date.txt file contains the last date for which we have actual historical recorded data.
            returns 1 or 0 if date is greater than the last historical date in the file.
        """
        return int(date >= self.last_historical_date)

if __name__ == "__main__":
    ld = OECDDataLoader("data/OECD_data.csv")
    df = ld.load_data()
    print(df[df['is_forecast'] != 0].head())