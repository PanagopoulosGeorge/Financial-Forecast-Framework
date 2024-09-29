import requests 
import sys
import pandas as pd
from src.DB_loader import get_sqlalchemy_engine

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
