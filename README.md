# beuth-printed-gateway

Gateway for PrintED project

## Compatibility

- [beuth-printed-sensor-fw](https://github.com/pdt590/beuth-printed-sensor-fw) using LIS3DH and BME680 sensors
- [beuth-printed-sensor-hw](https://github.com/pdt590/beuth-printed-sensor-hw) using LIS3DH and BME680 sensors
- [beuth-printed-app](https://github.com/pdt590/beuth-printed-app)
- [beuth-printed-gateway](https://github.com/pdt590/beuth-printed-gateway)
- [beuth-printed-cloud](https://github.com/pdt590/beuth-printed-cloud)

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