# https://makersportal.com/blog/2018/4/7/arduino-internet-of-things-part-5-raspberry-pi-as-a-smart-hub-for-sending-data-to-google-sheets
# https://makersportal.com/raspberry-pi-ble-google-sheets-code


from bluepy import btle
import struct, os
from concurrent import futures
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from subprocess import check_output

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

global creds
global addr_var
global delegate_global
global perif_global

creds = ServiceAccountCredentials.from_json_keyfile_name('rpi_creds.json',scope)

addr_var = ['00:25:8a:10:4f:9d','c4:36:c9:cd:9c:52']
sensor_name = ['SheetBME280','SheetDHT22']

class MyDelegate(btle.DefaultDelegate):

    def __init__(self,params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self,cHandle,data):
        global addr_var
        global delegate_global

        for ii in range(len(addr_var)):
            if delegate_global[ii]==self:
                try:
                    data_decoded = struct.unpack("b",data)
                    perif_global[ii].writeCharacteristic(cHandle,struct.pack("b",55))
                    print("Address: "+addr_var[ii])
                    print(data_decoded)
                    try:
                        update_Gsheet(perif_global[ii],sensor_name[ii],data_decoded)
                    except:
                        pass

                    return
                except:                    
                    pass
                try:
                    data_decoded = data.decode('utf-8')
                    perif_global[ii].writeCharacteristic(cHandle,struct.pack("b",55))
                    print("Address: "+addr_var[ii])
                    print(data_decoded)
                    try:
                        update_Gsheet(perif_global[ii],sensor_name[ii],data_decoded)
                    except:
                        pass
                    return
                except:
                    return

def update_Gsheet(perif,sensor_name,data):
    global creds
    data_packet = []
    data_split = data.split(";")
    print("Sensor Name: "+sensor_name)
    print("Data: "+data)
    [data_packet.append(float(ii)) for ii in data_split]
    client = gspread.authorize(creds)
    sheet = client.open("ble_iot_tests").worksheets()
    curr_time = time.localtime()
    time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)
    data_packet = [time_str]+data_packet
    print(data_packet)
    for jj in sheet:
        print(jj.title)
        if jj.title==sensor_name:
            jj.append_row(data_packet)
            print("successfully updated gsheet")
            return
        else:
            print("looking for workbook...")
            continue
    
def perif_loop(perif,indx):
    while True:
        try:
            print("waiting for notifications...")
            if perif.waitForNotifications(1.0):                                
                continue
        except:
            try:
                perif.unpair
                perif.disconnect()
                print("disconnecting from "+perif.addr)
                return
            except:
                return            
            
delegate_global = []
perif_global = []
[delegate_global.append(0) for ii in range(len(addr_var))]
[perif_global.append(0) for ii in range(len(addr_var))]

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
                    perif_global[jj] = p
                    p_delegate = MyDelegate(addr)
                    delegate_global[jj] = p_delegate
                    p.withDelegate(p_delegate)
                    print("Connected to "+addr+" at index: "+str(jj))                    
                    perif_loop(p,jj)                    
                    
        except:
            check_output("sudo hciconfig hci0 down",shell=True).decode()
            check_output("sudo hciconfig hci0 up",shell=True).decode()
            print("failed to connect to "+addr)

ex = futures.ProcessPoolExecutor(max_workers = os.cpu_count())
results = ex.map(establish_connection,addr_var)