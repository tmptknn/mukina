#! /usr/bin/env python3

import requests, urllib, time

def get_bitcoin ():
    url = 'https://blockchain.info/fi/ticker'
    r = requests.get(url)
    j = r.json()
    priceeur = j['EUR']

    text = "BITCOIN "+str(priceeur['last'])+" "+priceeur['symbol']

    print(text)
    return text

#get_bitcoin()


