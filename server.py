#!/usr/bin/env python3
from threading import Timer, Thread, Event
import time
import mugi
import muki_img
import renderer
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM

class ScanDelegate(DefaultDelegate):

    written = {}
    writing = False
    devices = ['dd:35:9b:c3:84:a5']
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.image_filename = "text.png"
        self.update_img()
        Thread(target=self.timed_event).start()
        
    def handleDiscovery(self, dev, isNewDev, isNewData):
        print("Discovered device", dev.addr)
        if(dev.addr in self.devices):
            print("FOund mugi????????"+dev.addr)
            if not self.writing:
                self.writing = True
                self.push_images(dev.addr)

    def push_images(self, addr):
        print("push images")
        if(addr in self.written):
            oldtime = self.written.get(addr)
            currenttime = time.time()
            print("current time"+str(currenttime))
            if currenttime < oldtime + 60:
                print("writing image")
                if mugi.putimage(addr, self.image):
                    self.written[addr] = currenttime
            else:
                print("just written not updating")
        else:
            print("new mugi writing image")
            if mugi.putimage(addr, self.image):
                currenttime = time.time()
                print("current time"+str(currenttime))
                self.written[addr] = currenttime
        self.writing = False

    def timed_event(self):

        while True:
            self.update_img()
            Event().wait(120)
        
    def update_img(self):
        renderer.update_img()
        print("Loading '%s'..." % self.image_filename)
        self.image = muki_img.load_one_bit_byte_array(self.image_filename)


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(600)
