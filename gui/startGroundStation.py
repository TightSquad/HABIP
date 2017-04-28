#!/usr/bin/env python

import subprocess
import time


# Start soundmodem
subprocess.Popen("./startsoundmodem.sh")
time.sleep(1)

# Start axlisten for soundmodem to listen for AX.25 packets
subprocess.Popen("./startaxlisten.sh")
time.sleep(1)

# Start logger to parse axlisten log to get data/commands out of it from the platform
subprocess.Popen(["python","axlisten_logger.py"])
time.sleep(1)

# Start command GUI to send commands to the platform
subprocess.Popen(["python","command_gui.py"])
time.sleep(1)

# Start data display GUI to show graphs of sensor data
subprocess.Popen(["python","data_plot_gui.py"])
time.sleep(1)

# Start GPS data display GUI to show GPS data path (GPS data from the telemetry stream)
subprocess.Popen(["python","gps_data_gui.py"])
time.sleep(1)

while True:
    time.sleep(1)


