import requests
import sys
from .urls import IMF_BASE_ENDPOINT
from datetime import datetime
from src.database import get_indicator_symbols
HELP ="""
This script is used to access the IMF API and download data from the IMF Economic outlook.

It checks all the available indicators in indicators and creates an endpoint for each symbol
to download the data.
    

"""
"""

API Documentation: https://www.imf.org/external/datamapper/api/help

Ex. https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH?periods=2019,2020  - retrieve Real GDP Growth values for 2019 and 2020.

"""
def fetch_imf_data(endpoint, params=None):
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == "__main__":
    IMF_indicators = get_indicator_symbols("IMF")
    data = {}
    for indicator in IMF_indicators:
        endpoint = IMF_BASE_ENDPOINT + indicator 
        indicator_data = fetch_imf_data(endpoint)
        indicator_data = indicator_data['values']
        data = {**data, **indicator_data}
    with open("data/IMF_data.json", "w") as f:
        text = str(data)
        f.write(text)