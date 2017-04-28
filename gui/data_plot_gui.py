# Make sure matplotlib is installed


# Based on tutorial at: https://pythonprogramming.net/adding-trading-option/?completed=/adding-indicator-choice-menu/
# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import Tkinter as tk
import ttk

from matplotlib import pyplot as plt

from decimal import Decimal

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

# Graph
f = Figure()
a = f.add_subplot(111)

# Current sensor
sensor = "B0:TD0" # default to BCM die temp sensor of Pi Hat 0

# Sensor abbreviation dictionary
# First value element is graph title associated with the sensor
# Second value element is y axis label with units associated with the sensor
# Third value is the index in the parsed data line (comma separated values on lines per received set of data) that the data for the sensor is at
graphTable = {
    "B0:TD0": ["Pi Hat 0 BCM Die Temperature Sensor","Temperature (degC)",5],
    "B0:TB0": ["Pi Hat 0 Board Temperature Sensor #0","Temperature (degC)",1],
    "B0:TB1": ["Pi Hat 0 Board Temperature Sensor #1","Temperature (degC)",2],
    "B0:TE0": ["Pi Hat 0 External Temperature Sensor #0","Temperature (degC)",3],
    "B0:TE1": ["Pi Hat 0 External Temperature Sensor #1","Temperature (degC)",4],
    "B1:TD0": ["Pi Hat 1 BCM Die Temperature Sensor","Temperature (degC)",15],
    "B1:TB0": ["Pi Hat 1 Board Temperature Sensor #0","Temperature (degC)",11],
    "B1:TB1": ["Pi Hat 1 Board Temperature Sensor #1","Temperature (degC)",12],
    "B1:TE0": ["Pi Hat 1 External Temperature Sensor #0","Temperature (degC)",13],
    "B1:TE1": ["Pi Hat 1 External Temperature Sensor #1","Temperature (degC)",14],
    "B2:TD0": ["Pi Hat 2 BCM Die Temperature Sensor","Temperature (degC)",25],
    "B2:TB0": ["Pi Hat 2 Board Temperature Sensor #0","Temperature (degC)",21],
    "B2:TB1": ["Pi Hat 2 Board Temperature Sensor #1","Temperature (degC)",22],
    "B2:TE0": ["Pi Hat 2 External Temperature Sensor #0","Temperature (degC)",23],
    "B2:TE1": ["Pi Hat 2 External Temperature Sensor #1","Temperature (degC)",24],
    "B3:TD0": ["Pi Hat 3 BCM Die Temperature Sensor","Temperature (degC)",35],
    "B3:TB0": ["Pi Hat 3 Board Temperature Sensor #0","Temperature (degC)",31],
    "B3:TB1": ["Pi Hat 3 Board Temperature Sensor #1","Temperature (degC)",32],
    "B3:TE0": ["Pi Hat 3 External Temperature Sensor #0","Temperature (degC)",33],
    "B3:TE1": ["Pi Hat 3 External Temperature Sensor #1","Temperature (degC)",34],
    "B4:TB0": ["DAQCS Board Temperature Sensor #0","Temperature (degC)",41],
    "B5:TD0": ["COMMS Board BCM Die Temperature Sensor","Temperature (degC)",58],
    "B5:TB0": ["COMMS Board Temperature Sensor #0","Temperature (degC)",57],
    "B0:P0": ["Pi Hat 0 Basic Pressure Sensor","Pressure (mBar)",6],
    "B0:P1": ["Pi Hat 0 Vacuum Pressure Sensor","Pressure (mBar)",7],
    "B1:P0": ["Pi Hat 1 Basic Pressure Sensor","Pressure (mBar)",16],
    "B1:P1": ["Pi Hat 1 Vacuum Pressure Sensor","Pressure (mBar)",17],
    "B2:P0": ["Pi Hat 2 Basic Pressure Sensor","Pressure (mBar)",26],
    "B2:P1": ["Pi Hat 2 Vacuum Pressure Sensor","Pressure (mBar)",27],
    "B3:P0": ["Pi Hat 3 Basic Pressure Sensor","Pressure (mBar)",36],
    "B3:P1": ["Pi Hat 3 Vacuum Pressure Sensor","Pressure (mBar)",37],
    "B4:PO": ["DAQCS Board Basic Pressure Sensor","Pressure (mBar)",42],
    "B4:PB": ["Balloon Pressure Sensor","Pressure (mBar)",43],
    "B5:P0": ["COMMS Board Basic Pressure Sensor","Pressure (mBar)",59],
    "B0:H": ["Pi Hat 0 Humidity Sensor","Relative Humidity (%)",8],
    "B1:H": ["Pi Hat 1 Humidity Sensor","Relative Humidity (%)",18],
    "B2:H": ["Pi Hat 2 Humidity Sensor","Relative Humidity (%)",28],
    "B3:H": ["Pi Hat 3 Humidity Sensor","Relative Humidity (%)",38],
    "B0:V": ["Pi Hat 0 Power Monitor - Supply Voltage","Voltage (V)",9],
    "B0:C": ["Pi Hat 0 Power Monitor - Supply Current","Current (mA)",10],
    "B1:V": ["Pi Hat 1 Power Monitor - Supply Voltage","Voltage (V)",19],
    "B1:C": ["Pi Hat 1 Power Monitor - Supply Current","Current (mA)",20],
    "B2:V": ["Pi Hat 2 Power Monitor - Supply Voltage","Voltage (V",29],
    "B2:C": ["Pi Hat 2 Power Monitor - Supply Current","Current (mA)",30],
    "B3:V": ["Pi Hat 3 Power Monitor - Supply Voltage","Voltage (V)",39],
    "B3:C": ["Pi Hat 3 Power Monitor - Supply Current","Current (mA)",40],
    "B4:V": ["DAQCS Board Power Monitor - Supply Voltage","Voltage (V)",44],
    "B4:C": ["DAQCS Board Power Monitor - Supply Current","Current (mA)",45],
    "B4:XGY": ["IMU Gyroscope X","Angular Velocity (deg/s)",46],
    "B4:XAC": ["IMU Acceleration X","Acceleration (deg/s^2)",47],
    "B4:YGY": ["IMU Gyroscope Y","Angular Velocity (deg/s)",48],
    "B4:YAC": ["IMU Acceleration Y","Acceleration (deg/s^2)",49],
    "B4:ZGY": ["IMU Gyroscope Z","Angular Velocity (deg/s)",50],
    "B4:ZAC": ["IMU Acceleration Z","Acceleration (deg/s^2)",51],
    "B4:MS": ["Motor Speed","Speed (RPM)",52],
    "B4:MC": ["Motor Current Draw","Current (mA)",53],
    "B4:MV": ["Motor Battery Voltage","Voltage (V)",54],
    "B4:MD": ["Motor Direction (1=CW, 0=CCW)","",55],
    "B4:ME": ["Motor Status (1=ON, 0=OFF)","",56],
    "B5:LAT": ["GPS - Latitude","",60],
    "B5:LON": ["GPS - Longitude","",61],
    "B5:TM": ["GPS - Time","",62],
    "B5:SPD": ["GPS - Speed","Speed (mph)",63],
    "B5:ALT": ["GPS - Altitude","Altitude (meters)",64],
    "B5:TBL": ["Balloon Temperature (degC", 65],
    "B5:PBL": ["Ballon Pressure (mBar)", 66],
}

graphStartTime = None

# Add the data of the currently selected sensor to a graph in the frame
def animate(i):
    global graphStartTime

    # Grab graph title, y axis label, data file index from dictionary based on current sensor
    graphInfo = graphTable.get(sensor, ["ERROR with sensor value","ERROR"])

    fileIndex = graphInfo[2]
    
    # Open data file and split up each line
    pullData = open("/home/spex/habip_data.log","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []

    # Loop through file lines
    for eachLine in dataList:
        if len(eachLine) > 1:
            lineData = eachLine.split(',') # Sensor data is comma separated

            # Data is on the y-axis
            data = lineData[fileIndex] # Grab the data for the current sensor (a string with the value)

            # If there is data present
            if data != "NULL":
                yList.append(Decimal(data)) # Add it to the list of y-values

                # Plot time on x-axis
                # First part of line is timestamp for data
                h, m, s = lineData[0].split(':')
                timeStampInMinutes = int(h)*60 + int(m) + int(s)/60
                if graphStartTime == None: # Put as start time if first data received
                    graphStartTime = timeStampInMinutes
                    xList.append(0)
                else:
                    xList.append(timeStampInMinutes-graphStartTime) # Just want difference in time since starting

    # Update data graph
    a.clear()
    a.plot(xList, yList)
    a.set_title(graphInfo[0])
    a.set_xlabel("Time Since Start (min)")
    a.set_ylabel(graphInfo[1])

class graphGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Data Graphs")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create top level sensor menu
        self.menubar = tk.Menu(container)

        # Create submenus
        self.createTempSensorMenu()
        self.createPresSensorMenu()
        self.createHumidSensorMenu()
        self.createPowerSensorMenu()
        self.createReactionWheelMenu()
        self.createGpsSensorMenu()

        # Configure top level sensor menu
        tk.Tk.config(self, menu=self.menubar)

        # Create data graph
        self.frame = DataGraph(container, self)
        self.frame.grid(row=0, column=0, sticky="nsew")

    def createTempSensorMenu(self):
        # Create dropdown in menu for temperature sensors
        tempSensorMenu = tk.Menu(self.menubar, tearoff=0)
        # Submenu for Pi Hat 0
        tempSensorPiHat0Menu = tk.Menu(tempSensorMenu, tearoff=0)
        tempSensorPiHat0Menu.add_command(label="BCM Die", command=lambda: self.changeSensor("B0:TD0"))
        tempSensorPiHat0Menu.add_separator()
        tempSensorPiHat0Menu.add_command(label="Board #0", command=lambda: self.changeSensor("B0:TB0"))
        tempSensorPiHat0Menu.add_separator()
        tempSensorPiHat0Menu.add_command(label="Board #1", command=lambda: self.changeSensor("B0:TB1"))
        tempSensorPiHat0Menu.add_separator()
        tempSensorPiHat0Menu.add_command(label="External #0", command=lambda: self.changeSensor("B0:TE0"))
        tempSensorPiHat0Menu.add_separator()
        tempSensorPiHat0Menu.add_command(label="External #1", command=lambda: self.changeSensor("B0:TE1"))
        tempSensorMenu.add_cascade(label="Pi Hat 0", menu=tempSensorPiHat0Menu)
        # Submenu for Pi Hat 1
        tempSensorPiHat1Menu = tk.Menu(tempSensorMenu, tearoff=0)
        tempSensorPiHat1Menu.add_command(label="BCM Die", command=lambda: self.changeSensor("B1:TD0"))
        tempSensorPiHat1Menu.add_separator()
        tempSensorPiHat1Menu.add_command(label="Board #0", command=lambda: self.changeSensor("B1:TB0"))
        tempSensorPiHat1Menu.add_separator()
        tempSensorPiHat1Menu.add_command(label="Board #1", command=lambda: self.changeSensor("B1:TB1"))
        tempSensorPiHat1Menu.add_separator()
        tempSensorPiHat1Menu.add_command(label="External #0", command=lambda: self.changeSensor("B1:TE0"))
        tempSensorPiHat1Menu.add_separator()
        tempSensorPiHat1Menu.add_command(label="External #1", command=lambda: self.changeSensor("B1:TE1"))
        tempSensorMenu.add_cascade(label="Pi Hat 1", menu=tempSensorPiHat1Menu)
        # Submenu for Pi Hat 2
        tempSensorPiHat2Menu = tk.Menu(tempSensorMenu, tearoff=0)
        tempSensorPiHat2Menu.add_command(label="BCM Die", command=lambda: self.changeSensor("B2:TD0"))
        tempSensorPiHat2Menu.add_separator()
        tempSensorPiHat2Menu.add_command(label="Board #0", command=lambda: self.changeSensor("B2:TB0"))
        tempSensorPiHat2Menu.add_separator()
        tempSensorPiHat2Menu.add_command(label="Board #1", command=lambda: self.changeSensor("B2:TB1"))
        tempSensorPiHat2Menu.add_separator()
        tempSensorPiHat2Menu.add_command(label="External #0", command=lambda: self.changeSensor("B2:TE0"))
        tempSensorPiHat2Menu.add_separator()
        tempSensorPiHat2Menu.add_command(label="External #1", command=lambda: self.changeSensor("B2:TE1"))
        tempSensorMenu.add_cascade(label="Pi Hat 2", menu=tempSensorPiHat2Menu)
        # Submenu for Pi Hat 3
        tempSensorPiHat3Menu = tk.Menu(tempSensorMenu, tearoff=0)
        tempSensorPiHat3Menu.add_command(label="BCM Die", command=lambda: self.changeSensor("B3:TD0"))
        tempSensorPiHat3Menu.add_separator()
        tempSensorPiHat3Menu.add_command(label="Board #0", command=lambda: self.changeSensor("B3:TB0"))
        tempSensorPiHat3Menu.add_separator()
        tempSensorPiHat3Menu.add_command(label="Board #1", command=lambda: self.changeSensor("B3:TB1"))
        tempSensorPiHat3Menu.add_separator()
        tempSensorPiHat3Menu.add_command(label="External #0", command=lambda: self.changeSensor("B3:TE0"))
        tempSensorPiHat3Menu.add_separator()
        tempSensorPiHat3Menu.add_command(label="External #1", command=lambda: self.changeSensor("B3:TE1"))
        tempSensorMenu.add_cascade(label="Pi Hat 3", menu=tempSensorPiHat3Menu)
        # Submenu for DAQCS host board
        tempSensorDaqcsMenu = tk.Menu(tempSensorMenu, tearoff=0)
        tempSensorDaqcsMenu.add_command(label="Board #0", command=lambda: self.changeSensor("B4:TB0"))
        tempSensorMenu.add_cascade(label="DAQCS Host", menu=tempSensorDaqcsMenu)
        # Submenu for COMMS board
        tempSensorCommsMenu = tk.Menu(tempSensorMenu, tearoff=0)
        tempSensorCommsMenu.add_command(label="BCM Die", command=lambda: self.changeSensor("B5:TD0"))
        tempSensorCommsMenu.add_separator()
        tempSensorCommsMenu.add_command(label="Board #0", command=lambda: self.changeSensor("B5:TB0"))
        tempSensorCommsMenu.add_separator()
        tempSensorCommsMenu.add_command(label="Balloon", command=lambda: self.changeSensor("B5:TBL"))
        tempSensorMenu.add_cascade(label="COMMS", menu=tempSensorCommsMenu)
        # Put temperature sensor menu in main menu
        self.menubar.add_cascade(label="Temp Sensors", menu=tempSensorMenu)

    def createPresSensorMenu(self):
        # Create dropdown in menu for pressure sensors
        presSensorMenu = tk.Menu(self.menubar, tearoff=0)
        # Submenu for Pi Hat 0
        presSensorPiHat0Menu = tk.Menu(presSensorMenu, tearoff=0)
        presSensorPiHat0Menu.add_command(label="Basic", command=lambda: self.changeSensor("B0:P0"))
        presSensorPiHat0Menu.add_separator()
        presSensorPiHat0Menu.add_command(label="Vacuum", command=lambda: self.changeSensor("B0:P1"))
        presSensorMenu.add_cascade(label="Pi Hat 0", menu=presSensorPiHat0Menu)
        # Submenu for Pi Hat 1
        presSensorPiHat1Menu = tk.Menu(presSensorMenu, tearoff=0)
        presSensorPiHat1Menu.add_command(label="Basic", command=lambda: self.changeSensor("B1:P0"))
        presSensorPiHat1Menu.add_separator()
        presSensorPiHat1Menu.add_command(label="Vacuum", command=lambda: self.changeSensor("B1:P1"))
        presSensorMenu.add_cascade(label="Pi Hat 1", menu=presSensorPiHat1Menu)
        # Submenu for Pi Hat 2
        presSensorPiHat2Menu = tk.Menu(presSensorMenu, tearoff=0)
        presSensorPiHat2Menu.add_command(label="Basic", command=lambda: self.changeSensor("B2:P0"))
        presSensorPiHat2Menu.add_separator()
        presSensorPiHat2Menu.add_command(label="Vacuum", command=lambda: self.changeSensor("B2:P1"))
        presSensorMenu.add_cascade(label="Pi Hat 2", menu=presSensorPiHat2Menu)
        # Submenu for Pi Hat 3
        presSensorPiHat3Menu = tk.Menu(presSensorMenu, tearoff=0)
        presSensorPiHat3Menu.add_command(label="Basic", command=lambda: self.changeSensor("B3:P0"))
        presSensorPiHat3Menu.add_separator()
        presSensorPiHat3Menu.add_command(label="Vacuum", command=lambda: self.changeSensor("B3:P1"))
        presSensorMenu.add_cascade(label="Pi Hat 3", menu=presSensorPiHat3Menu)
        # Submenu for DAQCS host board
        presSensorDaqcsMenu = tk.Menu(presSensorMenu, tearoff=0)
        presSensorDaqcsMenu.add_command(label="Basic", command= lambda: self.changeSensor("B4:P0"))
        presSensorDaqcsMenu.add_separator()
        presSensorDaqcsMenu.add_command(label="Balloon", command=lambda: self.changeSensor("B4:PB"))
        presSensorMenu.add_cascade(label="DAQCS Host", menu=presSensorDaqcsMenu)
        # Submenu for COMMS board
        presSensorCommsMenu = tk.Menu(presSensorMenu, tearoff=0)
        presSensorCommsMenu.add_command(label="Basic", command=lambda: self.changeSensor("B5:P0"))
        presSensorCommsMenu.add_separator()
        presSensorCommsMenu.add_command(label="Balloon", command=lambda: self.changeSensor("B5:PBL"))
        presSensorMenu.add_cascade(label="COMMS", menu=presSensorCommsMenu)
        # Put pressure sensor menu in main menu
        self.menubar.add_cascade(label="Pressure Sensors", menu=presSensorMenu)

    def createHumidSensorMenu(self):
        # Create dropdown menu for humidity sensors
        humidSensorMenu = tk.Menu(self.menubar, tearoff=0)
        humidSensorMenu.add_command(label="Pi Hat 0", command=lambda: self.changeSensor("B0:H"))
        humidSensorMenu.add_separator()
        humidSensorMenu.add_command(label="Pi Hat 1", command=lambda: self.changeSensor("B1:H"))
        humidSensorMenu.add_separator()
        humidSensorMenu.add_command(label="Pi Hat 2", command=lambda: self.changeSensor("B2:H"))
        humidSensorMenu.add_separator()
        humidSensorMenu.add_command(label="Pi Hat 3", command=lambda: self.changeSensor("B3:H"))
        # Add humidity sensor menu to main menu
        self.menubar.add_cascade(label="Humidity Sensors", menu=humidSensorMenu)

    def createPowerSensorMenu(self):
        # Create dropdown menu for power monitor data
        powerSensorMenu = tk.Menu(self.menubar, tearoff=0)
        # Submenu for Pi Hat 0
        powerSensorPiHat0Menu = tk.Menu(powerSensorMenu, tearoff=0)
        powerSensorPiHat0Menu.add_command(label="Voltage", command=lambda: self.changeSensor("B0:V"))
        powerSensorPiHat0Menu.add_separator()
        powerSensorPiHat0Menu.add_command(label="Current", command=lambda: self.changeSensor("B0:C"))
        powerSensorMenu.add_cascade(label="Pi Hat 0", menu=powerSensorPiHat0Menu)
        # Submenu for Pi Hat 1
        powerSensorPiHat1Menu = tk.Menu(powerSensorMenu, tearoff=0)
        powerSensorPiHat1Menu.add_command(label="Voltage", command=lambda: self.changeSensor("B1:V"))
        powerSensorPiHat1Menu.add_separator()
        powerSensorPiHat1Menu.add_command(label="Current", command=lambda: self.changeSensor("B1:C"))
        powerSensorMenu.add_cascade(label="Pi Hat 1", menu=powerSensorPiHat1Menu)
        # Submenu for Pi Hat 2
        powerSensorPiHat2Menu = tk.Menu(powerSensorMenu, tearoff=0)
        powerSensorPiHat2Menu.add_command(label="Voltage", command=lambda: self.changeSensor("B2:V"))
        powerSensorPiHat2Menu.add_separator()
        powerSensorPiHat2Menu.add_command(label="Current", command=lambda: self.changeSensor("B2:C"))
        powerSensorMenu.add_cascade(label="Pi Hat 2", menu=powerSensorPiHat2Menu)
        # Submenu for Pi Hat 3
        powerSensorPiHat3Menu = tk.Menu(powerSensorMenu, tearoff=0)
        powerSensorPiHat3Menu.add_command(label="Voltage", command=lambda: self.changeSensor("B3:V"))
        powerSensorPiHat3Menu.add_separator()
        powerSensorPiHat3Menu.add_command(label="Current", command=lambda: self.changeSensor("B3:C"))
        powerSensorMenu.add_cascade(label="Pi Hat 3", menu=powerSensorPiHat3Menu)
        # Submenu for DAQCS host board
        powerSensorDaqcsMenu = tk.Menu(powerSensorMenu, tearoff=0)
        powerSensorDaqcsMenu.add_command(label="Voltage", command=lambda: self.changeSensor("B4:V"))
        powerSensorDaqcsMenu.add_separator()
        powerSensorDaqcsMenu.add_command(label="Current", command=lambda: self.changeSensor("B4:C"))
        powerSensorMenu.add_cascade(label="DAQCS Host", menu=powerSensorDaqcsMenu)
        # Put power sensors menu in main menu
        self.menubar.add_cascade(label="Power Monitor", menu=powerSensorMenu)

    def createReactionWheelMenu(self):
        # Create dropdown menu for IMU and motor controller data
        reactionWheelMenu = tk.Menu(self.menubar, tearoff=0)
        # Submenu for IMU Data
        imuDataMenu = tk.Menu(reactionWheelMenu, tearoff=0)
        imuDataMenu.add_command(label="Gyroscope X", command=lambda: self.changeSensor("B4:XGY"))
        imuDataMenu.add_separator()
        imuDataMenu.add_command(label="Gyroscope Y", command=lambda: self.changeSensor("B4:YGY"))
        imuDataMenu.add_separator()
        imuDataMenu.add_command(label="Gyroscope Z", command=lambda: self.changeSensor("B4:ZGY"))
        imuDataMenu.add_separator()
        imuDataMenu.add_command(label="Acceleration X", command=lambda: self.changeSensor("B4:XAC"))
        imuDataMenu.add_separator()
        imuDataMenu.add_command(label="Acceleration Y", command=lambda: self.changeSensor("B4:YAC"))
        imuDataMenu.add_separator()
        imuDataMenu.add_command(label="Acceleration Z", command=lambda: self.changeSensor("B4:ZAC"))
        reactionWheelMenu.add_cascade(label="IMU Data", menu=imuDataMenu)
        # Submenu for motor controller data
        motorCtlMenu = tk.Menu(reactionWheelMenu, tearoff=0)
        motorCtlMenu.add_command(label="Motor Speed", command=lambda: self.changeSensor("B4:MS"))
        motorCtlMenu.add_separator()
        motorCtlMenu.add_command(label="Motor Current Draw", command=lambda: self.changeSensor("B4:MC"))
        motorCtlMenu.add_separator()
        motorCtlMenu.add_command(label="Motor Battery Voltage", command=lambda: self.changeSensor("B4:MV"))
        motorCtlMenu.add_separator()
        motorCtlMenu.add_command(label="Motor Direction", command=lambda: self.changeSensor("B4:MD"))
        motorCtlMenu.add_separator()
        motorCtlMenu.add_command(label="Motor Status", command=lambda: self.changeSensor("B4:ME"))
        reactionWheelMenu.add_cascade(label="Motor Controller", menu=motorCtlMenu)
        # Put reaction wheel menu in main menu
        self.menubar.add_cascade(label="Reaction Wheel", menu=reactionWheelMenu)

    def createGpsSensorMenu(self): # NOT SURE HOW GOING TO SHOW LATITUDE, LONGITUDE, TIME yet...... Need separate window or display instead of graph*****************Just display them in a separate window always
        # Create dropdown menu for GPS data
        gpsSensorMenu = tk.Menu(self.menubar, tearoff=0)
        #gpsSensorMenu.add_command(label="Latitude", command=lambda: self.changeSensor("B5:LAT"))
        #gpsSensorMenu.add_separator()
        #gpsSensorMenu.add_command(label="Longitude", command=lambda: self.changeSensor("B5:LON"))
        #gpsSensorMenu.add_separator()
        #gpsSensorMenu.add_command(label="Time", command=lambda: self.changeSensor("B5:TM"))
        #gpsSensorMenu.add_separator()
        gpsSensorMenu.add_command(label="Speed", command=lambda: self.changeSensor("B5:SPD"))
        gpsSensorMenu.add_separator()
        gpsSensorMenu.add_command(label="Altitude", command=lambda: self.changeSensor("B5:ALT"))
        # Put GPS sensor menu in main menu
        self.menubar.add_cascade(label="GPS", menu=gpsSensorMenu)

    # Change current sensor
    def changeSensor(self, sensorAbbrev):
        global sensor
        sensor = sensorAbbrev

# Frame with graph of data for the currently selected sensor
class DataGraph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Main loop
if __name__ == "__main__":
    app = graphGui()
    app.geometry("800x600")
    ani = animation.FuncAnimation(f, animate, interval=1000) #1000ms = 1s
    app.mainloop()
