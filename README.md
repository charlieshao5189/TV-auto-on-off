## Introduction

The purpose of this design is using Xethru X4M300 sensor to detect human presence state at one place and turn on/off TV according to this state through HDMI-CEC, the whole project is deployed on Raspberry Pi.


## Hardware connection 

![TVauto]((/TVauto.png)

## Development Environment

* Raspberry Pi3
* Raspbian: v4.9
* Python: v2.7 
* labcec: v4.0.2
* X4M300 ModuleConnector: rpi-1.1.8  
* GCC: 

## Deloyment


1. Install [labcec](https://github.com/Pulse-Eight/libcec) on Raspbian, following instructions on [this websit](https://github.com/Pulse-Eight/libcec/wiki/Raspberry-Pi-set-up), cec-client will also be installed. The python-libcec libitory may not be installed properly, running following command can add python-libcec manully.
```python
$ sudo apt-get get install python-libcec
```
2. Download X4M300 module connector from [XeThru Community](https://www.xethru.com/community/resources/module-connector-raspberry-pi.81/). Install python library pymoduleconnector by running the following command from the pymoduleconnector root directory:
```python
$ python setup.py install
```
3. Connecting equipment according to Hardware Connection. The serial interface connecting X4M300 can be identified by running:
```
$ dmesg | grep tty
```
The name of the serial interface looks like ttyS0.
4. Download [TVauto.py](https://github.com/charlieshao5189/TV-auto-on-off/blob/master/TVauto.py) from this repository. Run
 ```python
$ python TVauto.py ttyS0
```
 
## References
X4M300:[https://www.xethru.com/x4m300-presence-sensor.html](https://www.xethru.com/x4m300-presence-sensor.html)
HDMI-CEC:[https://en.wikipedia.org/wiki/Consumer_Electronics_Control](https://en.wikipedia.org/wiki/Consumer_Electronics_Control)
labcec:[https://github.com/Pulse-Eight/libcec](https://github.com/Pulse-Eight/libcec)
CEC commands: [http://www.cec-o-matic.com/](http://www.cec-o-matic.com/)
Using  cec-client and libcec on Respberry Pi: [https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=53481](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=53481)
