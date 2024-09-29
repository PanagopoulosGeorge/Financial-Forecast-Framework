import requests
import sys
from .urls import OECD_BASE_ENDPOINT
from .download_historical_points import write_last_historical_date
from datetime import datetime
HELP ="""
This script is used to access the OECD API and download data from the OECD Economic outlook database.

parameters:
    - country_code: str (3-letter country code) or 'all' to download data for all countries
    - indicator: str (indicator code) or 'all' to download all indicators
    - frequency: str (frequency code) 'A' for annual, 'Q' for quarterly.
    - data download: str (data download code) 'full' for full data download, 
                     or one of the following to specify the start date of the data download:
        Examples:
            • ‘2015’
            • ‘2015-A1’
            • ‘2015-S1’
            • ‘2015-Q1’
            • ‘2015-M01’
            • ‘2015-01’
            • ‘2015-01-01’
            • ‘2015-01-01T00:00:00’
    

"""
"""
url: https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CEconomy%23ECO%23%7CEconomic%20outlook%23ECO_OUT%23&pg=0&fc=Topic&bp=true&snb=2&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_EO%40DF_EO&df[ag]=OECD.ECO.MAD&df[vs]=1.1&dq=..A&to[TIME_PERIOD]=false&pd=%2C

API Documentation: https://gitlab.algobank.oecd.org/public-documentation/dotstat-migration/-/raw/main/OECD_Data_API_documentation.pdf

Example API request: url="https://sdmx.oecd.org/public/rest/data/OECD.ECO.MAD,DSD_EO@DF_EO,1.1/BEL..A"

All available indicators for BEL (Belgium) counted in annual frequency (A).

"""
BASE_URL = OECD_BASE_ENDPOINT

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(HELP)
        print("Usage: python OECD_API.py <country_code> <INDICATOR> <FREQUENCY> <DATA_DOWNLOAD>")
        sys.exit(1)
    country_code = sys.argv[1]
    indicator = sys.argv[2]
    frequency = sys.argv[3]
    data_download = sys.argv[4]
    country_code = "" if country_code == 'all' else country_code.upper()
    indicator = "" if indicator == 'all' else indicator.upper()
    params = {} if data_download == 'full' else {'startPeriod': data_download}
    write_last_historical_date()
    BASE_URL = OECD_BASE_ENDPOINT
    print(BASE_URL)
    
    url = f"{BASE_URL}/{country_code}.{indicator}.{frequency}"
    print("get response from url: " + url)

    response = requests.get(url, allow_redirects=True, 
                        params=params, 
                        headers={'Accept': 'application/vnd.sdmx.data+csv; charset=utf-8; version=2'})
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        sys.exit(1)
    with open("data/OECD_data.csv", "wb") as f:
        data = response.content
        f.write(data)