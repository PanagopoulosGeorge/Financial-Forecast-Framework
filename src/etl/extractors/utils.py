from datetime import datetime
import requests
def write_last_historical_date(endpoint, out_file) -> bool:
    url = endpoint
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,el;q=0.8",
        "content-type": "application/json",
        "origin": "https://data-explorer.oecd.org",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    payload = {
      "lang": "en",
      "search": "",
      "sort": "score desc, sname asc, indexationDate desc",
      "facets": {
        "Topic": [
          "1|Economy#ECO#|Economic outlook#ECO_OUT#"
        ],
        "datasourceId": [
          "dsDisseminateFinalDMZ",
          "dsDisseminateFinalCloud"
        ]
      },
      "rows": 20,
      "start": 0
    }
    try:
      response = requests.post(url, headers=headers, json=payload)
      response.raise_for_status()
      data = response.json()
      last_updated_date = str(data['dataflows'][-1]['lastUpdated']).split('T')[0]
      print(f"Last historical date: {last_updated_date}")
    
      with open(out_file, 'w') as f:
          f.write(last_updated_date)
      return True
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed with status code {response.status_code}")
        