# Development flow:

1. Learn about HDMI ECE 
2. Make HDMI ECE work on Raspbian, turn on/off TV through commands
3. turn on/off TV through Python scripts
4. Make X3M400 work on Raspbian, python based
5. Integer former designs together on one python script.

# Problems:
1. python-ece libary dones not work on rpi3?
Try to run python example, error occur:
```
pi@raspberrypi:~/libcec/src/pyCecClient $ python pyCecClient.py 
Traceback (most recent call last):
  File "pyCecClient.py", line 35, in <module>
    import cec
ImportError: No module named cec
```

It seems the libcec installtion process doesn't install python-cec lib properly.
accodring to https://github.com/Pulse-Eight/libcec/issues/210, reinstall through 
the command:
```
$ sudo apt-get get install python-libcec
```
problem solved.