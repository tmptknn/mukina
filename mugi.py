#!/usr/bin/env python3
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM, BTLEException

def putimage(addr,image):
    #  line below needs to be changed to use your mugs MAC address
    try:
        peripheral = Peripheral(addr, addrType=ADDR_TYPE_RANDOM)
        print("connected to muki")
        # line below uses characteristics directly. you can also request it
        characteristic = peripheral.getCharacteristics(uuid='06640002-9087-04a8-658f-ce44cb96b4a1')[0]
        print("writing image to device")
    
        characteristic.write(bytes.fromhex('74'),withResponse=True)
        # Write image in 291 chunks, 20 bytes at time
        index = 0
        for i in range(0,291):
            data = image[index:index + 20]
            # last one may be too short
            while len(data) < 20:
                data.append(0xFF)
            characteristic.write(data, withResponse=False)
            index = index + 20
    
        # this one is write without response because it fails if response
        # is required. Image is written anyway 
        characteristic.write(bytes.fromhex('64'), withResponse=True)
        peripheral.disconnect()
    except (BTLEException):
        print("Write failed")
        return False
    print("write successful");
    return True
