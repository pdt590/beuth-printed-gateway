# beuth-printed-gateway

Gateway for PrintED project

## Compatibility

- [beuth-printed-sensor-fw/bme680-lis3dh](https://github.com/pdthang/beuth-esp32-ble/tree/bme680-lis3dh) using LIS3DH and BME680 sensors
- [beuth-printed-sensor-hw/master](https://github.com/pdt590/beuth-printed-sensor-hw) using LIS3DH and BME680 sensors
- [beuth-printed-app/bme680-lis3dh](https://github.com/pdt590/beuth-printed-app/tree/bme680-lis3dh)
- [beuth-printed-gateway/master](https://github.com/pdt590/beuth-printed-gateway)
- [beuth-printed-cloud/master](https://github.com/pdt590/beuth-printed-cloud)

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

- Change MQTT Broker IP
  - [mqtt.py](https://github.com/pdt590/beuth-printed-gateway/blob/master/mqtt.py#L18)
  - [mqtt.service](https://github.com/pdt590/beuth-printed-gateway/blob/master/mqtt.service#L8)

- How to run

  ```bash
  $ sudo python3 mqtt.py
  ```

- How to make `mqtt.py` auto boot up
  - [autoboot](https://github.com/pdt590/beuth-printed-gateway/blob/master/AUTOBOOT.md)
