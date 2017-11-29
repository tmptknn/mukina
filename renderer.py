#!/usr/bin/env python3
import weather
import bitcoin
import bitcoin2

from wand.color import Color
from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing
import urllib.request

def update_img():
        bitcoins = bitcoin.get_bitcoin()
        bitcoingraph = bitcoin2.get_bitcoin()
        weath, icon = weather.get_weather()
        #weath = "Tiistai. Lumikuuroja. Ylin lämpötila 0ºC. Tuuli ENE, nopeus 10−15 km/h. Lumisateen mahd: 40%."

        f = urllib.request.urlopen(icon)
        infos = bitcoins+" "+weath
        weatherstrip = infos.split(" ")
        lines = [""]
        #extraimage = Image(filename='test2.png')
        extraimage = Image(file=f)
        eiw=extraimage.width
        eih=extraimage.height
        if eiw/eih > 176/264:
                iw = 176
                ih = 176*eih/eiw
        else:
                iw = 264*eiw/eih
                ih = 264
        #extraimage.resize(int(iw),int(ih))
        
        #extraimage.gamma(0.2)
        for w in weatherstrip:
                if len(w)+len(lines[-1]) < 23:
                        lines[-1]+=w+" "
                else:
                        lines.append(w+" ")

        with Color('white') as bg:
                with Drawing() as draw:
                        with Image(width=176, height=264, background=bg) as img:
                                img.type = 'bilevel'
                                img.composite(bitcoingraph,0,0)
                                img.composite(extraimage,0,100)
                                draw.font_size = 16 #27
                                lheight = len(lines)-1
                                for l in lines:
                                        draw.text(int(0),int(img.height-draw.font_size*(lheight+0.5)),l)
                                        lheight-=1
                                draw(img)
                                #img.negate()
                                img.save(filename='text.png')

#update_img()
