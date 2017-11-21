#! /usr/bin/env python3

import requests, urllib, time

def get_weather ():
    url = 'http://api.wunderground.com/api/yourapikeyhere/forecast/lang:FI/q/FI/Jyvaskyla.json'
    r = requests.get(url)
    j = r.json()
    co = j['forecast']['txt_forecast']['forecastday']

    for x in range(0,1):
        text =co[x]['title']+'. '+co[x]['fcttext_metric'] # +co[1]['title']+'.'+co[1]['fcttext_metric'];

    print(text)
    return text



