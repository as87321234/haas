#
''' COLLECTION GATINEAU '''
import sys
from datetime import datetime

import json
import requests

from bs4 import BeautifulSoup

CURRENT_TIME: datetime = datetime.now()
YEAR_INT = str(int(CURRENT_TIME.year) + 2)

URL = f'https://api.recollect.net/api/places/B8CACAE0-E7D7-11E8-98AA-1DCEB33ECFC0/services/' \
      f'798/events?nomerge=1&hide=reminder_only&after=' \
      f'{CURRENT_TIME.year}-{CURRENT_TIME.month}-{CURRENT_TIME.day}&before={YEAR_INT}-01-01' \
      f'&locale=en&include_message=email&_=1638837220'

URL = 'https://api.recollect.net/api/places/B7CACAE0-E7D7-11E8-98AA-1DCEB33ECFC0/services/798/events?nomerge=1&hide=reminder_only&after=%s-%s-%s&before=%s-12-31&locale=en&include_message=email&_=1638837219' % (
    '2021', '12', '10', int('2021') + 1
)
print(URL)

BEARER = "bearer eyJ1eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJmYzZmY2M4Y2M0MjY0MDZlODA0Z" \
         "TkzYjE5MmI3MTVjNCIsImlhdCI6MTYzODg0ODc3MCwiZXhwIjoxOTU0MjA4NzcwfQ.ee0px9b4bnU1QTInWdto" \
         "Sl4XYwaXiLtGYTyso8eP_QU"

BEARER="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJmYzZmY2M4Y2M0MjY0MDZlODA0ZTkzYjE5MmI3MTVjNCIsImlhdCI6MTYzODg0ODc3MCwiZXhwIjoxOTU0MjA4NzcwfQ.ee0px9b4bnU1QTInWdtoSl4XYwaXiLtGYTyso8eP_QU"

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


# Process collect events
for e in out:
    PAYLOAD = "{\"state\":\"{out[e]}\",\"attributes\":{\"friendly_name\":\"" \
        "sensor.collection_gatineau_{e}\",\"device_class\":\"timestamp\"}}"

    req = requests.post(
        "https://has.pointtomap.com/api/states/sensor.collection_gatineau_{e}",
            headers={'authorization': BEARER,
                        'content-type': 'application/json'
                        },
            data=PAYLOAD
            )
    # print(req.content)
print(json.dumps(out))
