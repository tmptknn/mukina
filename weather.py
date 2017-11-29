#! /usr/bin/env python3

import requests, urllib, time

def get_weather ():
    url = 'http://api.wunderground.com/api/yourapikeyhere/forecast/lang:FI/q/FI/Jyvaskyla.json'
    r = requests.get(url)
    j = r.json()
    #print(j)
    co = j['forecast']['txt_forecast']['forecastday']

    #for x in range(0,1):
    text =co[0]['title']+'. '+co[0]['fcttext_metric'] # +co[1]['title']+'.'+co[1]['fcttext_metric'];
    icon = co[0]['icon_url']
    print(icon)
    print(text)
    return text, icon



#get_weather()
