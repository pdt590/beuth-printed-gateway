# How to run script on startup

## Overview

- https://www.raspberrypi.org/documentation/linux/usage/
- https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all
- https://raspberrytips.com/autostart-a-program-on-boot/
- https://www.digikey.de/de/maker/projects/how-to-run-a-raspberry-pi-program-on-startup/cc16cb41a3d447b8aaacf1da14368b13

## crontab

 - References
   - https://www.raspberrypi.org/forums/viewtopic.php?t=187724
   - https://www.cyberciti.biz/faq/linux-execute-cron-job-after-system-reboot/
   - https://unix.stackexchange.com/questions/57852/crontab-job-start-1-min-after-reboot
  
 - Run a cron job automatically after server reboot
  
    ```bash
        sudo crontab -e

        # Edit
        @reboot sleep 300 && python3 /home/pi/mqtt.py >>/home/pi/log.txt 2>&1
    ```

- Start crond automatically at boot time

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable cron.service

    # test
    sudo systemctl start cron.service
    sudo systemctl status cron.service
    sudo systemctl stop cron.service
    ```

- Notes
  - Change sleep time to boot without fault
  - This way is not good

## systemd

- Reference
  - https://www.raspberrypi.org/documentation/linux/usage/systemd.md
  - https://unix.stackexchange.com/questions/531086/create-a-systemd-startup-script-that-delays-30-minutes
  - https://raspberrypi.stackexchange.com/questions/72287/paho-mqtt-error-during-autorun?rq=1
  - https://github.com/coreos/bugs/issues/1966#issuecomment-301825679
  - https://www.freedesktop.org/software/systemd/man/systemd.service.html
  - https://unix.stackexchange.com/questions/225401/how-to-see-full-log-from-systemctl-status-service

- Create a service

    ```bash
    sudo vim /etc/systemd/system/mqtt.service
    ```

    ```bash
    # mqtt.service
    [Unit]
    Description=Mqtt
    Wants=network-online.target
    After=network.target network-online.target

    [Service]
    Type=simple
    ExecStartPre=/bin/sh -c 'until ping -c1 192.168.2.176; do sleep 1; done;'
    ExecStart=/usr/bin/python3 /home/pi/mqtt.py

    [Install]
    WantedBy=multi-user.target
    ```

- Start mqtt.service automatically at boot time

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable mqtt.service

    # test
    sudo python3 run.py

    # or
    sudo systemctl start mqtt.service
    sudo systemctl status mqtt.service
    sudo systemctl stop mqtt.service
    ```

- Notes
  - Change MQTT Server IP
  - It is prossible to add `sleep` if ExecStartPre has timeout issue

## rc.local

## autostart