## Introduction

The purpose of this design is using Xethru X4M300 sensor to detect human presence state at one place and turn on/off TV according to this state through HDMI-CEC, the whole project is deployed on Raspberry Pi.

## Demonstration
Two demonstrations showing how this system work.

1. Backend running 
[https://youtu.be/xYG9iZ3WUAg](https://youtu.be/xYG9iZ3WUAg)

2. Automatically turn on TV (turn-off does not test since TV problem )
[https://youtu.be/nREWL4j3Qi4](https://youtu.be/nREWL4j3Qi4)

## Hardware connection 

![TVauto](/datasheets/TVauto.png)

![connection](/datasheets/connection.png)

## Development Environment

* Raspberry Pi3
* Raspbian: v4.9
* Python: v2.7 
* labcec: v4.0.2
* X4M300 ModuleConnector: rpi-1.1.8 


## Deployment


1. Install [labcec](https://github.com/Pulse-Eight/libcec) on Raspbian, following instructions on [this website](https://github.com/Pulse-Eight/libcec/wiki/Raspberry-Pi-set-up), cec-client will also be installed. The python-libcec library may not be installed correctly, running following command can add python-libcec manully.
```
$ sudo apt-get install python-libcec
```
2. Download X4M300 module connector from [XeThru Community](https://www.xethru.com/community/resources/module-connector-raspberry-pi.81/). Install python library pymoduleconnector by running the following command from the pymoduleconnector root directory:
```
$ python setup.py install
```
3. Connecting equipment according to Hardware Connection. The serial interface connecting X4M300 can be identified by running:
```
$ dmesg | grep tty
```
The name of the serial interface looks like ttyACM0(in my situation).

4. Download [TVauto.py](https://github.com/charlieshao5189/TV-auto-on-off/blob/master/TVauto.py) from this repository. Run
 ```
$ python TVauto.py -d /dev/ttyACM0
```
ttyACM0 should be replaced by your serial interface name.

If evey step goes smoothly, it will just cost half one hour to deploy and test this application.
 
## References
X4M300:[https://www.xethru.com/x4m300-presence-sensor.html](https://www.xethru.com/x4m300-presence-sensor.html)

HDMI-CEC:[https://en.wikipedia.org/wiki/Consumer_Electronics_Control](https://en.wikipedia.org/wiki/Consumer_Electronics_Control)

labcec:[https://github.com/Pulse-Eight/libcec](https://github.com/Pulse-Eight/libcec)

CEC commands: [http://www.cec-o-matic.com/](http://www.cec-o-matic.com/)

Using  cec-client and libcec on Respberry Pi: [https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=53481](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=53481)
