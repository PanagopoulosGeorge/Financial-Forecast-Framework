import requests 
import sys
from datetime import datetime
from src.IMF.urls import IMF_BASE_ENDPOINT
from src.IMF.IMF_download import fetch_imf_data
import pandas as pd
from src.DB_loader import get_sqlalchemy_engine

def convert_to_dataframe(data):
    rows = []
    for indicator_id, details in data.items():
        row = {'indicator_id': indicator_id}
        row.update(details)
        rows.append(row)
    df = pd.DataFrame(rows)
    return df

def load_indicators():
    indicators = pd.read_csv('src/IMF/IMF_indicators.csv')
    return indicators

def load_countries():
    countries = pd.read_csv('src/IMF/countries.csv')
    return countries

def append_countries_to_db():
    data = load_countries()
    engine = get_sqlalchemy_engine()
    area_ids = pd.read_sql('select areaid from area', con=engine)
    data = data[~data['areaid'].isin(area_ids['areaid'])]
    data.dropna(subset=['areaid', 'name'], inplace=True)
    data.to_sql('area', con=engine, if_exists='append', index=False)

def append_indicators_to_db():
    data = load_indicators()
    engine = get_sqlalchemy_engine()
    data.to_sql('indicators', con=engine, if_exists='append', index=False)


if __name__ == "__main__":
    append_countries_to_db()
