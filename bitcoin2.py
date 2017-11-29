#! /usr/bin/env python3

import requests, urllib, time, json
from datetime import date, time, timedelta, datetime
from wand.color import Color
from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing

def get_bitcoin ():
    today = date.today()
    weekago = today - timedelta(days=7)
    currenthour = datetime.utcnow().hour
    #url = 'https://blockchain.info/fi/ticker'
    urlexts ='&start=' + str(weekago.year) + '-' + str(weekago.month) + '-' + str(weekago.day) + \
        '&end=' + str(today.year) + '-' + str(today.month) + '-' + str(today.day)

    print(urlexts)
    url = 'https://api.coindesk.com/v1/bpi/historical/close.json?currency=EUR'+urlexts
    currenturl = 'https://api.coindesk.com/v1/bpi/currentprice/eur.json'

    r = requests.get(url)
    j = r.json()

    r2 = requests.get(currenturl)
    j2 = r2.json()
    #j =json.loads('{"bpi":{"2017-11-21":6898.976,"2017-11-22":6964.1453,"2017-11-23":6753.0209,"2017-11-24":6873.8498,"2017-11-25":7344.8844,"2017-11-26":7814.2358,"2017-11-27":8184.1759},"disclaimer":"This data was produced from the CoinDesk Bitcoin Price Index. BPI value data returned as EUR.","time":{"updated":"Nov 28, 2017 04:00:40 UTC","updatedISO":"2017-11-28T04:00:40+00:00"}}')

    #j2 = json.loads('{"time":{"updated":"Nov 28, 2017 04:05:00 UTC","updatedISO":"2017-11-28T04:05:00+00:00","updateduk":"Nov 28, 2017 at 04:05 GMT"},"disclaimer":"This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org","bpi":{"USD":{"code":"USD","rate":"9,719.1100","description":"United States Dollar","rate_float":9719.11},"EUR":{"code":"EUR","rate":"8,164.5384","description":"Euro","rate_float":8164.5384}}}')
    pbi = j['bpi']
    graphdata =[]
    for i in range(7,1,-1):
        dt = timedelta(days=i)
        d = today-dt
        graphdata.append(pbi[str(d.year)+'-'+str(d.month)+'-'+str(d.day)])

    graphdata.append(j2['bpi']['EUR']['rate_float'])
    minvalue = graphdata[0]
    maxvalue = graphdata[0]
    for i in range(0,7):
        print(graphdata[i])
        if minvalue>graphdata[i]:
            minvalue = graphdata[i]
        if maxvalue<graphdata[i]:
            maxvalue = graphdata[i]
    #priceeur = j['EUR']
    scalevalue = maxvalue-minvalue
    #text = "BITCOIN "+str(priceeur['last'])+" "+priceeur['symbol']
    print('current hour '+str(currenthour))
    bg = Color("white")
    img = Image(width=176, height=264, background=bg)
    with Drawing() as draw: 
        gh = 100
        draw.stroke_color = Color("black")
        draw.stroke_width = 3.0
        draw.fill_color = bg
        points = []
        for i in range(0,6):
            #points.append((int(176*(i-1)/6),int(gh-gh*(graphdata[i-1]-minvalue)/scalevalue)))
            points.append((int(176*i/6),int(gh-gh*(graphdata[i]-minvalue)/scalevalue)))
        #points.append((int(176*(5)/6),int(gh-gh*(graphdata[5]-minvalue)/scalevalue)))
        points.append((int(176*(5+(currenthour/24))/6),int(176-176*(graphdata[6]-minvalue)/scalevalue)))
        draw.polyline(points)
        draw.stroke_width = 0.0
        draw.fill_color = Color("black")
        draw.text(10,int(gh-gh*(minvalue-minvalue)/scalevalue),str(minvalue)+'€')
        draw.text(10,int(gh-gh*(maxvalue-minvalue)/scalevalue+10),str(maxvalue)+'€')
        draw(img)
        img.save(filename='graph.png')
    return img

#get_bitcoin()


