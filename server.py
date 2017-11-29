#!/usr/bin/env python3
from threading import Timer, Thread, Event
import time
import mugi
import muki_img
import renderer
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM, BTLEException

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
    def handleDiscovery(self, dev, isNewDev, isNewData):
        print("Discovered device", dev.addr)

def push_images(addr, image):
    print("push images "+addr)
    if(addr in written):
        oldtime = written.get(addr)
        currenttime = time.time()
        print("current time"+str(currenttime))
        if currenttime > oldtime + 60:
            print("writing image")
            if mugi.putimage(addr, image):
                written[addr] = currenttime
        else:
            print("just written not updating")
    else:
        print("new mugi writing image")
        if mugi.putimage(addr, image):
            currenttime = time.time()
            print("current time"+str(currenttime))
            written[addr] = currenttime
    writing = False

def update_img():
    renderer.update_img()
    print("Loading '%s'..." % image_filename)
    image = muki_img.load_one_bit_byte_array(image_filename)
    return image

def timed_event():
    while True:
        global img
        img = update_img()
        Event().wait(1200)
written = {}
writing = False
mydevices = ['dd:35:9b:c3:84:a5']

image_filename = "text.png"
devices = []

scanner = Scanner().withDelegate(ScanDelegate())

Thread(target=timed_event).start()
while True:
    try:
        devices = scanner.scan(30.0)
    except BTLEException:
        print("failed to scan")
    for device in devices:
        if device.addr in mydevices:
            push_images(device.addr, img)

        
