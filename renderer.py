#!/usr/bin/env python3
import weather

from wand.color import Color
from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing

def update_img():
        # weath = weather.get_weather()
        weath = "Tiistai. Lumikuuroja. Ylin lämpötila 0ºC. Tuuli ENE, nopeus 10−15 km/h. Lumisateen mahd: 40%."
        weatherstrip = weath.split(" ")
        lines = [""]
        extraimage = Image(filename='test2.png')

        for w in weatherstrip:
                if len(w)+len(lines[-1]) < 23:
                        lines[-1]+=w+" "
                else:
                        lines.append(w+" ")


        with Color('white') as bg:
                with Drawing() as draw:
                        with Image(width=176, height=264, background=bg) as img:
                                img.composite(extraimage,0,0)
                                draw.font_size = 16 #27
                                lheight = len(lines)-1
                                for l in lines:
                                        draw.text(int(0),int(img.height-draw.font_size*(lheight+0.5)),l)
                                        lheight-=1
                                draw(img)
                                img.save(filename='text.png')
