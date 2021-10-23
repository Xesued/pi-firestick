PI Firestick
==============

Simple project to make your Raspberry pi capible of being a 
conroller for the Amazon Firestick.

Insperation
--------------
IR Circuit:
https://blog.gordonturner.com/2020/05/31/raspberry-pi-ir-receiver/

Bluetooth:
https://impythonist.wordpress.com/2014/02/01/emulate-a-bluetooth-keyboard-with-the-raspberry-pi/


Requirements 
--------------

(If we are using the IR remote...)

Install the [`pigpio`](http://abyz.me.uk/rpi/pigpio/index.html):

```bash
sudo apt-get update
sudo apt-get install pigpio python-pigpio python3-pigpio
sudo systemctl enable pigpiod
```

Install LCD libraries
```
sudo ./setup-lcd.sh
```

Install python requirements

```bash
pip3 install -r requirments.txt
```

Usage
-------------

Before anything else, you need to start the pigpiod dameon
```bash
sudo pigpiod
```

Record IR codes for your TV:

```bash
python3 -u main.py read
```


### Installing the service
If you want to have the remote startup, copy the service file to your local services:
```
sudo cp pifirestick.service /etc/systemd/system/pifirestick.service
sudo systemctl enable pifirestick.service
```

