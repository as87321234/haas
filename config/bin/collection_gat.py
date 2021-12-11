from bs4 import BeautifulSoup
import datetime
import requests
import json
from datetime import datetime, timedelta, date

now=datetime.now()
url = 'https://api.recollect.net/api/places/B7CACAE0-E7D7-11E8-98AA-1DCEB33ECFC0/services/798/events?nomerge=1&hide=reminder_only&after=%s-%s-%s&before=%s-12-31&locale=en&include_message=email&_=1638837219' % (
    now.year, now.month, now.day, int(now.year) + 1
)
bearer="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJmYzZmY2M4Y2M0MjY0MDZlODA0ZTkzYjE5MmI3MTVjNCIsImlhdCI6MTYzODg0ODc3MCwiZXhwIjoxOTU0MjA4NzcwfQ.ee0px9b4bnU1QTInWdtoSl4XYwaXiLtGYTyso8eP_QU"
# print(url)
page = requests.get(url)

if page.status_code != 200:
    exit(1)

soup = BeautifulSoup(page.text, 'html.parser')
site_json=json.loads(soup.text)

out = {}

for e in site_json["events"]:
    name=e['flags'][0]['name']
    name=name.replace("\"","").lower()
    date=e['day']
    date=date.replace("\"","")
    event_time=datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))

    if event_time > now :

        try:
            if out[name] >  date:
               out[name]=date
        except KeyError:
           out[name]=date


# Process collect events
for e in out:
    data='{"state":"%s","attributes":{"friendly_name":"sensor.collection_gatineau_%s","device_class":"timestamp"}}' %(out[e],e)

    req=requests.post('http://localhost:8123/api/states/sensor.collection_gatineau_%s' % e,
                  headers = {'authorization': bearer ,
                            'content-type': 'application/json'
                            },
                  data = data
                  )
    print(req.content)
    #print(json.dumps(out))

