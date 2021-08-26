# https://anthonychiu.xyz/2016/04/05/communication-between-raspberry-pi-and-multiple-arduinos-via-bluetooth-low-power-ble/

from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import threading

class NotificationDelegate(DefaultDelegate):

    def __init__(self, number):
        DefaultDelegate.__init__(self)
        self.number = number

    def handleNotification(self, cHandle, data):
        print '\n*****Notification*****\nConnection:'+str(self.number)+'\nHandler:'+str(cHandle)+'\nMsg:'+data

connections = []
connection_threads = []
scanner = Scanner(0)

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

while True:
    print'\nConnected: '+str(len(connection_threads))
    print '\nScanning...'
    devices = scanner.scan(5, passive=True)
    for d in devices:
        if d.getValueText(9) and "ESP32" in d.getValueText(9):
            print '\nAddress:'+d.addr
            p = Peripheral(d)
            p.setMTU(256)
            connections.append(p)
            t = ConnectionHandlerThread(len(connections)-1)
            t.start()
            connection_threads.append(t)