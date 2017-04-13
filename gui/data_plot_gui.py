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
        # Put submenus in temperature sensor menu
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
        # Put submenus in pressure sensor menu
        self.menubar.add_cascade(label="Pres Sensors", menu=presSensorMenu)

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
