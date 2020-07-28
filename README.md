# beuth-printed-gateway

Gateway for PrintED project

## Keywords
  
  - Raspberry Pi 4B
  - ESP32
  - BLE
    - [bluepy](https://github.com/IanHarvey/bluepy)
    - bluez
  - Mqtt

## Get started
  - Use Python 3
  - Install
  
    ```bash
      $ sudo apt-get install python3-pip libglib2.0-dev
      $ sudo pip3 install bluepy
      $ sudo pip3 install paho-mqtt 
    ```
  - How to run

    ```bash
      $ sudo python3 mqtt.py
    ```
  - How to make `mqtt.py` auto boot up
    - [autoboot](https://github.com/pdt590/beuth-printed-gateway/blob/master/AUTOBOOT.md)
