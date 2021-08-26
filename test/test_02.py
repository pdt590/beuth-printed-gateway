# https://makersportal.com/blog/2018/3/25/arduino-internet-of-things-part-4-connecting-bluetooth-nodes-to-the-raspberry-pi-using-pythons-bluepy-library
# https://makersportal.com/raspberry-pi-ble-code
# https://thingsmatic.com/2017/03/02/influxdb-and-grafana-for-sensor-time-series/

from bluepy import btle
import struct, os
from concurrent import futures

global addr_var
global delegate_global
global perif_global

#addr_var = ['80:7d:3a:b8:27:fa']
addr_var = []
delegate_global = []
perif_global = []
scanner = btle.Scanner(0)

class MyDelegate(btle.DefaultDelegate):

    def __init__(self,params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self,cHandle,data):
        print(data)

    
def perif_loop(perif,indx):
    while True:
        try:
            if perif.waitForNotifications(1.0):
                print("waiting for notifications...")
                continue
        except:
            try:
                perif.disconnect()
            except:
                pass
            print("disconnecting perif: "+perif.addr+", index: "+str(indx))
            reestablish_connection(perif,perif.addr,indx)

def reestablish_connection(perif,addr,indx):
    while True:
        try:
            print("trying to reconnect with "+addr)
            #perif.connect(addr)
            establish_connection(addr)
        except:
            continue

def establish_connection(addr):
    global delegate_global
    global perif_global
    global addr_var

    while True:
        try:
            for jj in range(len(addr_var)):
                if addr_var[jj]==addr:
                    print("Attempting to connect with "+addr+" at index: "+str(jj))
                    p = btle.Peripheral(addr)
                    p.setMTU(256)
                    perif_global[jj] = p
                    p_delegate = MyDelegate(addr)
                    delegate_global[jj] = p_delegate
                    p.withDelegate(p_delegate)
                    print("Connected to "+addr+" at index: "+str(jj))

                    # enable notification
                    setup_data = b"\x01\x00"
                    notify = p.getCharacteristics(uuid='beb5483e-36e1-4688-b7f5-ea07361b26a8')[0]
                    notify_handle = notify.getHandle() + 1
                    p.writeCharacteristic(notify_handle, setup_data, withResponse=True)

                    perif_loop(p,jj)
        except:
            print("failed to connect to "+addr)
            continue

devices = scanner.scan(10.0, passive=True)
for d in devices:
    print(d.addr)
    if d.getValueText(9) and "ESP32" in d.getValueText(9):
        if d.addr not in addr_var:
            addr_var.append(d.addr)

[delegate_global.append(0) for ii in range(len(addr_var))]
[perif_global.append(0) for ii in range(len(addr_var))]

ex = futures.ProcessPoolExecutor(max_workers = os.cpu_count())
results = ex.map(establish_connection,addr_var)