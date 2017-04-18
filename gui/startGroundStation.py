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

while True:
    time.sleep(1)


