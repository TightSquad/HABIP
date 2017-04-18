# Need to install six
# Need to install pillow

# Help with map window code from: http://hci574.blogspot.com/2010/04/using-google-maps-static-images.html
# Image updating code based on: http://stackoverflow.com/questions/23969883/tkinter-changing-image-on-a-canvas

from motionless import DecoratedMap, LatLonMarker
import urllib
from Tkinter import *
from PIL import Image
from PIL import ImageTk

import time

class MapWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.caption = Label(self, text="Hi")
        self.caption.pack()

        self.initMap()
        self.image = ImageTk.PhotoImage(self.im)
        self.image_label = Label(self, image=self.image, bd=0)
        self.image_label.pack()
        self.pack(side="top", fill="both", expand=True)

        self.dataLines = 0

        self.id = self.after(1000, self.mapLoop)

    def initMap(self):
        self.fileName = "/home/spex/habipMapStart.jpg"

        # Generate map URL
        self.map = DecoratedMap(key="AIzaSyDzElKnTJkAewIuxuAUZJYmRfXz1mg0vYU")
        # Add marker for Meteor Lab to start at
        self.map.add_marker(LatLonMarker(lat=43.08463,lon=-77.67914))
        self.map.add_path_latlon(lat=43.08463,lon=-77.67914)
        self.requestUrl = self.map.generate_url()

        # Save image to disk
        urllib.urlretrieve(self.requestUrl, self.fileName)
        self.im = Image.open(self.fileName)

    def mapLoop(self):
        self.latList = []
        self.lonList = []

        # Open data file and split up each line
        sensorData = open("/home/spex/habip_data.log","r").read()
        dataList = sensorData.split("\n")

        # Just continue if there is new data (if dataList length changed)
        if len(dataList) > self.dataLines:
            self.dataLines = len(dataList)
                
            # Loop through file lines
            for eachLine in dataList:
                if len(eachLine) > 0:
                    lineData = eachLine.split(",") # Sensor data is comma separated

                    # Grab latitude and longitude
                    lat = lineData[60] # N (+) or S (-)
                    lon = lineData[61] # E (+) or W (-)

                    # Just continue if there is data present
                    if (lat != "NULL") and (lon != "NULL"):
                        # Change latitude and longitude to be +- instead of direction
                        if lat[-1] == "N":
                            lat = lat[:-1]
                        elif lat[-1] == "S":
                            lat = "-" + lat[:-1]
                        if lon[-1] == "E":
                            lon = lon[:-1]
                        elif lon[-1] == "W":
                            lon = "-" + lon[:-1]

                        # Add latitude and longitude to lists
                        self.latList.append(lat)
                        self.lonList.append(lon)

            self.updateImage()

        self.id = self.after(1000,self.mapLoop) # Keep checking for more data (keep re-calling this function) every 1000ms

    def updateImage(self):
        self.fileName = "/home/spex/habipMapUpdated.jpg"

        # Generate map URL
        self.map = DecoratedMap(key="AIzaSyDzElKnTJkAewIuxuAUZJYmRfXz1mg0vYU")
        for lat, lon in zip(self.latList,self.lonList):
            self.map.add_marker(LatLonMarker(lat=lat,lon=lon))
            self.map.add_path_latlon(lat=lat,lon=lon)
        self.requestUrl = self.map.generate_url()

        # Save image to disk
        urllib.urlretrieve(self.requestUrl, self.fileName)
        
        self.im.close()
        self.im = Image.open(self.fileName)
        self.image = ImageTk.PhotoImage(self.im)
        self.image_label.configure(image=self.image)

# Main loop
if __name__ == "__main__":
    # Make map window
    mapWin = Tk()
    mapWin.title("Telemetry GPS Data Tracking")
    mapWin.frame = MapWindow(mapWin)
    mapWin.mainloop()
