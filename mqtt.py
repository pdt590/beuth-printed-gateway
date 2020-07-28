# https://anthonychiu.xyz/2016/04/05/communication-between-raspberry-pi-and-multiple-arduinos-via-bluetooth-low-power-ble/
# https://techtutorialsx.com/2017/04/14/python-publishing-messages-to-mqtt-topic/
# https://thingsmatic.com/2017/03/02/influxdb-and-grafana-for-sensor-time-series/
# http://www.steves-internet-guide.com/loop-python-mqtt-client/

from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import threading

import paho.mqtt.client as mqttClient
import time

import json

#
# MQTT
#
Connected = False   #global variable for the state of the connection
broker_address= "141.64.29.79"
port = 1883
user = "mqttuser"
password = "mqttpassword"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

client = mqttClient.Client("Gateway")
client.username_pw_set(user, password=password)
client.on_connect= on_connect
client.connect(broker_address, port=port)

client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)

#
# Bluetooth LE
#
connections = []
connection_threads = []
scanner = Scanner(0)

class NotificationDelegate(DefaultDelegate):

    def __init__(self, number):
        DefaultDelegate.__init__(self)
        self.number = number

    def handleNotification(self, cHandle, data):
        print(data)
        client.publish("sensors/test",data)

class ConnectionHandlerThread (threading.Thread):
    def __init__(self, connection_index):
        threading.Thread.__init__(self)
        self.connection_index = connection_index

    def run(self):
        connection = connections[self.connection_index]
        connection.setDelegate(NotificationDelegate(self.connection_index))

        # enable notification
        setup_data = b"\x01\x00"
        notify = connection.getCharacteristics(uuid='beb5483e-36e1-4688-b7f5-ea07361b26a8')[0]
        notify_handle = notify.getHandle() + 1
        connection.writeCharacteristic(notify_handle, setup_data, withResponse=True)

        while True:
            try:
                if connection.waitForNotifications(1):
                    print("waiting for notifications...")
                    continue
            except:
                connection.disconnect()
                return

try:
    while True:
        print('\nConnected: '+str(len(connection_threads)))
        print('\nScanning...')
        devices = scanner.scan(5, passive=True)
        for d in devices:
            if d.getValueText(9) and "ESP32" in d.getValueText(9):
                print('\nAddress:'+d.addr)
                p = Peripheral(d)
                p.setMTU(256)
                connections.append(p)
                t = ConnectionHandlerThread(len(connections)-1)
                t.start()
                connection_threads.append(t)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()