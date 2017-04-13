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

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

# Graph
f = Figure()
a = f.add_subplot(111)

# Current sensor
sensor = "B0:TD0" # default to BCM die temp sensor of Pi Hat 0

# Sensor abbreviation to graph title dictionary
graphTitleTable = {
    "B0:TD0": "Pi Hat 0 BCM Die Temperature Sensor",
    "B0:TB0": "Pi Hat 0 Board Temperature Sensor #0",
    "B0:TB1": "Pi Hat 0 Board Temperature Sensor #1",
    "B0:TE0": "Pi Hat 0 External Temperature Sensor #0",
    "B0:TE1": "Pi Hat 0 External Temperature Sensor #1",
    "B1:TD0": "Pi Hat 1 BCM Die Temperature Sensor",
    "B1:TB0": "Pi Hat 1 Board Temperature Sensor #0",
    "B1:TB1": "Pi Hat 1 Board Temperature Sensor #1",
    "B1:TE0": "Pi Hat 1 External Temperature Sensor #0",
    "B1:TE1": "Pi Hat 1 External Temperature Sensor #1",
    "B2:TD0": "Pi Hat 2 BCM Die Temperature Sensor",
    "B2:TB0": "Pi Hat 2 Board Temperature Sensor #0",
    "B2:TB1": "Pi Hat 2 Board Temperature Sensor #1",
    "B2:TE0": "Pi Hat 2 External Temperature Sensor #0",
    "B2:TE1": "Pi Hat 2 External Temperature Sensor #1",
    "B3:TD0": "Pi Hat 3 BCM Die Temperature Sensor",
    "B3:TB0": "Pi Hat 3 Board Temperature Sensor #0",
    "B3:TB1": "Pi Hat 3 Board Temperature Sensor #1",
    "B3:TE0": "Pi Hat 3 External Temperature Sensor #0",
    "B3:TE1": "Pi Hat 3 External Temperature Sensor #1",
    "B4:TB0": "DAQCS Board Temperature Sensor #0",
    "B5:TD0": "COMMS Board BCM Die Temperature Sensor",
    "B5:TB0": "COMMS Board Temperature Sensor #0",
    "B0:P0": "Pi Hat 0 Basic Pressure Sensor",
    "B0:P1": "Pi Hat 0 Vacuum Pressure Sensor",
    "B1:P0": "Pi Hat 1 Basic Pressure Sensor",
    "B1:P1": "Pi Hat 1 Vacuum Pressure Sensor",
    "B2:P0": "Pi Hat 2 Basic Pressure Sensor",
    "B2:P1": "Pi Hat 2 Vacuum Pressure Sensor",
    "B3:P0": "Pi Hat 3 Basic Pressure Sensor",
    "B3:P1": "Pi Hat 3 Vacuum Pressure Sensor",
    "B4:PO": "DAQCS Board Basic Pressure Sensor",
    "B4:PB": "Balloon Pressure Sensor",
    "B5:P0": "COMMS Board Basic Pressure Sensor",
    "B0:H": "Pi Hat 0 Humidity Sensor",
    "B1:H": "Pi Hat 1 Humidity Sensor",
    "B2:H": "Pi Hat 2 Humidity Sensor",
    "B3:H": "Pi Hat 3 Humidity Sensor",
    "B0:V": "Pi Hat 0 Power Monitor - Supply Voltage",
    "B0:C": "Pi Hat 0 Power Monitor - Supply Current",
    "B1:V": "Pi Hat 1 Power Monitor - Supply Voltage",
    "B1:C": "Pi Hat 1 Power Monitor - Supply Current",
    "B2:V": "Pi Hat 2 Power Monitor - Supply Voltage",
    "B2:C": "Pi Hat 2 Power Monitor - Supply Current",
    "B3:V": "Pi Hat 3 Power Monitor - Supply Voltage",
    "B3:C": "Pi Hat 3 Power Monitor - Supply Current",
    "B4:V": "DAQCS Board Power Monitor - Supply Voltage",
    "B4:C": "DAQCS Board Power Monitor - Supply Current",
    "B4:XGY": "IMU Gyroscope X (Angular Velocity)",
    "B4:XAC": "IMU Acceleration X",
    "B4:YGY": "IMU Gyroscope Y (Angular Velocity)",
    "B4:YAC": "IMU Acceleration Y",
    "B4:ZGY": "IMU Gyroscope Z (Angular Velocity)",
    "B4:ZAC": "IMU Acceleration Z",
    "B4:MS": "Motor Speed",
    "B4:MC": "Motor Current Draw",
    "B4:MV": "Motor Battery Voltage",
    "B4:MD": "Motor Direction (1=CW, 0=CCW)",
    "B4:ME": "Motor Status (1=ON, 0=OFF)",
    "B5:LAT": "GPS - Latitude",
    "B5:LON": "GPS - Longitude",
    "B5:TM": "GPS - Time",
    "B5:SPD": "GPS - Speed",
    "B5:ALT": "GPS - Altitude",
}

# Add the data of the currently selected sensor to a graph in the frame
def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)

    title = graphTitleTable.get(sensor, "ERROR with sensor value")
    a.set_title(title)

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

    def createGpsSensorMenu(self): # NOT SURE HOW GOING TO SHOW LATITUDE, LONGITUDE, TIME yet...... Need separate window or display instead of graph*****************
        # Create dropdown menu for GPS data
        gpsSensorMenu = tk.Menu(self.menubar, tearoff=0)
        gpsSensorMenu.add_command(label="Latitude", command=lambda: self.changeSensor("B5:LAT"))
        gpsSensorMenu.add_separator()
        gpsSensorMenu.add_command(label="Longitude", command=lambda: self.changeSensor("B5:LON"))
        gpsSensorMenu.add_separator()
        gpsSensorMenu.add_command(label="Time", command=lambda: self.changeSensor("B5:TM"))
        gpsSensorMenu.add_separator()
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
    ani = animation.FuncAnimation(f, animate, interval=1000)
    app.mainloop()
