#https://www.silabs.com/community/wireless/bluetooth/forum.topic.html/python_code_to_useb-RswG

import struct
from bluepy.btle import *

# callback class
class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(data)

# connect to device
per = Peripheral("80:7d:3a:b8:27:fa", "public")

try:
    # set callback for notifications
    per.setDelegate(MyDelegate())

    # enable notification
    setup_data = b"\x01\x00"
    notify = per.getCharacteristics(uuid='beb5483e-36e1-4688-b7f5-ea07361b26a8')[0]
    notify_handle = notify.getHandle() + 1
    per.writeCharacteristic(notify_handle, setup_data, withResponse=True)
    
    # send test string
    c = per.getCharacteristics(uuid='beb5483e-36e1-4688-b7f5-ea07361b26a8')[0]
    c.write("Hello Gecko")
    
    # wait for answer
    while True:
        if per.waitForNotifications(1.0):
            continue
finally:
    per.disconnect()