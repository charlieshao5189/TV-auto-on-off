#!/usr/bin/env python
""" 
Modified form x4m300_presence_simpleoutput.py. This script sets up and read presence
single messages from the X4M300 module with the ModuleConnector python wrapper.
If the presence state is change from False to True, turn on TV through HDMI-CEC command.
else if the state change from True to False, turn off TV.
"""
import cec
import numpy as np
import time
from pymoduleconnector import ModuleConnector
from time import sleep




XTID_SM_RUN     = int("1",16)
XTID_SM_IDLE    = int("11",16)
XTID_SM_MANUAL  = int("12",16)
XTID_SM_STOP    = int("13",16)


XTID_SSIC_FIRMWAREID                = int("0x02",16)
XTID_SSIC_VERSION                   = int("0x03",16)
XTID_SSIC_BUILD                     = int("0x04",16)
XTID_SSIC_SERIALNUMBER              = int("0x06",16)


XTS_ID_APP_PRESENCE            = int("0x014d4ab8", 16)


XTS_ID_PRESENCE_SINGLE         = int("0x723bfa1e", 16)
XTS_ID_PRESENCE_MOVINGLIST     = int("0x723bfa1f", 16)


class pyCecClient:
  cecconfig = cec.libcec_configuration()
  lib = {}
  # don't enable debug logging by default
  log_level = cec.CEC_LOG_TRAFFIC

  # create a new libcec_configuration
  def SetConfiguration(self):
    self.cecconfig.strDeviceName   = "pyLibCec"
    self.cecconfig.bActivateSource = 0
    self.cecconfig.deviceTypes.Add(cec.CEC_DEVICE_TYPE_RECORDING_DEVICE)
    self.cecconfig.clientVersion = cec.LIBCEC_VERSION_CURRENT

  def SetLogCallback(self, callback):
    self.cecconfig.SetLogCallback(callback)

  def SetKeyPressCallback(self, callback):
    self.cecconfig.SetKeyPressCallback(callback)

  def SetCommandCallback(self, callback):
    self.cecconfig.SetCommandCallback(callback)

  # detect an adapter and return the com port path
  def DetectAdapter(self):
    retval = None
    adapters = self.lib.DetectAdapters()
    for adapter in adapters:
      print("found a CEC adapter:")
      print("port:     " + adapter.strComName)
      print("vendor:   " + hex(adapter.iVendorId))
      print("product:  " + hex(adapter.iProductId))
      retval = adapter.strComName
    return retval

  # initialise libCEC
  def InitLibCec(self):
    self.lib = cec.ICECAdapter.Create(self.cecconfig)
    # print libCEC version and compilation information
    print("libCEC version " + self.lib.VersionToString(self.cecconfig.serverVersion) + " loaded: " + self.lib.GetLibInfo())

    # search for adapters
    adapter = self.DetectAdapter()
    if adapter == None:
      print("No adapters found")
    else:
      if self.lib.Open(adapter):
        print("connection opened")
        self.MainLoop()
      else:
        print("failed to open a connection to the CEC adapter")

  # display the addresses controlled by libCEC
  def ProcessCommandSelf(self):
    addresses = self.lib.GetLogicalAddresses()
    strOut = "Addresses controlled by libCEC: "
    x = 0
    notFirst = False
    while x < 15:
      if addresses.IsSet(x):
        if notFirst:
          strOut += ", "
        strOut += self.lib.LogicalAddressToString(x)
        if self.lib.IsActiveSource(x):
          strOut += " (*)"
        notFirst = True
      x += 1
    print(strOut)

  # send an active source message
  def ProcessCommandActiveSource(self):
    self.lib.SetActiveSource()

  # send a standby command
  def ProcessCommandStandby(self):
    self.lib.StandbyDevices(cec.CECDEVICE_BROADCAST)

  # send a custom command
  def ProcessCommandTx(self, data):
    cmd = self.lib.CommandFromString(data)
    print("transmit " + data)
    if self.lib.Transmit(cmd):
      print("command sent")
    else:
      print("failed to send command")

  # scan the bus and display devices that were found
  def ProcessCommandScan(self):
    print("requesting CEC bus information ...")
    strLog = "CEC bus information\n===================\n"
    addresses = self.lib.GetActiveDevices()
    activeSource = self.lib.GetActiveSource()
    x = 0
    while x < 15:
      if addresses.IsSet(x):
        vendorId        = self.lib.GetDeviceVendorId(x)
        physicalAddress = self.lib.GetDevicePhysicalAddress(x)
        active          = self.lib.IsActiveSource(x)
        cecVersion      = self.lib.GetDeviceCecVersion(x)
        power           = self.lib.GetDevicePowerStatus(x)
        osdName         = self.lib.GetDeviceOSDName(x)
        strLog += "device #" + str(x) +": " + self.lib.LogicalAddressToString(x)  + "\n"
        strLog += "address:       " + str(physicalAddress) + "\n"
        strLog += "active source: " + str(active) + "\n"
        strLog += "vendor:        " + self.lib.VendorIdToString(vendorId) + "\n"
        strLog += "CEC version:   " + self.lib.CecVersionToString(cecVersion) + "\n"
        strLog += "OSD name:      " + osdName + "\n"
        strLog += "power status:  " + self.lib.PowerStatusToString(power) + "\n\n\n"
      x += 1
    print(strLog)


def x4m300_presence_simpleoutput(device_name, detection_zone=(0.5,9), sensitivity=5):


    # User settings
    detzone_start = detection_zone[0]
    detzone_end = detection_zone[1]


    presence_state_text = []
    presence_state_text.append("No presence")
    presence_state_text.append("Presence")
    presence_state_text.append("Initializing")


    mc = ModuleConnector(device_name, log_level=0)
    x4m300 = mc.get_x4m300()


    sleep(1) # Allow for MC to read waiting messages from module.


    try:
        x4m300.set_sensor_mode(XTID_SM_STOP, 0) # Make sure no profile is running.
        print("Stopped already running profile.")
    except RuntimeError:
        # If not initialized, stop returns error. Still OK, just wanted to make sure the profile was not running.
        pass


    # Now flush old messages from module
    print("Flushing any old data.")
    while x4m300.peek_message_presence_single():
        presence_single = x4m300.read_message_presence_single()


    # Read module info
    print("FirmwareID: " + x4m300.get_system_info(XTID_SSIC_FIRMWAREID))
    print("Version: " + x4m300.get_system_info(XTID_SSIC_VERSION))
    print("Build: " + x4m300.get_system_info(XTID_SSIC_BUILD))
    print("Serial number: " + x4m300.get_system_info(XTID_SSIC_SERIALNUMBER))


    print("Loading new profile.")
    x4m300.load_profile(XTS_ID_APP_PRESENCE)


    print("Selecting module output.")
    x4m300.set_output_control(XTS_ID_PRESENCE_SINGLE, 1) # PresenceSingle
    x4m300.set_output_control(XTS_ID_PRESENCE_MOVINGLIST, 0) # PresenceMovingList


    print("Setting user settings: DetectionZone = " + str(detzone_start) + " to " + str(detzone_end) + ", Sensitivity = " + str(sensitivity))
    x4m300.set_detection_zone(detzone_start, detzone_end)
    x4m300.set_sensitivity(sensitivity)


    print("Start profile execution.")
    x4m300.set_sensor_mode(XTID_SM_RUN, 0) # Make sure no profile is running.


    print("Waiting for data...")


    while True:
        time.sleep(0.1)


        while x4m300.peek_message_presence_single():
            presence_single = x4m300.read_message_presence_single()
            print("Presence ->"
                + " FrameCounter: " + str(presence_single.frame_counter)
                + ", State: " + presence_state_text[presence_single.presence_state]
                + ", Distance: " + str(round(presence_single.distance,2))
                + ", SignalQuality: " + str(presence_single.signal_quality)
                )
            # turn on/off TV according to humman persence state 
            if 1 == presence_single and 0 == prePresence_single:
                 #turn on
                 cec.ProcessCommandActiveSource()
                 print  "Turn on TV"
            elsif 0 == presence_single and 1 == prePresence_single:
                 #turn off
                 cec.ProcessCommandStandby()
                 print  "Turn off TV"
            else:
                 print "no turn on/off action to TV"
    return x2m200




def main():
    import sys
    from optparse import OptionParser
    
    cec = pyCecClient()
   
    parser = OptionParser()
    parser.add_option(
        "-d",
        "--device",
        dest="device_name",
        help="device file to use, example: python %s -d COM4"%sys.argv[0],
        metavar="FILE")


    parser.add_option('-z', '--detection_zone', nargs=2, type='float',
        help='Start and stop of detection zone.', metavar='START STOP',
        default=(0.5, 9))


    parser.add_option('-s', '--sensitivity', nargs=1, type='int',
        help='Sensor Sensitivity.', metavar='SENSITIVITY',
        default=5)


    (options, args) = parser.parse_args()


    if not options.device_name:
        print "Please specify a device name, example: python %s -d COM4"%sys.argv[0]
        sys.exit(1)
    x4m300_presence_simpleoutput(**vars(options))




if __name__ == "__main__":
    main()
