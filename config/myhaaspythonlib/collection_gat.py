''' COLLECTION GATINEAU '''

import sys
from datetime import datetime

import json
import requests

from bs4 import BeautifulSoup

from utility_lib import UtilityLib

CURRENT_TIME: datetime = datetime.now()
YEAR_INT = str(int(CURRENT_TIME.year) + 2)
YEAR_START=str(CURRENT_TIME.year - 1)

URL = f'https://api.recollect.net/api/places/B7CACAE0-E7D7-11E8-98AA-1DCEB33ECFC0/services/' \
      f'798/events?nomerge=1&hide=reminder_only&after=' \
      f'{YEAR_START}-{CURRENT_TIME.month}-{CURRENT_TIME.day}&before={YEAR_INT}-01-01' \
      f'&locale=en&include_message=email&_=1638837220'

PAGE = requests.get(URL)

if PAGE.status_code != 200:
    sys.exit(0)

SOUP = BeautifulSoup(PAGE.text, 'html.parser')
site_json = json.loads(SOUP.text)

# print(json.dumps(site_json,  indent=2))

out = {}

for e in site_json["events"]:

    name = e['flags'][0]['name']
    name = name.replace("\"", "").lower()
    a_date = e['day']
    a_date = a_date.replace("\"", "")
    event_time = datetime(
        int(a_date.split('-')[0]), int(a_date.split('-')[1]), int(a_date.split('-')[2]))

    if event_time > datetime.now():

        try:
            if out[name] > a_date:
                out[name] = a_date
        except KeyError:
            out[name] = a_date

BEARER = UtilityLib.get_secret_password('rest_api_bearer')

# Process collect events
for e, value in out.items():

    a_state = e

    PAYLOAD = '{"state":"##",' \
              '"attributes": { "friendly_name": "collection_gatineau_#",' \
              '"device_class":"timestamp" } }'
    PAYLOAD = PAYLOAD.replace("##", value)
    PAYLOAD = PAYLOAD.replace("#", e)

    URL = f"http://10.0.0.248:8123/api/states/sensor.collection_gatineau_{e}"

    headers = {}
    headers["Accept"] = "*/*"
    headers["authorization"] = BEARER
    headers["content-type"] = 'application/json;charset=UTF-8'
    headers["host"] = "10.0.0.248:8123"
    headers["Origin"] = "10.0.0.248:8123"
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
                            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0" \
                            ".4664.93 Safari/537.36"

    #print(URL)
    #print(json.dumps(headers, indent=2))
    #print(json.dumps(PAYLOAD, indent=2))
    req = requests.post(URL, headers=headers, data= PAYLOAD  )
    #print(req.content)

print(json.dumps(out))
