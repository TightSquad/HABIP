import Tkinter # Needed to create the GUI
import time # Needed to get timestamps
import logging # Needed for creating command log file
import subprocess # Needed for calling soundmodem's beacon command to transmit commands

# Main command GUI class
class MyApp(Tkinter.Frame):
    # Create camera number selection buttons
    def createCamSelect(self):
        self.camSelFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.camSelButton = Tkinter.Button(self.camSelFrame, text="Camera Number", command=lambda: self.camSelectionMade()).grid(row=0,column=5)
        self.camSelVal = Tkinter.IntVar()
        Tkinter.Radiobutton(self.camSelFrame, text="CAM0", variable=self.camSelVal, value=0).grid(row=0,column=6)
        Tkinter.Radiobutton(self.camSelFrame, text="CAM1", variable=self.camSelVal, value=1).grid(row=0,column=7)
        Tkinter.Radiobutton(self.camSelFrame, text="CAM2", variable=self.camSelVal, value=2).grid(row=0,column=8)
        Tkinter.Radiobutton(self.camSelFrame, text="CAM3", variable=self.camSelVal, value=3).grid(row=0,column=9)
        #root.grid_rowconfigure(1, weight=1)
        self.camSelFrame.grid()

    # Add camera selection command to command list to be sent
    def camSelectionMade(self):
        # Camera source dictionary (button value->command string)
        camSelTable = {
            0: "CAM:0",
            1: "CAM:1",
            2: "CAM:2",
            3: "CAM:3",
        }

        self.camSelCmdString = camSelTable.get(self.camSelVal.get(),"CAM:0")
        self.addToCmdDisplay(self.camSelCmdString)

    # Create OSD temp sensor source select buttons
    def createOsdTempSelect(self):
        self.osdTempFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.osdTempSelVal = Tkinter.IntVar()
        self.osdTempButton = Tkinter.Button(self.osdTempFrame, text="OSD Temp Source", command=lambda: self.osdTempSelectionMade())
        self.osdTempButton.grid(row=4,column=0)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi0 BCM Die", variable=self.osdTempSelVal, value=1).grid(row=2,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi0 Board 0", variable=self.osdTempSelVal, value=2).grid(row=3,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi0 Board 1", variable=self.osdTempSelVal, value=3).grid(row=4,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi0 Ext. 0", variable=self.osdTempSelVal, value=4).grid(row=5,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi0 Ext. 1", variable=self.osdTempSelVal, value=5).grid(row=6,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi1 BCM Die", variable=self.osdTempSelVal, value=6).grid(row=2,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi1 Board 0", variable=self.osdTempSelVal, value=7).grid(row=3,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi1 Board 1", variable=self.osdTempSelVal, value=8).grid(row=4,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi1 Ext. 0", variable=self.osdTempSelVal, value=9).grid(row=5,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi1 Ext. 1", variable=self.osdTempSelVal, value=10).grid(row=6,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi2 BCM Die", variable=self.osdTempSelVal, value=11).grid(row=2,column=3, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi2 Board 0", variable=self.osdTempSelVal, value=12).grid(row=3,column=3, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi2 Board 1", variable=self.osdTempSelVal, value=13).grid(row=4,column=3, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi2 Ext. 0", variable=self.osdTempSelVal, value=14).grid(row=5,column=3, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi2 Ext. 1", variable=self.osdTempSelVal, value=15).grid(row=6,column=3, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi3 BCM Die", variable=self.osdTempSelVal, value=16).grid(row=2,column=4, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi3 Board 0", variable=self.osdTempSelVal, value=17).grid(row=3,column=4, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi3 Board 1", variable=self.osdTempSelVal, value=18).grid(row=4,column=4, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi3 Ext. 0", variable=self.osdTempSelVal, value=19).grid(row=5,column=4, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="Pi3 Ext. 1", variable=self.osdTempSelVal, value=20).grid(row=6,column=4, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="DAQCS Board", variable=self.osdTempSelVal, value=21).grid(row=2,column=5, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="COMMS BCM Die", variable=self.osdTempSelVal, value=22).grid(row=3,column=5, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdTempFrame, text="COMMS Board", variable=self.osdTempSelVal, value=23).grid(row=4,column=5, sticky=Tkinter.W)
        self.osdTempFrame.grid()

    # Add OSD temp sensor source select to command list to be sent
    def osdTempSelectionMade(self):
        # OSD temp sensor source dictionary (button value->command string)
        osdTempSelTable = {
            1: "OSD:TEMP:B0:TD0",
            2: "OSD:TEMP:B0:TB0",
            3: "OSD:TEMP:B0:TB1",
            4: "OSD:TEMP:B0:TE0",
            5: "OSD:TEMP:B0:TE1",
            6: "OSD:TEMP:B1:TD0",
            7: "OSD:TEMP:B1:TB0",
            8: "OSD:TEMP:B1:TB1",
            9: "OSD:TEMP:B1:TE0",
            10: "OSD:TEMP:B1:TE1",
            11: "OSD:TEMP:B2:TD0",
            12: "OSD:TEMP:B2:TB0",
            13: "OSD:TEMP:B2:TB1",
            14: "OSD:TEMP:B2:TE0",
            15: "OSD:TEMP:B2:TE1",
            16: "OSD:TEMP:B3:TD0",
            17: "OSD:TEMP:B3:TB0",
            18: "OSD:TEMP:B3:TB1",
            19: "OSD:TEMP:B3:TE0",
            20: "OSD:TEMP:B3:TE1",
            21: "OSD:TEMP:B4:TB0",
            22: "OSD:TEMP:B5:TD0",
            23: "OSD:TEMP:B5:TB0",
        }

        self.osdTempSelCmdString = osdTempSelTable.get(self.osdTempSelVal.get(),"OSD:TEMP:B0:TD0")
        self.addToCmdDisplay(self.osdTempSelCmdString)

    # Create OSD pressure sensor source select buttons
    def createOsdPresSelect(self):
        self.osdPresFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.osdPresSelVal = Tkinter.IntVar()
        self.osdPresButton = Tkinter.Button(self.osdPresFrame, text="OSD Pres Source", command=lambda: self.osdPresSelectionMade())
        self.osdPresButton.grid(row=9,column=0)
        Tkinter.Radiobutton(self.osdPresFrame, text="Pi0 Basic", variable=self.osdPresSelVal, value=1).grid(row=8,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="Pi0 Vacuum", variable=self.osdPresSelVal, value=2).grid(row=9,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="Pi1 Basic", variable=self.osdPresSelVal, value=3).grid(row=10,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="Pi1 Vacuum", variable=self.osdPresSelVal, value=4).grid(row=11,column=1, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="Pi2 Basic", variable=self.osdPresSelVal, value=5).grid(row=8,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="Pi2 Vacuum", variable=self.osdPresSelVal, value=6).grid(row=9,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="Pi3 Basic", variable=self.osdPresSelVal, value=7).grid(row=10,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="Pi3 Vacuum", variable=self.osdPresSelVal, value=8).grid(row=11,column=2, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="DAQCS Basic", variable=self.osdPresSelVal, value=9).grid(row=8,column=3, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="Balloon", variable=self.osdPresSelVal, value=10).grid(row=9,column=3, sticky=Tkinter.W)
        Tkinter.Radiobutton(self.osdPresFrame, text="COMMS Basic", variable=self.osdPresSelVal, value=11).grid(row=10,column=3, sticky=Tkinter.W)
        self.osdPresFrame.grid()

    # Add OSD pressure sensor source select to command list to be sent
    def osdPresSelectionMade(self):
        # OSD pressure sensor source dictionary (button value->command string)
        osdPresSelTable = {
            1: "OSD:PRES:B0:P0",
            2: "OSD:PRES:B0:P1",
            3: "OSD:PRES:B1:P0",
            4: "OSD:PRES:B1:P1",
            5: "OSD:PRES:B2:P0",
            6: "OSD:PRES:B2:P1",
            7: "OSD:PRES:B3:P0",
            8: "OSD:PRES:B3:P1",
            9: "OSD:PRES:B4:P0",
            10: "OSD:PRES:B4:PB",
            11: "OSD:PRES:B5:P0",
        }

        self.osdPresSelCmdString = osdPresSelTable.get(self.osdPresSelVal.get(),"OSD:PRES:B0:P0")
        self.addToCmdDisplay(self.osdPresSelCmdString)

    # Create OSD humidity sensor source select buttons
    def createOsdHumidSelect(self):
        self.osdHumidSelFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.osdHumidButton = Tkinter.Button(self.osdHumidSelFrame, text="OSD Humid Source", command=lambda: self.osdHumidSelectionMade()).grid(row=13,column=5)
        self.osdHumidSelVal = Tkinter.IntVar()
        Tkinter.Radiobutton(self.osdHumidSelFrame, text="Pi0", variable=self.osdHumidSelVal, value=0).grid(row=13,column=6)
        Tkinter.Radiobutton(self.osdHumidSelFrame, text="Pi1", variable=self.osdHumidSelVal, value=1).grid(row=13,column=7)
        Tkinter.Radiobutton(self.osdHumidSelFrame, text="Pi2", variable=self.osdHumidSelVal, value=2).grid(row=13,column=8)
        Tkinter.Radiobutton(self.osdHumidSelFrame, text="Pi3", variable=self.osdHumidSelVal, value=3).grid(row=13,column=9)
        self.osdHumidSelFrame.grid()

    # Add OSD humidity sensor source select to command list to be sent
    def osdHumidSelectionMade(self):
        # OSD humidity sensor source dictionary (button value->command string)
        osdHumidSelTable = {
            0: "OSD:HUM:B0",
            1: "OSD:HUM:B1",
            2: "OSD:HUM:B2",
            3: "OSD:HUM:B3",
        }

        self.osdHumidSelCmdString = osdHumidSelTable.get(self.osdHumidSelVal.get(),"OSD:HUM:B0")
        self.addToCmdDisplay(self.osdHumidSelCmdString)

    # Create OSD power control portion of GUI
    def createOsdPowerControl(self):
        self.osdPwrCtlFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.osdPwrCtlLabel = Tkinter.Label(self.osdPwrCtlFrame, text="OSD Power Control:")
        self.osdPwrCtlLabel.grid(row=15,column=0)
        self.osdPwrOnButton = Tkinter.Button(self.osdPwrCtlFrame, text="ON", command=lambda: self.osdPwrCtlSelectionMade(0)).grid(row=15,column=1)
        self.osdPwrOffButton = Tkinter.Button(self.osdPwrCtlFrame, text="OFF", command=lambda: self.osdPwrCtlSelectionMade(1)).grid(row=15,column=2)
        self.osdPwrRstButton = Tkinter.Button(self.osdPwrCtlFrame, text="RESET", command=lambda: self.osdPwrCtlSelectionMade(2)).grid(row=15,column=3)
        self.osdPwrCtlFrame.grid()

    # Add OSD power control button select to command list to be sent
    def osdPwrCtlSelectionMade(self,argument=0):
        # OSD power control command string dictionary (button value->command string)
        osdPwrCtlTable = {
            0: "OSD:ON",
            1: "OSD:OFF",
            2: "OSD:RST",
        }

        self.osdPwrCtlCmdString = osdPwrCtlTable.get(argument,"OSD:ON")
        self.addToCmdDisplay(self.osdPwrCtlCmdString)

    # Create reaction wheel control portion of GUI
    def createRxnWheelControl(self):
        self.rxnWhlCtlFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.rxnWhlPwrCtlLabel = Tkinter.Label(self.rxnWhlCtlFrame, text="Reaction Wheel Power Control:")
        self.rxnWhlPwrCtlLabel.grid(row=17,column=0)
        self.rxnWhlDirection = Tkinter.IntVar()
        self.rxnWhlDegrees = Tkinter.IntVar()
        self.rxnWhlOnButton = Tkinter.Button(self.rxnWhlCtlFrame, text="ON", command=lambda: self.rxnWhlPwrCtlSelectionMade(0)).grid(row=17,column=1)
        self.rxnWhlOffButton = Tkinter.Button(self.rxnWhlCtlFrame, text="OFF", command=lambda: self.rxnWhlPwrCtlSelectionMade(1)).grid(row=17,column=2)
        self.rxnWhlTurnCtlLabel = Tkinter.Label(self.rxnWhlCtlFrame, text="Reaction Wheel Turn Control:")
        self.rxnWhlTurnCtlLabel.grid(row=17,column=3)
        self.rxnWhlTurnButton = Tkinter.Button(self.rxnWhlCtlFrame, text="Turn", command=lambda: self.rxnWhlTurnSelectionMade(self.rxnWhlDirection.get(),self.rxnWhlDegrees.get())).grid(row=17,column=4)
        Tkinter.Radiobutton(self.rxnWhlCtlFrame, text="CW Direction", variable=self.rxnWhlDirection, value=0).grid(row=17,column=5)
        Tkinter.Radiobutton(self.rxnWhlCtlFrame, text="CCW Direction", variable=self.rxnWhlDirection, value=1).grid(row=18,column=5)
        #self.rxnWhlDegSlide = Tkinter.Scale(self.rxnWhlCtlFrame, from_=0, to=180, orient=Tkinter.HORIZONTAL, label="Degrees to Turn", variable=self.rxnWhlDegrees)
        #self.rxnWhlDegSlide.set(0)
        #self.rxnWhlDegSlide.grid(row=17,column=6)
        self.rxnWhlDegLabel = Tkinter.Label(self.rxnWhlCtlFrame, text="Degrees to Turn (0-180):")
        self.rxnWhlDegLabel.grid(row=17,column=6)
        self.rxnWhlDegEntry = Tkinter.Entry(self.rxnWhlCtlFrame, textvariable=self.rxnWhlDegrees, width=5)
        self.rxnWhlDegEntry.grid(row=18,column=6)
        self.rxnWhlCtlFrame.grid()

    # Check the reaction wheel degree entry value
    def rxnWhlDegCheck(self,argument=0):
        if ((argument>=0) and (argument<=180)):
            print "returning true"
            return True
        else:
            print "returning false"
            return False

    # Add reaction wheel power control button select to command list to be sent
    def rxnWhlPwrCtlSelectionMade(self,argument=0):
        # Reaction wheel power control command string dictionary (button value->command string)
        rxnWhlPwrCtlTable = {
            0: "RW:ON",
            1: "RW:OFF",
        }

        self.rxnWhlPwrCtlString = rxnWhlPwrCtlTable.get(argument,"RW:OFF")
        self.addToCmdDisplay(self.rxnWhlPwrCtlString)

    # Add reaction wheel turn control selection to command list to be sent
    def rxnWhlTurnSelectionMade(self,direction=0,degrees=0):
    	if(degrees>=0 and degrees<=180): # make sure valid degrees avlue
            if direction == 1:
                self.rxnWhlTurnCtlString = "RW:CCW," + str(degrees)
            else:
                self.rxnWhlTurnCtlString = "RW:CW," + str(degrees)
            self.addToCmdDisplay(self.rxnWhlTurnCtlString)
        else:
            self.errorMsg("Invalid rxn wheel degrees value")

    # Create board reset command portion of GUI
    def createBoardResetControl(self):
        self.boardRstFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.boardRstLabel = Tkinter.Label(self.boardRstFrame, text="Board Reset Control:")
        self.boardRstLabel.grid(row=20,column=0)
        self.boardRstBoardVal = Tkinter.IntVar()
        self.boardRstButton = Tkinter.Button(self.boardRstFrame, text="RESET", command=lambda: self.boardRstSelectionMade(self.boardRstBoardVal.get())).grid(row=20,column=1)
        Tkinter.Radiobutton(self.boardRstFrame, text="Pi0", variable=self.boardRstBoardVal, value=0).grid(row=20,column=2)
        Tkinter.Radiobutton(self.boardRstFrame, text="Pi1", variable=self.boardRstBoardVal, value=1).grid(row=20,column=3)
        Tkinter.Radiobutton(self.boardRstFrame, text="Pi2", variable=self.boardRstBoardVal, value=2).grid(row=20,column=4)
        Tkinter.Radiobutton(self.boardRstFrame, text="Pi3", variable=self.boardRstBoardVal, value=3).grid(row=20,column=5)
        self.boardRstFrame.grid()

    # Add board reset control button select to command list to be sent
    def boardRstSelectionMade(self,argument=0):
        # Board reset power control command string dictionary (button value->command string)
        piRstCtlTable = {
            0: "RST:B0",
            1: "RST:B1",
            2: "RST:B2",
            3: "RST:B3",
        }

        self.piRstCtlString = piRstCtlTable.get(argument,"RST:B0")
        self.addToCmdDisplay(self.piRstCtlString)

    # Create ATV power control command portion of GUI
    def createAtvPwrControl(self):
        self.atvPwrCtlFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.atvPwrCtlLabel = Tkinter.Label(self.atvPwrCtlFrame, text="ATV Output Power (Watts):")
        self.atvPwrCtlLabel.grid(row=22,column=0)
        self.atvPwrCtlVal = Tkinter.DoubleVar()
        self.atvPwrCtlButton = Tkinter.Button(self.atvPwrCtlFrame, text="Update", command=lambda: self.atvPwrCtlSelectionMade(self.atvPwrCtlVal.get())).grid(row=22,column=1)
        self.atvPwrCtlSlide = Tkinter.Scale(self.atvPwrCtlFrame, from_=0.5, to=5.0, resolution = 0.5, orient=Tkinter.HORIZONTAL, variable=self.atvPwrCtlVal)
        self.atvPwrCtlSlide.set(1.5)
        self.atvPwrCtlSlide.grid(row=22,column=2)
        self.atvPwrCtlFrame.grid()

    # Add ATV power control selection to command list to be sent
    def atvPwrCtlSelectionMade(self,argument=1.5):
        self.atvPwrCtlString = "ATV:PWR:" + str(argument)
        self.addToCmdDisplay(self.atvPwrCtlString)

    # Send computer time (seconds since Linux epoch for time value)
    def createTimeSyncButton(self):
        self.timeSyncFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.timeSyncLabel = Tkinter.Label(self.timeSyncFrame, text="Send time for data logging sync purposes:")
        self.timeSyncLabel.grid(row=24,column=0)
        self.timeSyncButton = Tkinter.Button(self.timeSyncFrame, text="Update", command=lambda: self.timeSyncSelectionMade()).grid(row=24,column=1)
        self.timeSyncFrame.grid()

    # Add time sync to command list to be sent
    def timeSyncSelectionMade(self):
        epoch_time = int(time.time())
        self.timeSyncString = "TIME:" + str(epoch_time)
        self.addToCmdDisplay(self.timeSyncString)

    # Create cutdown button in GUI
    def createCutdownButton(self):
        self.cutdownFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.cutdownLabel = Tkinter.Label(self.cutdownFrame, text="Cut down balloon (select both boxes and press the button):")
        self.cutdownLabel.grid(row=26,column=0)
        self.cutdownVal1 = Tkinter.IntVar()
        self.cutdownVal2 = Tkinter.IntVar()
        self.cutdownButton = Tkinter.Button(self.cutdownFrame, text="CUT", command=lambda: self.cutdownSelectionMade(self.cutdownVal1.get(),self.cutdownVal2.get())).grid(row=26,column=1)
        Tkinter.Checkbutton(self.cutdownFrame, text="Check if sure", variable=self.cutdownVal1).grid(row=26, column=2)
        Tkinter.Checkbutton(self.cutdownFrame, text="Check if sure", variable=self.cutdownVal2).grid(row=26, column=3)
        self.cutdownFrame.grid()

    # Add cut down to command list to be sent if really sure
    def cutdownSelectionMade(self,check1=0,check2=0):
        if ((check1==1)and(check2==1)):
            self.cutdownString = "CUTDOWN"

            # Platform needs to see the command twice in a row
            self.addToCmdDisplay(self.cutdownString)
            self.addToCmdDisplay(self.cutdownString)

    # Create a text box display to show the command strings selected
    def createCmdStringDisplay(self):
        self.cmdStringFrame = Tkinter.Frame(root, bd=2, relief=Tkinter.SUNKEN)
        self.cmdBoxScroll = Tkinter.Scrollbar(self.cmdStringFrame)
        self.cmdStringTextBox = Tkinter.Text(self.cmdStringFrame, height=3, width=100)
        self.cmdStringTextBox.grid(row=28,column=2)
        self.cmdBoxScroll.grid(row=28,column=3, sticky="ns")
        self.cmdBoxScroll.config(command=self.cmdStringTextBox.yview)
        self.cmdStringTextBox.config(yscrollcommand=self.cmdBoxScroll.set)
        self.cmdStringTextLabel = Tkinter.Label(self.cmdStringFrame, text="Command Queue:")
        self.cmdStringTextLabel.grid(row=28,column=0)
        self.cmdSendButton = Tkinter.Button(self.cmdStringFrame, text="Send", command=lambda: self.sendCommands())
        self.cmdSendButton.grid(row=28,column=1)
        self.cmdBackButton = Tkinter.Button(self.cmdStringFrame, text="Back", command=lambda: self.removeLastCommand())
        self.cmdBackButton.grid(row=28,column=4)
        self.cmdClearButton = Tkinter.Button(self.cmdStringFrame, text="Clear", command=lambda: self.clearCommands())
        self.cmdClearButton.grid(row=28,column=5)
        self.cmdStringFrame.grid()

    # Add a command string to the text box display of commands and add it to the command list
    def addToCmdDisplay(self, argument=""):
        # Add command string to the command list
        self.commandList.append(argument)

        # Update display
        self.updateCmdDisplay()

    # Update command string text box display
    def updateCmdDisplay(self):
        # Clear out old text box contents and add latest string
        self.cmdStringTextBox.delete(1.0,Tkinter.END)

        # Update command string based on command list
        self.commandString = ";".join(self.commandList)

        # Update command string in display box
        self.cmdStringTextBox.insert(Tkinter.END,self.commandString)

    # Create a text box display to show error messages
    # Also create a text box to manually enter commands into
    def createErrorAndManualDisplay(self):
    	self.bottomFrame = Tkinter.Frame(root, bd=2)

    	# Error Message Box
        self.errorStringFrame = Tkinter.Frame(self.bottomFrame, bd=2, relief=Tkinter.SUNKEN)
        self.errorBoxScroll = Tkinter.Scrollbar(self.errorStringFrame)
        self.errorStringTextBox = Tkinter.Text(self.errorStringFrame, height=5, width=50)
        self.errorStringTextBox.grid(row=30,column=1)
        self.errorBoxScroll.grid(row=30,column=2, sticky="ns")
        self.errorBoxScroll.config(command=self.errorStringTextBox.yview)
        self.errorStringTextBox.config(yscrollcommand=self.errorBoxScroll.set)
        self.errorStringTextLabel = Tkinter.Label(self.errorStringFrame, text="Errors:")
        self.errorStringTextLabel.grid(row=30,column=0)
        self.errorMsgClearButton = Tkinter.Button(self.errorStringFrame, text="Clear Errors", command=lambda: self.clearErrors())
        self.errorMsgClearButton.grid(row=30,column=3)
        self.errorStringFrame.grid(row=30,column=0)

        # Manual Command Entry Box
        self.manualCmdFrame = Tkinter.Frame(self.bottomFrame, bd=2, relief=Tkinter.SUNKEN)
        self.manualCmdLabel = Tkinter.Label(self.manualCmdFrame, text="Manually Enter a Command:")
        self.manualCmdLabel.grid(row=30,column=7)
        self.manualCmd = Tkinter.StringVar()
        self.manualCmdEntry = Tkinter.Entry(self.manualCmdFrame, textvariable=self.manualCmd, width=20)
        self.manualCmdEntry.grid(row=30,column=8)
        self.manualCmdButton = Tkinter.Button(self.manualCmdFrame, text="Go", command=lambda: self.addManualCommand(self.manualCmd.get()))
        self.manualCmdButton.grid(row=30,column=9)
        self.manualCmdFrame.grid(row=30,column=2)

        self.bottomFrame.grid()

    # Print and show error message
    def errorMsg(self, argument=""):
        print argument
        self.updateErrorDisplay(argument)

    # Add error string to text box of error messages
    def updateErrorDisplay(self, argument=""):
        self.errorStringTextBox.insert(Tkinter.END,argument+"\n")

    # Clear error message text box
    def clearErrors(self):
        self.errorStringTextBox.delete(1.0,Tkinter.END)

    # Deal with a manually entered command
    def addManualCommand(self, command=""):
        # Check if valid command
        if command in self.validCommandList:
            # Add the command to the command queue
            self.addToCmdDisplay(command)
        else:
            if command[:6] == "RW:CW,":
                # Add the command to the command queue if valid degrees value for reaction wheel to turn
                degreesVal = int(command[6:])
                if (degreesVal>=0 and degreesVal<=180):
                    # Add the command to the command queue
                    self.addToCmdDisplay(command)
                else:
                    self.errorMsg("Invalid degrees value for manual RW:CW,# command")
            elif command[:7] == "RW:CCW,":
                # Add the command to the command queue if valid degrees value for reaction wheel to turn
                degreesVal = int(command[7:])
                if (degreesVal>=0 and degreesVal<=180):
                    # Add the command to the command queue
                    self.addToCmdDisplay(command)
                else:
                    self.errorMsg("Invalid degrees value for manual RW:CCW,# command")
            elif command[:5] == "TIME:":
                # Assume the time value given is correct *************************************************************
                # Add the command to the command queue
                self.addToCmdDisplay(command)
            else:
                self.errorMsg("Invalid manual command entered")

        # Clear contents of Manual Command Entry box
        self.manualCmdEntry.delete(0,Tkinter.END)

    # Send commands listed in self.commandString
    def sendCommands(self):
        # Update command string based on command list
        #self.commandString = ";".join(self.commandList)

        # Create a new version of the command string that includes command number
        #    Each command should have a 4 digit (4 ASCII characters) number in front of it
        #    Increment this number as commands are sent
        #    Need to make sure only transmit a max of 256 characters at a time
        finalCommandString = ""
        finalCommandStringList = []
        for commandNumber in range(0, len(self.commandList)):
            tempCommandString = "%04d"%(self.commandSentNumber) + ":" + self.commandList[commandNumber] + ";"
            self.commandSentNumber += 1

            # Add the command string to a list if it is going to be too long to send and start a new string
            if ((len(finalCommandString)+len(tempCommandString))>256):
                finalCommandStringList.append(finalCommandString)
                finalCommandString = ""
                finalCommandString += tempCommandString
            # Add the command string to the list if it is the last
            elif (commandNumber==(len(self.commandList)-1)):
                finalCommandString += tempCommandString
                finalCommandStringList.append(finalCommandString)
            else:
                finalCommandString += tempCommandString

        # Go through finalCommandStringList and transmit the elements
        for commandStringToSend in finalCommandStringList:
            # Add commands to be sent to command log file
            self.commandLogger.info(commandStringToSend)

            # Call beacon in Linux to transmit command(s)
            subprocess.call(["beacon","-s","sm0",commandStringToSend])

            # Sleep between transmissions
            time.sleep(1) # 1 second

        # Clear commands once done sending
        self.clearCommands()

    # Remove last command from command "queue"
    def removeLastCommand(self):
        # Remove last command from command list
        self.commandList.pop()

        # Update display
        self.updateCmdDisplay()

    # Clear commands from command "queue"
    def clearCommands(self):
        # Remove commands from the command list
        self.commandList = []

        # Remove commands from the command string
        self.commandString = ""

        # Remove commands from display box
        self.cmdStringTextBox.delete(1.0,Tkinter.END)

    # Create the command GUI
    def createGUI(self):
        self.createCamSelect()
        self.createOsdTempSelect()
        self.createOsdPresSelect()
        self.createOsdHumidSelect()
        self.createOsdPowerControl()
        self.createRxnWheelControl()
        self.createBoardResetControl()
        self.createAtvPwrControl()
        self.createTimeSyncButton()
        self.createCutdownButton()
        self.createCmdStringDisplay()
        self.createErrorAndManualDisplay()

    # Class initialization
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.grid() # Grid placement method of Tkinter widgets
        self.commandString = "" # String for commands being queued up to send
        self.commandList = [] # Keep a list of the commands being queued up to send
        self.commandSentNumber = 0 # Keep track of how many commands have been sent

        # List valid commands
        self.validCommandList = ["CAM:0","CAM:1","CAM:2","CAM:3","OSD:TEMP:B0:TD0","OSD:TEMP:B0:TB0","OSD:TEMP:B0:TB1","OSD:TEMP:B0:TE0","OSD:TEMP:B0:TE1","OSD:TEMP:B1:TD0"]
        self.validCommandList.extend(["OSD:TEMP:B1:TB0","OSD:TEMP:B1:TB1","OSD:TEMP:B1:TE0","OSD:TEMP:B1:TE1","OSD:TEMP:B2:TD0","OSD:TEMP:B2:TB0","OSD:TEMP:B2:TB1","OSD:TEMP:B2:TE0"])
        self.validCommandList.extend(["OSD:TEMP:B2:TE1","OSD:TEMP:B3:TD0","OSD:TEMP:B3:TB0","OSD:TEMP:B3:TB1","OSD:TEMP:B3:TE0","OSD:TEMP:B3:TE1","OSD:TEMP:B4:TB0","OSD:TEMP:B5:TD0"])
        self.validCommandList.extend(["OSD:TEMP:B5:TB0","OSD:PRES:B0:P0","OSD:PRES:B0:P1","OSD:PRES:B1:P0","OSD:PRES:B1:P1","OSD:PRES:B2:P0","OSD:PRES:B2:P1","OSD:PRES:B3:P0"])
        self.validCommandList.extend(["OSD:PRES:B3:P1","OSD:PRES:B4:P0","OSD:PRES:B4:PB","OSD:PRES:B5:P0","OSD:HUM:B0","OSD:HUM:B1","OSD:HUM:B2","OSD:HUM:B3","OSD:ON","OSD:OFF","OSD:RST"])
        self.validCommandList.extend(["RW:ON","RW:OFF","RST:B0","RST:B1","RST:B2","RST:B3","ATV:PWR:0.5","ATV:PWR:1.0","ATV:PWR:1.5","ATV:PWR:2.0","ATV:PWR:2.5","ATV:PWR:3.0"])
        self.validCommandList.extend(["ATV:PWR:3.5","ATV:PWR:4.0","ATV:PWR:4.5","ATV:PWR:5.0","CUTDOWN"])

        # Create command log file
        self.commandLogger = logging.getLogger('myapp')
        self.loggerHandler = logging.FileHandler('./command.log')
        self.loggerFormatter = logging.Formatter('%(asctime)s %(message)s')
        self.loggerHandler.setFormatter(self.loggerFormatter)
        self.commandLogger.addHandler(self.loggerHandler)
        self.commandLogger.setLevel(logging.INFO)

        # Create GUI
        self.createGUI()
        
# Main loop
if __name__ == "__main__":
	root = Tkinter.Tk()
	root.title("HABIP Commands")
	root.geometry('{}x{}'.format(1200,700))
	app = MyApp(master=root)
	app.mainloop()
	root.destroy()
