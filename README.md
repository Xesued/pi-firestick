PI Firestick
==============

Simple project to make your Raspberry pi capible of being a 
conroller for the Amazon Firestick.


Requirements 
--------------

(IF we are using the IR remote stuff....)

Install the [`pigpio`](http://abyz.me.uk/rpi/pigpio/index.html):

```bash
sudo apt-get update
sudo apt-get install pigpio python-pigpio python3-pigpio
```

Then run it:
```bash
sudo pigpiod
```

Usage
-------------

Record IR codes for your TV:

```bash
python3 pi-firestick read
```
