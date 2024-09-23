# src/db_utils.py
## This script is used for main database utilities.
## Fills the area table
from src.config import load_config_db, get_connection_string
from src.OECD.countries import country_codes
from src.OECD.loader import OECDDataLoader
import psycopg2
import logging
from sqlalchemy import create_engine, text
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("DB_loader.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_indicator_symbols(inst_instid="OECD"):
    conn = connect_to_db()
    with conn.cursor() as cur:
        cur.execute("SELECT indicid FROM indicators WHERE inst_instid = %s", (inst_instid,))
        query_out = cur.fetchall()
        return [x[0] for x in query_out]

def get_areas():
    conn = connect_to_db()
    with conn.cursor() as cur:
        cur.execute("SELECT areaid FROM area")
        query_out = cur.fetchall()
        return [x[0] for x in query_out]

def connect_to_db():
    """Connect to the PostgreSQL database server."""
    conn = None
    try:
        params = load_config_db()
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error: {error}")
        if conn is not None:
            conn.close()
        return None

def get_sqlalchemy_engine():
    params = load_config_db()
    db_url = get_connection_string(params)
    engine = create_engine(db_url)
    return engine

def load_OECD_countries(country_codes = country_codes):
    conn = connect_to_db()
    with conn.cursor() as cur:
        for section in country_codes:
            for country_code, country_name in country_codes[section].items():
                cur.execute("SELECT 1 FROM area WHERE areaid = %s", (country_code,))
                if cur.fetchone() is None:
                    if section == "OECD_countries":
                        cur.execute("INSERT INTO area (areaid, name, description) VALUES (%s, %s, %s)", (country_code, country_name, "Country (OECD Member)"))
                    elif section == "Non_OECD_member_countries":
                        cur.execute("INSERT INTO area (areaid, name, description) VALUES (%s, %s, %s)", (country_code, country_name, "Country (Non-OECD Member)"))
                    else:
                        cur.execute("INSERT INTO area (areaid, name, description) VALUES (%s, %s, %s)", (country_code, country_name, "Country Grouping"))
            conn.commit()
    logging.info("loading finished.")
    logging.info("Closing connection to the PostgreSQL database.")
    conn.close()

def load_measures(data = "data/OECD_data.csv", engine = get_sqlalchemy_engine(), institute = 'OECD'):
    logger.info("  ############ Starting load_measures process  ############ ")
    logger.info("institute: " + institute)
    if institute =='OECD':
        loader = OECDDataLoader(data)
    data = loader.load_data()
    indicators = get_indicator_symbols('OECD')
    areas = get_areas()
    logger.info("Number of records before filtering: " + f"{len(data)}")
    with engine.connect() as conn:
        data = data[data["indic_indicid"].isin(indicators)]
        data = data[data["area_areaid"].isin(areas)]
        existing_forecasts = pd.read_sql("SELECT inst_instid,indic_indicid, area_areaid, date_from, date_until, is_forecast FROM publishes", conn)
        data['date_from'] = pd.to_datetime(data['date_from']).dt.date
        data['date_until'] = pd.to_datetime(data['date_until']).dt.date
        existing_forecasts['date_from'] = pd.to_datetime(existing_forecasts['date_from']).dt.date
        existing_forecasts['date_until'] = pd.to_datetime(existing_forecasts['date_until']).dt.date
        existing_forecasts['is_forecast']  = existing_forecasts['is_forecast'].astype(int)
        data = data.merge(existing_forecasts, on=['inst_instid', 'indic_indicid', 'area_areaid', 'date_from', 'date_until', 'is_forecast'], how='left', indicator=True)
        data = data[data['_merge']=='left_only'].drop(columns=['_merge'])
        rows = [tuple(row) for row in data.values]
        logging.info("Number of records after filtering: " + f"{len(rows)}")
    conn = connect_to_db()
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO publishes (inst_instid, indic_indicid, area_areaid, value, value_normalized, date_from, date_until, date_published, date_updated, is_forecast) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            rows
        )
        conn.commit()
    logger.info("Data insertion completed")
    logger.info("  ############ Ending load_measures process  ############ ")

if __name__ == '__main__':
    load_measures()